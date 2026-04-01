# 1688 价格监控系统 - 完整使用指南

## 🎯 功能概述

自动监控 1688 商品价格变化，实时推送 WhatsApp 通知。

**核心功能：**
- ✅ 自动抓取 1688 商品价格
- ✅ 检测价格变化（可配置阈值）
- ✅ WhatsApp 实时推送提醒
- ✅ 定时任务自动执行
- ✅ 价格历史记录保存
- ✅ 目标价格监控

---

## 📁 文件结构

```
1688-price-monitor/
├── SKILL.md                      # 技能定义
├── monitor.py                    # Python 监控脚本
├── fetch-price.js                # CDP 价格抓取脚本 ✅
├── price-alert.js                # 价格提醒主脚本 ✅
├── test-whatsapp.js              # WhatsApp 测试脚本 ✅
├── README.md                     # 简要说明
├── README_COMPLETE.md            # 完整指南（本文件）
├── QUICKSTART.md                 # 快速开始
├── CONFIG_GUIDE.md               # 配置指南
├── WHATSAPP_SETUP.md             # WhatsApp 配置
├── USAGE.md                      # 使用说明
├── package.json                  # Node.js 配置
├── requirements.txt              # Python 依赖
├── cron-config.json              # 定时任务配置
├── .gitignore                    # Git 忽略
├── config/
│   └── monitored-products.json   # 监控商品配置 ✅
└── data/
    ├── price-history.csv         # 价格历史记录 ✅
    └── alert-log.json            # 提醒发送记录 ✅
```

---

## 🚀 快速开始（5 分钟配置）

### 步骤 1：安装依赖

```bash
cd 你的 OpenClaw 工作区\skills\1688-price-monitor
npm install ws
```

### 步骤 2：配置 WhatsApp 号码

编辑 `config/monitored-products.json`，找到：

```json
"notifications": {
  "whatsapp": {
    "enabled": true,
    "target": "+8613800138000"
  }
}
```

**将 `target` 改为你的 WhatsApp 手机号码**（如 `+8613800138000`）

### 步骤 3：测试 WhatsApp

```bash
node test-whatsapp.js +8613800138000
```

替换为你的实际号码。如果收到测试消息，说明配置成功！

### 步骤 4：添加监控商品

编辑 `config/monitored-products.json` 的 `products` 数组：

```json
{
  "products": [
    {
      "id": "product-001",
      "name": "十字链蛇骨链麻花链盒子链",
      "url": "https://detail.1688.com/offer/633830968371.html",
      "target_price": 45.00,
      "notify_threshold": 5
    }
  ]
}
```

### 步骤 5：手动测试监控

```bash
node price-alert.js
```

**预期输出：**
```
============================================================
🔍 开始 1688 价格监控
📦 监控商品数：1
============================================================

📦 检查：十字链蛇骨链麻花链盒子链
  🔍 抓取价格中...
  💰 当前价格：¥50.5
  ✅ 变化在阈值内

============================================================
📊 监控完成
============================================================
```

---

## ⏰ 配置定时任务

### 方法 1：HEARTBEAT（推荐）

OpenClaw 会自动读取 `HEARTBEAT.md` 并定时执行。

**已配置：** 每小时整点执行

如需修改频率，编辑 `HEARTBEAT.md`。

### 方法 2：Windows 任务计划程序

1. 打开 **任务计划程序**
2. 创建基本任务 → 名称：`1688 价格监控`
3. 触发器：每天，重复间隔 **1 小时**
4. 操作：启动程序
   - 程序：`node.exe`
   - 参数：`price-alert.js`
   - 起始于：`你的 OpenClaw 工作区\skills\1688-price-monitor`

---

## 📊 查看监控数据

### 价格历史

```bash
Get-Content data/price-history.csv
```

**格式：**
```csv
timestamp,target_id,product_name,price,price_range,min_order,supplier
2026-04-01T07:49:20.408Z,...,"商品名称",50.5,...
```

### 提醒记录

```bash
Get-Content data/alert-log.json | ConvertFrom-Json
```

**格式：**
```json
[
  {
    "productId": "product-001",
    "productName": "商品名称",
    "timestamp": 1712073600000,
    "oldPrice": 50.5,
    "newPrice": 45.0,
    "changePercent": -10.89
  }
]
```

---

## 🔔 通知规则

### 触发条件

