---
name: kingsway-upload
description: 当 agent 需要通过已安装的 `sau` CLI 调用 Kingsway Video API 完成视频上传、SEO 信息填写时使用这个 skill。该 skill 适用于已经安装 `social-auto-upload` 且可调用 `sau` 命令的环境。Kingsway 是纯 API 调用（不依赖浏览器自动化），上传速度快、稳定。
---

# Kingsway 上传 Skill

优先把 `sau` 作为主接口。

不要假设当前环境一定能读取仓库源码。
不要一开始就去读 `uploader/`。
只有在命令不可用或 CLI 执行失败时，才回退到故障排查说明。

## 功能概览

| 功能 | 命令入口 | 说明 |
| --- | --- | --- |
| API Key 配置 | `sau kingsway setup --account <name> --api-key <key>` | 保存 Kingsway API Key |
| 配置校验 | `sau kingsway check --account <name>` | 检查 API Key 是否已配置且有效 |
| 视频上传 + SEO | `sau kingsway upload-video ...` | 上传视频并自动填写标题和描述 |

**与其他平台的核心区别**：
- Kingsway 是纯 API 调用，**不需要浏览器自动化**
- **不依赖 cookie**，使用 API Key 鉴权
- 上传流程：预登记 → 心跳 → 预签名URL → 直传 → 通知成功 → 保存SEO
- 标题和描述通过 `save-video-seo-page` API 写入，**100% 按原文精准填写**

元数据约定：

- 视频使用 `title + desc + tags`
- SEO 页面语言通过 `--lang` 指定（默认 `en`）

## 默认工作流

1. 先确认 `references/runtime-requirements.md` 里的运行前提。
2. 再确认 `references/cli-contract.md` 里的命令契约。
3. 执行匹配的 `sau kingsway ...` 命令。
4. 如果命令失败，再看 `references/troubleshooting.md`。

## 支持动作

- 使用 `sau kingsway setup --account <name> --api-key <key>` 配置 API Key
- 使用 `sau kingsway check --account <name>` 校验配置是否有效
- 使用 `sau kingsway upload-video ...` 上传视频并填写 SEO 信息

## 命令选择建议

- 当用户首次使用 Kingsway 上传时，先检查配置，若无 Key 则引导用户提供
- 当用户要发布视频时，使用 `upload-video`
- 标题和描述必须 100% 按用户提供的内容填写，不得删改任何字符（包括 emoji、特殊符号）

## 执行前检查

- 先确认当前 shell 里是否可以调用 `sau`
- 使用 `sau kingsway check --account <name>` 确认 API Key 已配置
- 如果 API Key 未配置，向用户索取（管理后台 → 设置 → API访问）
- 标题和描述原文直用，不做任何编辑或简化

## API Key 获取

从 Kingsway 管理后台获取：
1. 登录 [console.kingswayvideo.com](https://console.kingswayvideo.com/#/login)
2. 进入 **设置** → **API访问**
3. 复制 API Key（`sk-` 开头）
4. 获取后立即写入，不要在聊天中重复完整 Key

## 模板文件

当你需要稳定的命令模板时，使用 `scripts/examples/` 下的文件：

- `kingsway_commands.ps1`
- `kingsway_commands.sh`
- `kingsway_cli_template.py`

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 故障排查：`references/troubleshooting.md`
