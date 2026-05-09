# social-auto-upload

> 多平台社媒视频/图文自动上传工具

支持：抖音、快手、小红书、B站、Kingsway、TikTok、视频号、百家号

---

## 安装

1. 把 social-auto-upload 文件夹复制到 OpenClaw 的 skills 目录
2. 进入目录运行: uv pip install -e .
3. 安装浏览器驱动: patchright install chromium
4. 验证: sau --help

## 环境要求

- Python 3.10 ~ 3.12
- Google Chrome

## 各平台命令

| 平台 | 登录 | 上传视频 |
|------|------|---------|
| 抖音 | sau douyin login --account <name> | sau douyin upload-video --account <name> --file video.mp4 --title "标题" --desc "描述" |
| 快手 | sau kuaishou login --account <name> | sau kuaishou upload-video --account <name> --file video.mp4 --title "标题" --desc "描述" |
| 小红书 | sau xiaohongshu login --account <name> | sau xiaohongshu upload-video --account <name> --file video.mp4 --title "标题" --desc "描述" |
| B站 | sau bilibili login --account <name> | sau bilibili upload-video --account <name> --file video.mp4 --title "标题" --desc "描述" --tid 249 |
| Kingsway | sau kingsway setup --account <name> --api-key sk-xxx | sau kingsway upload-video --account <name> --file video.mp4 --title "标题" --desc "描述" |

## 图文上传

sau douyin upload-note --account <name> --images img1.png img2.png --title "标题" --note "正文"
sau xiaohongshu upload-note --account <name> --images img1.png img2.png --title "标题" --note "正文"
sau kuaishou upload-note --account <name> --images img1.png img2.png --title "标题" --note "正文"

## 定时发布

sau douyin upload-video --account <name> --file video.mp4 --title "标题" --desc "描述" --schedule "2026-05-10 10:00"

## 描述包含引号

用 --desc-file 从文件读取，避免 shell 引号问题

## AI Agent Skills

skills/ 目录下有每个平台的 SKILL.md，AI Agent 可直接读取使用。