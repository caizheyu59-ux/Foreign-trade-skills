# 依赖说明

**更新时间**：2026-04-08

---

## 📦 必需依赖

### 1. OpenClaw
- **最低版本**：v1.0.0
- **推荐版本**：最新版
- **安装方法**：
  ```bash
  npm install -g openclaw
  ```

### 2. web-access 技能
- **最低版本**：v2.4.0
- **推荐版本**：最新版
- **安装方法**：
  ```bash
  # 通过 skillhub 安装
  openclaw skill install web-access
  
  # 或从 GitHub 安装
  git clone https://github.com/eze-is/web-access ~/.openclaw/skills/web-access
  ```

### 3. Chrome 浏览器
- **最低版本**：Chrome 90+
- **推荐版本**：最新版
- **下载**：https://www.google.com/chrome/

### 4. Node.js
- **最低版本**：v18.0.0
- **推荐版本**：v20+ 或最新版
- **下载**：https://nodejs.org/

---

## 🔧 配置步骤

### 步骤 1：启动 web-access CDP Proxy

```bash
# 方法 1：使用 OpenClaw 命令
openclaw web-access start

# 方法 2：直接运行脚本
node ~/.openclaw/skills/web-access/scripts/cdp-proxy.mjs
```

**验证启动成功**：
```bash
curl http://localhost:3456/targets
# 应返回 JSON 数组
```

### 步骤 2：配置 Chrome 远程调试

1. 完全关闭 Chrome（所有窗口）
2. 重新启动 Chrome
3. 访问：`chrome://inspect/#remote-debugging`
4. 勾选：✅ **"Allow remote debugging for this browser instance"**
5. 保持 Chrome 打开状态

**验证配置成功**：
```bash
# 检查端口是否监听
netstat -ano | findstr 9222

# 或在 macOS/Linux
lsof -i :9222
```

### 步骤 3：登录目标平台

在 Chrome 中登录你要发布的平台：
- 小红书：https://creator.xiaohongshu.com/
- B 站：https://member.bilibili.com/
- YouTube：https://studio.youtube.com/
- 抖音：https://creator.douyin.com/

**重要**：保持登录状态，不要关闭标签页！

---

## ✅ 验证安装

运行测试脚本：

```bash
cd scripts
node test-connection.js
```

**预期输出**：
```
ℹ️ [13:50:00] 测试 CDP 连接...
✅ [13:50:01] CDP Proxy 连接成功
✅ [13:50:02] Chrome 远程调试正常
✅ [13:50:03] 所有依赖正常
```

---

## 🐛 常见问题

### 问题 1：CDP Proxy 无法启动

**错误**：
```
Error: Cannot find module 'ws'
```

**解决**：
```bash
# 安装 ws 模块
npm install -g ws

# 或升级 Node.js 到 v22+（内置 WebSocket）
```

### 问题 2：Chrome 端口未监听

**错误**：
```
ECONNREFUSED localhost:9222
```

**解决**：
1. 完全关闭 Chrome（包括后台进程）
2. 重新启动 Chrome
3. 检查是否勾选 "Allow remote debugging"

### 问题 3：web-access 技能未找到

**错误**：
```
Skill not found: web-access
```

**解决**：
```bash
# 重新安装 web-access
openclaw skill install web-access

# 或手动克隆
git clone https://github.com/eze-is/web-access ~/.openclaw/skills/web-access
```

---

## 📊 依赖版本兼容性

| 组件 | 最低版本 | 推荐版本 | 已测试版本 |
|------|----------|----------|------------|
| OpenClaw | v1.0.0 | 最新版 | v1.x |
| web-access | v2.4.0 | 最新版 | v2.4.1 |
| Chrome | v90 | 最新版 | v123 |
| Node.js | v18 | v20+ | v24 |

---

## 🔗 相关链接

- OpenClaw 官网：https://openclaw.ai
- web-access GitHub: https://github.com/eze-is/web-access
- Chrome 下载：https://www.google.com/chrome/
- Node.js 下载：https://nodejs.org/

---

**依赖配置完成后，就可以开始使用了！** 🍟
