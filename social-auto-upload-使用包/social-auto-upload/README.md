# social-auto-upload

`social-auto-upload` 是一个强大的自动化工具，旨在帮助内容创作者和运营者高效地将视频内容一键发布到多个国内外主流社交媒体平台。
项目实现了对 `抖音`、`Bilibili`、`小红书`、`快手`、`视频号`、`百家号` 以及 `TikTok` 等平台的视频上传、定时发布等功能。
结合各平台 `uploader` 模块，您可以轻松配置和扩展支持的平台，并通过示例脚本快速上手。

<img src="media/show/tkupload.gif" alt="tiktok show" width="800"/>



---


## 目录

- [💡 功能特性](#💡功能特性)
- [💾 安装指南](#💾安装指南)
- [🤖 AI Agent](#🤖ai-agent)
- [🏁 快速开始](#🏁快速开始)
- [🗂️ 重构计划](#🗂️重构计划)
- [🐇 项目背景](#🐇项目背景)
- [📃 详细文档](#📃详细文档)
- [🤝 贡献指南](#🤝贡献指南)
- [🙏 致谢](#🙏致谢)
- [🐾 维护者](#🐾维护者)
- [📜 许可证](#📜许可证)
- [⭐ Star History](#⭐Star-History)

## 💡功能特性

| 平台 | 登录/账号准备 | 视频上传 | 图文上传 | 定时发布 | CLI | Skill | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 抖音 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 当前主线重构最完整 |
| Bilibili | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | 运行时自动准备 `biliup` |
| 小红书（浏览器版） | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 浏览器自动化，CLI/Skill 已接入 |
| 快手 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 浏览器自动化，CLI/Skill 初版已接入 |
| 视频号 | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | 对应 `tencent_uploader` |
| 百家号 | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | 浏览器自动化 |
| TikTok | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | 当前示例走 Chrome 版实现 |
| Kingsway Video | ❌ (API Key) | ✅ | ❌ | ✅ | ✅ | ✅ | 纯 API 调用，预签名 URL 直传 + 自动 SEO 填写 |

### AI这么强，为什么还需要这个项目
在你使用AI的能力，browser agent等等，每次都让 agent 重新解析网页、截图理解, 临场判断
该项目经过大量验证，上传这种 高频，重复，无聊的工作交给脚本和程序去执行


## 💾安装指南

### 自己上手使用
如果你只是普通用户，不准备借助 agent 客户端，直接看

安装、更新、环境准备已经统一收敛到文档：

- [安装说明](./docs/install.md)
- [更新说明](./docs/update.md)


### AGENT

```
AI的发展毋庸置疑，希望你遇到这种安装和使用，不要再怯场，而是交给各种AI Agent来协助你
```

如果你准备把这个仓库直接交给 `OpenClaw`、`Codex`、`Claude Code` 来安装和使用

先把仓库给 agent，再把这份启动提示词一起发给它：

- [Agent Bootstrap Prompt](./docs/agent-bootstrap.md)

这份提示词会引导 agent：

- 优先按当前主线安装项目
- 优先使用 `uv`、`sau` CLI 和 `skills/`
- 先验证 `bilibili`、`douyin`、`kuaishou`、`xiaohongshu`、`kingsway` 五个平台入口是否可用

### 🤖 Agent Skills（AI Agent 专用）

本项目为每个 CLI 平台提供对应的 **SKILL.md**，Agent 可直接读取，无需理解源码：

| 平台 | Skill 文档 | 上传方式 | 说明 |
| --- | --- | --- | --- |
| 抖音 | [Douyin Upload Skill](./skills/douyin-upload/SKILL.md) | 视频 + 图文 | 浏览器自动化，无头模式 |
| 快手 | [Kuaishou Upload Skill](./skills/kuaishou-upload/SKILL.md) | 视频 + 图文 | 浏览器自动化，无头模式 |
| 小红书 | [Xiaohongshu Upload Skill](./skills/xiaohongshu-upload/SKILL.md) | 视频 + 图文 | 浏览器自动化 |
| B 站 | [Bilibili Upload Skill](./skills/bilibili-upload/SKILL.md) | 视频 | 自动准备 `biliup` |
| Kingsway | [Kingsway Upload Skill](./skills/kingsway-upload/SKILL.md) | 视频 | ⚡ 纯 API 调用，无需浏览器 |

**Kingsway 特别说明**：
- Kingsway 是唯一一个**纯 API 上传**的平台，不需要浏览器自动化
- 上传速度快、稳定性高，不受平台检测风险影响
- 通过预签名 URL 直传，标题和描述通过 API 100% 精准填写
- 首次使用需要先配置 API Key：`sau kingsway setup --account <name> --api-key sk-xxx`

### 补充说明：

- CLI 使用请看：[CLI 使用说明](./docs/CLI.md)
- 历史 Web 说明请看：[历史 Web 版本说明](./docs/legacy-web.md)
- 各平台 Skill 详见上方「🤖 Agent Skills」表格
- `requirements.txt` 目前主要用于历史兼容路径，普通用户不需要优先使用它




## 🗂️重构计划

项目正在进行一轮整体重构，当前重构重点是：

- 各平台 uploader 的结构收敛
- CLI 统一接入
- 面向 OpenClaw、Codex、 Claude Code 等工具的 skill 化
- 更换为 `patchright` 驱动，提升兼容性与隐蔽性
- 主线优先围绕无头模式推进

"无头模式（headless）"，指的是浏览器在后台运行，不弹出可见窗口，但自动化流程仍然会照常执行。这样更适合 CLI、服务端、自动任务和 agent 场景。

Web 端相关代码仍然保留，但已经不是当前主线，不保证可直接运行，也不保证与当前 uploader/CLI 完全同步。


## 🏁快速开始

### 方式 1：使用 CLI

当前抖音、快手、小红书、Bilibili、Kingsway Video 已经接入 CLI：

```bash
sau douyin login --account <account_name>
sau douyin check --account <account_name>
sau douyin upload-video --account <account_name> --file videos/demo.mp4 --title "示例标题" --desc "示例简介"
sau douyin upload-note --account <account_name> --images videos/1.png videos/2.png --title "图文标题" --note "图文正文"

sau kuaishou login --account <account_name>
sau kuaishou check --account <account_name>
sau kuaishou upload-video --account <account_name> --file videos/demo.mp4 --title "示例标题" --desc "示例简介"
sau kuaishou upload-note --account <account_name> --images videos/1.png videos/2.png videos/3.png --title "图文标题" --note "图文正文"

sau xiaohongshu login --account <account_name>
sau xiaohongshu check --account <account_name>
sau xiaohongshu upload-video --account <account_name> --file videos/demo.mp4 --title "示例标题" --desc "示例简介"
sau xiaohongshu upload-note --account <account_name> --images videos/1.png videos/2.png videos/3.png --title "图文标题" --note "图文正文"

sau bilibili login --account <account_name>
sau bilibili check --account <account_name>
sau bilibili upload-video --account <account_name> --file videos/demo.mp4 --title "示例标题" --desc "示例简介" --tid 249

sau kingsway setup --account <account_name> --api-key <sk-xxx>
sau kingsway check --account <account_name>
sau kingsway upload-video --account <account_name> --file videos/demo.mp4 --title "示例标题" --desc "示例简介" --lang en
```

补充说明：

- `creator` 之类的名字只是示例值，真正含义是 `account_name`
- 一个 `account_name` 对应一个账号文件，可以准备多个账号，也可以按账号名并发执行任务
- 浏览器平台统一约定：
- 视频使用 `title + desc + tags`
- 图文使用 `title + note + tags`
- Bilibili CLI 不要求用户手动安装 `biliup`
- 首次运行相关命令时，程序会自动下载 `biliup`
- 后续运行会自动检查上游 release 并更新
- Bilibili 登录建议由用户自己在本地真实终端里执行；如果终端二维码显示不完整，可以直接打开当前目录下的 `qrcode.png` 扫码

### 方式 2：使用 examples

`examples/` 目录里同时存在两类脚本：

- 当前主线 CLI 包装示例
- 历史直连 uploader 示例

对抖音、快手、小红书、Bilibili 来说，当前主线优先使用上面的 `sau ...` CLI。
下面这些脚本主要是历史直连 uploader 示例或调试入口：

- `examples/upload_to_douyin.py`
- `examples/upload_video_to_bilibili.py`
- `examples/upload_to_kuaishou.py`
- `examples/upload_video_to_tencent.py`
- `examples/upload_video_to_baijiahao.py`
- `examples/upload_video_to_tiktok.py`
- `examples/upload_video_to_xiaohongshu.py`

## 🐇项目背景

本项目用于自动化管理多平台社交媒体视频发布，支持定时发布、批量上传等功能。定时发布相关逻辑默认基于"第二天"的时间进行计算。

## 📃详细文档

详细文档请查看仓库 `docs/` 目录下的文件。

## 🐾维护者

### Maintainer

|  |  |
| --- | --- |
| **Morment** | Kingsway Video 产品运营 |
| **GitHub** | [Kingsway Video](https://github.com/kingswayvideo) |
| **官网** | [kingswayvideo.com](https://www.kingswayvideo.com) |

本项目由 **Morment** 维护，用于 Kingsway Video 团队内部的社媒自动化上传与管理。如有问题或建议，欢迎通过 GitHub Issues 联系。

## 🤝贡献指南

欢迎各种形式的贡献，包括但不限于：

-   提交 Bug报告 和 Feature请求。
-   改进代码、文档。
-   分享使用经验和教程。

如果您希望贡献代码，请遵循以下步骤：

1.  Fork 本仓库。
2.  创建一个新的分支 (`git checkout -b feature/YourFeature` 或 `bugfix/YourBugfix`)。
3.  提交您的更改 (`git commit -m 'Add some feature'`)。
4.  Push到您的分支 (`git push origin feature/YourFeature`)。
5.  创建一个 Pull Request。

## 🙏致谢

本项目的 Bilibili 上传能力基于开源项目 `biliup` 的能力进行接入与封装。
感谢 `biliup` 项目及其贡献者提供的基础能力：

- https://github.com/biliup/biliup

## 📜许可证

本项目暂时采用 [MIT License](LICENSE) 开源许可证。

## ⭐Star-History

> 如果这个项目对您有帮助，请给一个 ⭐ Star 以表示支持！

[![Star History Chart](https://api.star-history.com/svg?repos=dreammis/social-auto-upload&type=Date)](https://star-history.com/#dreammis/social-auto-upload&Date)

## Community
LINUX DO - The New Ideal Community