| 情况 | 阈值 | 通知 |
|------|------|------|
| 价格下降 | ≥ 5% | ✅ 发送 |
| 价格上涨 | ≥ 5% | ✅ 发送 |
| 降至目标价 | 任何幅度 | ✅ 发送 |
| 正常波动 | < 5% | ❌ 不发送 |

### 频率限制

- 同一商品 **1 小时内** 不重复发送
- 每天最多 **20 条** 通知
- 安静时间 **23:00-08:00** 不发送（紧急情况除外）

---

## 📱 WhatsApp 通知示例

### 价格下降

```
📉 1688 价格提醒

📦 商品：十字链蛇骨链麻花链盒子链
💰 当前价格：¥45.5
📊 原价：¥50.5
📈 变化：-9.9%
🔗 链接：https://detail.1688.com/offer/633830968371.html

价格下降 9.9%，已低于目标价！
```

### 价格降至目标价

```
🎯 1688 价格提醒

📦 商品：XXX 产品
💰 当前价格：¥42.0
🎯 目标价：¥45.0
🔗 链接：https://...

价格降至目标价以下，建议立即采购！
```

### 价格上涨

```
📈 1688 价格提醒

📦 商品：XXX 产品
💰 当前价格：¥120.0
📊 原价：¥100.0
📈 变化：+20.0%
🔗 链接：https://...

价格上涨 20.0%，超过阈值！
```

---

## ⚙️ 高级配置

### 修改价格阈值

编辑 `config/monitored-products.json`：

```json
{
  "products": [
    {
      "id": "product-001",
      "notify_threshold": 10  // 改为 10%
    }
  ],
  "settings": {
    "notify_threshold": 5  // 全局默认阈值
  }
}
```

### 配置安静时间

```json
{
  "settings": {
    "quiet_hours": {
      "start": "23:00",
      "end": "08:00"
    }
  }
}
```

### 修改检查频率

```json
{
  "settings": {
    "check_interval_hours": 2  // 每 2 小时检查一次
  }
}
```

### 添加多个商品

```json
{
  "products": [
    {
      "id": "product-001",
      "name": "商品 A",
      "url": "https://detail.1688.com/offer/XXX.html",
      "target_price": 45.00,
      "notify_threshold": 5
    },
    {
      "id": "product-002",
      "name": "商品 B",
      "url": "https://detail.1688.com/offer/YYY.html",
      "target_price": 20.00,
      "notify_threshold": 10
    }
  ]
}
```

---

## ❓ 故障排除

### 问题 1：WhatsApp 收不到消息

**检查清单：**
1. ✅ 号码格式正确（`+8613800138000`）
2. ✅ 测试发送：`node test-whatsapp.js +8613800138000`
3. ✅ OpenClaw WhatsApp 已连接：`openclaw message status`

### 问题 2：价格为空

**可能原因：**
- 1688 页面结构变化
- 需要登录才能看到价格
- 页面加载超时

**解决方法：**
1. 手动打开商品链接确认价格可见
2. 更新 `fetch-price.js` 中的选择器
3. 增加 WebSocket 超时时间

### 问题 3：定时任务不执行

**检查：**
1. HEARTBEAT.md 配置是否正确
2. OpenClaw 会话是否活跃
3. 查看日志：`Get-Content data/alert-log.json`

### 问题 4：npm 安装失败

**错误：** `Cannot find module 'ws'`

**解决：**
```bash
cd skills/1688-price-monitor
npm install ws
```

---

## 📈 监控面板（可选）

查看实时统计：

```bash
# 今日监控次数
Get-Content data/price-history.csv | Select-String "2026-04-01" | Measure-Object | Select-Object Count

# 今日提醒次数
Get-Content data/alert-log.json | ConvertFrom-Json | Where-Object { $_.timestamp -gt (Get-Date).Date } | Measure-Object | Select-Object Count

# 平均价格
Get-Content data/price-history.csv | ConvertFrom-Csv | Measure-Object -Property price -Average | Select-Object Average
```

---

## 🎯 最佳实践

1. **合理设置阈值** - 建议 5-10%，避免频繁通知
2. **定期检查配置** - 确保商品链接有效
3. **监控日志** - 每周检查 alert-log.json
4. **备份数据** - 定期导出 price-history.csv
5. **测试通知** - 每月测试一次 WhatsApp 连接

---

## 📞 技术支持

- **技能位置：** `你的 OpenClaw 工作区\skills\1688-price-monitor`
- **GitHub：** （待上传）
- **版本：** 1.0.0
- **最后更新：** 2026-04-01

---

**配置完成后，运行 `node price-alert.js` 开始监控！** 🍔
