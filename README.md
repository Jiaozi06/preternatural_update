# 超自然行动组 PC 版本目录

[versions.json](versions.json) 保存版本号、官方下载地址、文件大小（未知为 null）及 official（官方 PC 接口当前返回版本）。按四段数字倒序排列。

订阅地址：https://raw.githubusercontent.com/Jiaozi06/preternatural_update/main/versions.json

GitHub Actions 每小时第 17 分钟读取官方接口的 PC 渠道，自动合并新增版本，保留所有历史记录，内容没变时不提交。也可以在 Actions 页面手动 Run workflow。GitHub 定时任务可能延迟；长期没有仓库活动时也可能被平台暂停。

官方接口：https://sphinx.preternatural.cn/api/official/channel/list?gametag=preternatural

历史地址由项目维护者提供，不代表已逐个验证仍可下载。任务只获取接口列表，不遍历 CDN 或下载完整安装包。接口异常、字段不匹配或 URL 不属于官方文件域名时任务失败，原 JSON 不变。

本地更新：`python scripts/update_versions.py`（Python 3.12，无第三方依赖）。

添加发现的历史版本时按现有结构编辑 versions.json，official 设为 false，size 未知设为 null。
