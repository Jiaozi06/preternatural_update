"""Merge the official PC package into versions.json without losing history."""
import json
import re
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

API = 'https://sphinx.preternatural.cn/api/official/channel/list?gametag=preternatural'
CATALOG = Path(__file__).resolve().parents[1] / 'versions.json'
HOSTS = {'op-file.preternatural.cc', 'op-file.chaoziran.com'}


def validate(package):
    if not re.fullmatch(r'\d+\.\d+\.\d+\.\d+', package['version']):
        raise ValueError('Invalid version')
    url = urlparse(package['url'])
    if url.scheme != 'https' or url.hostname not in HOSTS:
        raise ValueError('Unexpected download host')
    if not url.path.endswith('winsetup_official_win_901_' + package['version'] + '.exe'):
        raise ValueError('URL/version mismatch')
    size = package.get('size')
    if size is not None and (type(size) is not int or size <= 0):
        raise ValueError('Invalid size')


def merge(existing, response):
    if response.get('code') != 0 or not isinstance(response.get('data'), list):
        raise ValueError('Official API failed')
    pc = next(x for x in response['data'] if x.get('channelName') == 'pc')
    match = re.fullmatch(r'winsetup_official_win_901_(\d+\.\d+\.\d+\.\d+)\.exe', pc['pkgName'])
    if not match:
        raise ValueError('Unexpected PC filename')
    latest = dict(version=match[1], url=pc['pkgURL'], size=pc.get('pkgSize'), official=True)
    validate(latest)
    packages = {}
    for item in existing:
        validate(item)
        packages[item['version']] = {**item, 'official': False}
    packages[latest['version']] = latest
    return sorted(packages.values(), key=lambda x: tuple(map(int, x['version'].split('.'))), reverse=True)


def fetch():
    for attempt in range(3):
        try:
            request = urllib.request.Request(API, headers={'User-Agent': 'preternatural-update/1.0'})
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def main():
    existing = json.loads(CATALOG.read_text(encoding='utf-8-sig'))
    updated = merge(existing, fetch())
    content = json.dumps(updated, ensure_ascii=False, indent=2) + '\n'
    if content != CATALOG.read_text(encoding='utf-8-sig'):
        temp = CATALOG.with_suffix('.json.tmp')
        temp.write_text(content, encoding='utf-8')
        temp.replace(CATALOG)
        print('Updated:', updated[0]['version'], '| packages:', len(updated))
    else:
        print('No change')


if __name__ == '__main__':
    main()
