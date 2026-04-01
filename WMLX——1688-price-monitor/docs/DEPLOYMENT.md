# 部署指南

本文档介绍如何将 1688 价格监控系统部署到生产环境。

---

## 📋 部署方式

### 方式一：本地部署（开发/测试）

适用于个人使用和测试。

#### 1. 克隆仓库

```bash
git clone https://github.com/your-username/1688-price-monitor.git
cd 1688-price-monitor
```

#### 2. 安装依赖

```bash
npm install
```

#### 3. 配置环境

复制示例配置：

```bash
cp config/monitored-products.json.example config/monitored-products.json
```

编辑配置文件，添加监控商品和通知设置。

#### 4. 连接通知渠道

```bash
# WhatsApp
openclaw channels login --channel whatsapp --account default

# 飞书
openclaw channels login --channel feishu --account default
```

#### 5. 测试运行

```bash
node price-alert.js
```

---

### 方式二：OpenClaw Skill 部署（推荐）

适用于 OpenClaw 用户，集成到工作区。

#### 1. 复制到 Skills 目录

```bash
cp -r 1688-price-monitor ~/.openclaw/workspace-hamburger/skills/
```

或在 Windows 上：

```powershell
Copy-Item -Recurse 1688-price-monitor C:\Users\your-username\.openclaw\workspace-hamburger\skills\
```

#### 2. 安装依赖

```bash
cd ~/.openclaw/workspace-hamburger/skills/1688-price-monitor
npm install
```

#### 3. 配置

编辑 `config/monitored-products.json`。

#### 4. 配置定时任务

编辑 `HEARTBEAT.md`（工作区根目录）：

```markdown
## 1688 价格监控

**执行频率：** 每小时整点

**执行命令：**
```bash
cd skills/1688-price-monitor
node price-alert.js
```
```

#### 5. 测试

```bash
node price-alert.js
```

---

### 方式三：服务器部署（生产环境）

适用于 24/7 不间断监控。

#### 前置要求

- Linux 服务器（Ubuntu/CentOS）
- Node.js 18+
- PM2（进程管理）
- OpenClaw Gateway

#### 1. 安装 Node.js

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs
```

#### 2. 克隆项目

```bash
cd /opt
git clone https://github.com/your-username/1688-price-monitor.git
cd 1688-price-monitor
npm install
```

#### 3. 安装 PM2

```bash
npm install -g pm2
```

#### 4. 配置 PM2

创建 `ecosystem.config.js`：

```javascript
module.exports = {
  apps: [{
    name: '1688-price-monitor',
    script: 'price-alert.js',
    cron_restart: '0 * * * *',  // 每小时执行
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
```

#### 5. 启动服务

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

#### 6. 配置通知

按照 [WHATSAPP_SETUP.md](./WHATSAPP_SETUP.md) 或 [FEISHU_SETUP.md](./FEISHU_SETUP.md) 配置通知渠道。

#### 7. 监控日志

```bash
pm2 logs 1688-price-monitor
```

---

## 🔐 安全配置

### 环境变量

创建 `.env` 文件：

```bash
# 通知配置
WHATSAPP_TARGET=+86XXXXXXXXXXX
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx

# 监控配置
CHECK_INTERVAL_HOURS=1
NOTIFY_THRESHOLD=5

# 安静时间
QUIET_HOURS_START=23
QUIET_HOURS_END=8
```

### Git 忽略

确保 `.gitignore` 包含：

```gitignore
# 敏感信息
.env
config/monitored-products.json

# 数据文件
data/*.csv
data/*.json

# 依赖
node_modules/
```

### 文件权限

```bash
# 设置配置文件权限
chmod 600 config/monitored-products.json
chmod 600 .env

# 设置脚本执行权限
chmod +x price-alert.js
```

---

## 📊 监控与维护

### 日志管理

```bash
# 查看日志
pm2 logs 1688-price-monitor

# 日志轮转（PM2 自动处理）
pm2 flush
```

### 数据备份

```bash
# 每日备份
0 2 * * * cp data/price-history.csv /backup/price-history-$(date +\%Y\%m\%d).csv

# 清理旧数据（保留 30 天）
find /backup -name "price-history-*.csv" -mtime +30 -delete
```

### 健康检查

创建 `healthcheck.js`：

```javascript
const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'data', 'price-history.csv');
const lastCheck = fs.statSync(dataPath).mtime;
const now = new Date();
const hoursSinceCheck = (now - lastCheck) / (1000 * 60 * 60);

if (hoursSinceCheck > 2) {
    console.error('❌ 监控异常：超过 2 小时未执行');
    process.exit(1);
}

console.log('✅ 监控正常：上次检查在', hoursSinceCheck.toFixed(1), '小时前');
```

---

## 🔄 更新与升级

### 从 Git 更新

```bash
cd /opt/1688-price-monitor
git pull
npm install  # 如果有新依赖
pm2 restart 1688-price-monitor
```

### 备份配置

更新前备份配置文件：

```bash
cp config/monitored-products.json config/monitored-products.json.bak
cp .env .env.bak
```

### 回滚

如果更新后出现问题：

```bash
git checkout <previous-tag>
npm install
pm2 restart 1688-price-monitor
```

---

## 📱 多渠道通知配置

### 同时启用 WhatsApp 和飞书

编辑 `config/monitored-products.json`：

```json
{
  "notifications": {
    "whatsapp": {
      "enabled": true,
      "target": "+86XXXXXXXXXXX"
    },
    "feishu": {
      "enabled": true,
      "type": "webhook",
      "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    }
  }
}
```

---

## 🧪 测试部署

### 完整测试流程

```bash
# 1. 测试价格抓取
node fetch-price.js <targetId>

# 2. 测试通知发送
node test-whatsapp.js +86XXXXXXXXXXX

# 3. 测试完整流程
node price-alert.js

# 4. 检查数据保存
Get-Content data/price-history.csv
```

---

## ❓ 部署问题

### 问题 1：PM2 启动失败

**错误：** `Error: Cannot find module`

**解决：**
```bash
npm install
pm2 restart 1688-price-monitor
```

### 问题 2：权限不足

**错误：** `Permission denied`

**解决：**
```bash
chmod +x price-alert.js
chown -R $USER:$USER /opt/1688-price-monitor
```

### 问题 3：通知不发送

**检查：**
1. 通知渠道已连接
2. 配置文件正确
3. 网络连接正常

---

## 📚 参考资源

- [PM2 文档](https://pm2.keymetrics.io/docs/usage/quick-start/)
- [Node.js 部署指南](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [OpenClaw 文档](https://docs.openclaw.ai/)

---

**版本：** 1.0.0  
**最后更新：** 2026-04-01
