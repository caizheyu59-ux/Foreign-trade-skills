# Kingsway 上传 Skill - CLI 契约

## 命令格式

```powershell
sau kingsway <action> [options]
```

## 子命令

### check - 检查配置

```powershell
sau kingsway check --account <name>
# 输出: valid 或 invalid
```

### setup - 配置 API Key

```powershell
sau kingsway setup --account <name> --api-key <key> [--base-url <url>]
```

### upload-video - 上传视频

```powershell
sau kingsway upload-video `
  --account <name> `
  --file <video.mp4> `
  --title "<标题>" `
  --desc "<描述>" `
  [--tags "tag1,tag2,tag3"] `
  [--lang en|zh|ja|ko]
```

参数说明：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--account` | ✅ | Kingsway 账号名称 |
| `--file` | ✅ | 视频文件路径 |
| `--title` | ✅ | 视频标题 |
| `--desc` | 可选 | 视频描述 |
| `--tags` | 可选 | 逗号分隔的标签 |
| `--lang` | 可选 | SEO 页面语言，默认 `en` |

## 上传流程（内部自动执行）

1. **预登记** → 获取 `sourceVideoId`
2. **心跳保活** → 每 ≤10 秒一次，防止上传超时
3. **获取预签名 PUT URL** → 腾讯云 COS
4. **直传视频** → HTTP PUT 到预签名 URL
5. **通知成功** → 触发 Kingsway 转码
6. **保存 SEO** → 写入标题和描述

## 语言支持

| 语言 | --lang 值 |
|------|-----------|
| 英语（默认） | `en` |
| 中文 | `zh` |
| 日语 | `ja` |
| 韩语 | `ko` |
| 繁体中文 | `zh-HK` |
