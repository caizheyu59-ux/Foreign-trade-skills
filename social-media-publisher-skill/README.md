# Social Media Publisher Skill

**版本**：1.1.0  
**发布日期**：2026-04-08  
**作者**：薯条 + 小龙虾  
**许可证**：MIT

**语言**：[中文](README.md) | [English](README.en.md)

---

## 📋 简介

这是一个多平台视频发布自动化技能，支持通过 CDP（Chrome DevTools Protocol）自动上传视频到主流社交媒体平台。

**支持平台**：
- ✅ 小红书 (Xiaohongshu)
- ✅ B 站 (Bilibili)
- ✅ YouTube
- ✅ 抖音 (Douyin)

**核心功能**：
- 自动上传视频文件
- 自动填写标题和描述
- 自动添加标签/话题
- 支持保存草稿或发布

---

## 🚀 快速开始

### 前提条件

**必需依赖**：
1. ✅ **OpenClaw** v1.0.0+
2. ✅ **web-access** 技能 v2.4.0+
3. ✅ **Chrome 浏览器** v90+（开启远程调试）
4. ✅ **Node.js** v18+（运行脚本）

**详细依赖说明**：见 [`docs/DEPENDENCIES.md`](docs/DEPENDENCIES.md)

### 安装步骤

1. **安装依赖**
   ```bash
   # 安装 OpenClaw（如果未安装）
   npm install -g openclaw
   
   # 安装 web-access 技能
   openclaw skill install web-access
   ```

2. **复制技能文件**
   ```bash
   # 将整个文件夹复制到 OpenClaw skills 目录
   cp -r social-media-publisher-skill ~/.openclaw/skills/
   ```

3. **配置 Chrome 远程调试**
   - 打开 Chrome 浏览器
   - 访问：`chrome://inspect/#remote-debugging`
   - 勾选：✅ "Allow remote debugging for this browser instance"
   - 重启 Chrome（如果需要）

4. **启动 web-access CDP Proxy**
   ```bash
   node ~/.openclaw/skills/web-access/scripts/cdp-proxy.mjs
   ```
   
   **验证启动成功**：
   ```bash
   curl http://localhost:3456/targets
   # 应返回 JSON 数组
   ```

---

## 📖 使用方法

### 测试连接

在开始之前，先测试依赖是否正常：

```bash
cd social-media-publisher-skill/scripts
node test-connection.js
```

**预期输出**：
```
ℹ️  测试 CDP 连接...

✅ CDP Proxy 连接成功
   当前 tab 数：X
✅ Chrome 远程调试正常

✅ 所有依赖正常
```

### 基本命令

```bash
# 发布视频到小红书
发布视频到小红书，视频在 C:\Users\caizheyu\Desktop\video.mp4，内容在 C:\Users\caizheyu\Desktop\content.txt

# 发布视频到 B 站
上传视频到 B 站，内容文件在 D:\videos\content.txt

# 测试抖音上传
测试抖音上传
```

### 内容文件格式

创建文本文件（如 `content.txt`），格式如下：

```
1. 短标题
AI 时代，如何让海外客户一眼信任你？

4. 第一人称摘要
AI 时代的信任贵如金：
现在的 B2B 行业，信任就是命脉。因为 AI 太强大，客户越来越怕看到的东西是假的。

怎么玩转这个功能：
客户可以实时切换不同的镜头，还能放大看细节。你可以直接发链接给客户，或者干脆内嵌到你的独立站里，当场解惑。

标签：#外贸独立站 #跨境电商 #电商售后 #产品售后
```

---

## 🔧 技术细节

### CDP Proxy API

所有操作都通过 web-access 的 CDP Proxy 执行（端口 3456）：

```bash
# 列出所有 tab
curl -s http://localhost:3456/targets

# 打开页面
curl -s "http://localhost:3456/new?url=https://example.com"

# 执行 JS
curl -s -X POST "http://localhost:3456/eval?target=TARGET_ID" -d "document.title"

# 上传文件
curl -s -X POST "http://localhost:3456/setFiles?target=TARGET_ID" -d '{"selector":"input[type=file]","files":["video.mp4"]}'

# 点击元素
curl -s -X POST "http://localhost:3456/click?target=TARGET_ID" -d 'button[type="submit"]'

# 截图
curl -s "http://localhost:3456/screenshot?target=TARGET_ID&file=check.png"
```

### 平台选择器

每个平台都有精确的 CSS 选择器，详见：
- `docs/platform-selectors.md` - 完整选择器列表
- `docs/buttons.md` - 按钮选择器汇总

---

## 📁 文件结构

```
social-media-publisher-skill/
├── SKILL.md              # 技能主文件
├── README.md             # 本文件
├── docs/                 # 文档目录
│   ├── platform-selectors.md    # 平台选择器
│   ├── buttons.md               # 按钮选择器
│   ├── quick-start.md           # 快速开始指南
│   └── troubleshooting.md       # 故障排除
├── scripts/              # 脚本目录
│   ├── upload-xhs.mjs    # 小红书上传脚本
│   ├── upload-bilibili.mjs     # B 站上传脚本
│   ├── upload-youtube.mjs      # YouTube 上传脚本
│   └── upload-douyin.mjs       # 抖音上传脚本
└── examples/             # 示例目录
    └── content-template.txt      # 内容模板
```

---

## ⚠️ 注意事项

### 1. Chrome 远程调试
- 必须开启远程调试端口（默认 9222）
- 必须勾选 "Allow remote debugging"
- 可能需要重启 Chrome 生效

### 2. 登录状态
- 所有平台都需要提前在 Chrome 中登录
- CDP 复用 Chrome 登录态
- 登录失效需手动重新登录

### 3. 文件上传
- 使用 `DOM.setFileInputFiles` + `objectId`
- 不要使用 `nodeId`（会失败）
- 上传后必须触发 `change` 事件

### 4. 文本输入
- 标题：直接设置 `value`（YouTube 除外）
- 描述：使用 `execCommand` 或 `innerText`
- 标签：输入后按 `Enter` 确认

---

## 🐛 故障排除

### 常见问题

**问题 1**：CDP 连接失败
```
错误：ECONNREFUSED
解决：检查 Chrome 是否开启远程调试，端口 9222 是否监听
```

**问题 2**：文件上传失败
```
错误：Cannot set files
解决：确保使用 objectId 而非 nodeId
```

**问题 3**：YouTube 描述填写无效
```
错误：描述为空
解决：必须使用 document.execCommand('insertText')，不能直接设置 innerText
```

**问题 4**：抖音标签不显示
```
错误：标签未添加
解决：在描述框内直接输入 #话题 格式，无需单独输入框
```

详见：`docs/troubleshooting.md`

---

## 📚 文档

- **README.md** - 本文件，快速入门
- **docs/platform-selectors.md** - 所有平台的完整选择器
- **docs/buttons.md** - 保存/发布按钮选择器
- **docs/quick-start.md** - 5 分钟快速开始
- **docs/troubleshooting.md** - 故障排除指南

---

## 📝 更新日志

### v1.0.0 (2026-04-08)
- ✅ 初始版本发布
- ✅ 支持 4 个主流平台
- ✅ 完整的文档和示例
- ✅ 所有平台已测试验证

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub 仓库**：（待创建）

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

**祝你发布顺利！** 🍟
