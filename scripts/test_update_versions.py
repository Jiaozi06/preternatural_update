import copy
import unittest
from update_versions import merge

class MergeTests(unittest.TestCase):
    def setUp(self):
        self.old = [{'version': '1.9.1.1', 'url': 'https://op-file.preternatural.cc/pntlpro/apk/winsetup_official_win_901_1.9.1.1.exe', 'size': None, 'official': True}]
        self.response = {'code': 0, 'data': [{'channelName': 'official', 'pkgName': 'android.apk'}, {'channelName': 'pc', 'pkgName': 'winsetup_official_win_901_1.31.2.1.exe', 'pkgURL': 'https://op-file.chaoziran.com/pntlpro/apk/winsetup_official_win_901_1.31.2.1.exe', 'pkgSize': 100}]}
    def test_history_sort_and_idempotence(self):
        new = merge(self.old, self.response)
        self.assertEqual(len(new), 2)
        self.assertEqual(new[0]['version'], '1.31.2.1')
        self.assertFalse(new[1]['official'])
        self.assertEqual(merge(new, self.response), new)
        self.assertTrue(self.old[0]['official'])
    def test_invalid_response_does_not_change_input(self):
        before = copy.deepcopy(self.old)
        self.response['data'][1]['pkgURL'] = 'https://evil.com/setup.exe'
        with self.assertRaises(ValueError):
            merge(self.old, self.response)
        self.assertEqual(before, self.old)
    def test_api_error(self):
        with self.assertRaises(ValueError):
            merge(self.old, {'code': 1, 'data': []})

if __name__ == '__main__':
    unittest.main()
