# 1688 价格监控系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://docs.openclaw.ai/)

> 自动监控 1688 商品价格变化，实时推送 WhatsApp/飞书通知

**实时价格监控 · 多渠道通知 · 定时任务 · 历史记录**

---

## 🎯 功能特性

- ✅ **自动价格抓取** - 使用 CDP 协议直接抓取 1688 商品实时价格
- ✅ **价格变化检测** - 可配置阈值（默认 5%），低于目标价自动提醒
- ✅ **多渠道通知** - 支持 WhatsApp、飞书、邮件等多种通知方式
- ✅ **定时任务** - 每小时自动执行，支持自定义频率
- ✅ **历史记录** - CSV 格式保存价格历史，支持趋势分析
- ✅ **安静时间** - 23:00-08:00 免打扰模式
- ✅ **防重复通知** - 同一商品 1 小时内不重复发送

---

## 📦 快速开始

### 前置要求

- Node.js 18+
- OpenClaw 已安装并配置
- WhatsApp 或飞书账号

### 1. 安装依赖

```bash
cd 1688-price-monitor
npm install
```

### 2. 配置监控商品

编辑 `config/monitored-products.json`：

```json
{
  "products": [
    {
      "id": "product-001",
      "name": "商品名称",
      "url": "https://detail.1688.com/offer/633830968371.html",
      "target_price": 45.00,
      "notify_threshold": 5
    }
  ],
  "notifications": {
    "whatsapp": {
      "enabled": true,
      "target": "+86XXXXXXXXXXX"
    }
  }
}
```

### 3. 配置通知渠道

#### WhatsApp

```bash
openclaw channels login --channel whatsapp --account default
```

扫描二维码完成连接。

#### 飞书

```bash
openclaw channels login --channel feishu --account default
```

或使用飞书机器人 Webhook（见 [FEISHU_SETUP.md](./docs/FEISHU_SETUP.md)）。

### 4. 测试运行

```bash
node price-alert.js
```

### 5. 配置定时任务

编辑 `HEARTBEAT.md`（OpenClaw 工作区根目录）：

```markdown
## 1688 价格监控

**执行频率：** 每小时整点

**执行命令：**
```bash
cd skills/1688-price-monitor
node price-alert.js
```
```

---

## 📁 项目结构

```
1688-price-monitor/
├── README.md                       # 项目说明（本文件）
├── SKILL.md                        # OpenClaw 技能定义
├── price-alert.js                  # 价格提醒主脚本 ⭐
├── fetch-price.js                  # CDP 价格抓取脚本
├── test-whatsapp.js                # WhatsApp 测试工具
├── package.json                    # Node.js 配置
├── .gitignore                      # Git 忽略规则
├── config/
│   └── monitored-products.json     # 监控商品配置 ⚙️
├── data/
│   ├── price-history.csv           # 价格历史记录 📊
│   └── alert-log.json              # 提醒发送记录 📝
└── docs/
    ├── WHATSAPP_SETUP.md           # WhatsApp 配置指南
    ├── FEISHU_SETUP.md             # 飞书配置指南
    ├── USER_GUIDE.md               # 用户操作指南
    └── DEPLOYMENT.md               # 部署指南
```

---

## 🚀 使用示例

### 监控单个商品

```bash
node price-alert.js
```

### 查看价格历史

```bash
# PowerShell
Get-Content data/price-history.csv

# 或使用 Node.js
node -e "console.log(require('fs').readFileSync('data/price-history.csv', 'utf-8'))"
```

### 查看提醒记录

```bash
Get-Content data/alert-log.json | ConvertFrom-Json
```

### 测试 WhatsApp 通知

```bash
node test-whatsapp.js +86XXXXXXXXXXX
```

---

## 📊 输出示例

### 价格历史 (CSV)

```csv
timestamp,target_id,product_name,price,price_range,min_order,supplier
2026-04-01T07:49:20.408Z,E8C471022EE3436066517E1737A63A36,"十字链蛇骨链...",50.5,"","",""
```

### WhatsApp 通知

```
📉 1688 价格提醒

📦 商品：十字链蛇骨链麻花链盒子链
💰 当前价格：¥45.5
📊 原价：¥50.5
📈 变化：-9.9%
🔗 链接：https://detail.1688.com/offer/633830968371.html

价格下降 9.9%，已低于目标价！
```

---

## ⚙️ 配置说明

### config/monitored-products.json

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `products` | Array | 监控商品列表 | 必填 |
| `products[].id` | String | 商品唯一标识 | - |
| `products[].name` | String | 商品名称 | - |
| `products[].url` | String | 1688 商品链接 | 必填 |
| `products[].target_price` | Number | 目标采购价 | - |
| `products[].notify_threshold` | Number | 通知阈值（%） | 5 |
| `notifications.whatsapp.target` | String | WhatsApp 号码 | - |
| `settings.check_interval_hours` | Number | 检查间隔（小时） | 1 |
| `settings.quiet_hours` | Object | 安静时间配置 | 23:00-08:00 |

完整配置示例见 [CONFIG_EXAMPLE.md](./docs/CONFIG_EXAMPLE.md)。

---

## 🔧 故障排除

### WhatsApp 收不到消息

1. 检查连接状态：`openclaw channels list`
2. 重新登录：`openclaw channels login --channel whatsapp`
3. 测试发送：`node test-whatsapp.js +86你的号码`

### 价格为空

- 检查商品链接是否有效
- 确认页面是否需要登录
- 更新 `fetch-price.js` 中的选择器

### 定时任务不执行

- 检查 `HEARTBEAT.md` 配置
- 确认 OpenClaw 会话活跃
- 查看日志：`Get-Content data/alert-log.json`

更多问题见 [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)。

---

## 📈 监控面板

查看实时统计：

```bash
# 今日监控次数
Get-Content data/price-history.csv | Select-String (Get-Date -Format "yyyy-MM-dd") | Measure-Object

# 今日提醒次数
Get-Content data/alert-log.json | ConvertFrom-Json | Where-Object { $_.timestamp -gt [DateTimeOffset]::Now.Date.ToUnixTimeSeconds() * 1000 }
```

---

## 🔐 安全说明

- 不要提交 `config/monitored-products.json` 中的真实手机号到公开仓库
- 使用 `.env` 文件管理敏感信息
- 定期备份 `data/` 目录数据

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📞 联系方式

- **作者：** 汉堡 🍔
- **项目主页：** [GitHub](https://github.com/your-username/1688-price-monitor)
- **OpenClaw 文档：** https://docs.openclaw.ai/

---

## 📝 更新日志

### v1.0.0 (2026-04-01)

- ✅ 初始版本发布
- ✅ CDP 价格抓取
- ✅ WhatsApp 通知
- ✅ 定时任务支持
- ✅ 历史记录保存

---

**如果这个项目对你有帮助，请给个 ⭐ Star！**
