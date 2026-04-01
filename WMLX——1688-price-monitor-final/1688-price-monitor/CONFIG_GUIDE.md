# 1688 价格监控 - 完整配置指南

## 📋 第一步：配置 WhatsApp 接收号码

### 编辑配置文件

打开 `config/monitored-products.json`：

```json
{
  "notifications": {
    "whatsapp": {
      "enabled": true,
      "target": "+8613800138000"
    }
  }
}
```

**将 `target` 改为你的 WhatsApp 手机号码**（带国家码，如 +86 表示中国）

### 测试 WhatsApp 连接

```bash
openclaw message send --target +8613800138000 --message "🍔 1688 价格监控测试"
```

---

## 📦 第二步：添加监控商品

### 编辑商品列表

在 `config/monitored-products.json` 的 `products` 数组中添加：

```json
{
  "products": [
    {
      "id": "product-001",
      "name": "商品名称",
      "url": "https://detail.1688.com/offer/633830968371.html",
      "targetId": "",
      "target_price": 45.00,
      "currency": "CNY",
      "check_frequency": "hourly",
      "notify_threshold": 5
    },
    {
      "id": "product-002",
      "name": "第二个商品",
      "url": "https://detail.1688.com/offer/XXXXXXXXX.html",
      "target_price": 20.00,
      "notify_threshold": 10
    }
  ]
}
```

**字段说明：**
- `id`: 商品唯一标识（自定义）
- `name`: 商品名称（用于通知显示）
- `url`: 1688 商品详情页链接
- `target_price`: 目标采购价（低于此价格会发送提醒）
- `notify_threshold`: 价格变化通知阈值（百分比）
- `check_frequency`: 检查频率（hourly/daily/weekly）

---

## ⏰ 第三步：配置定时任务

### 方法 1：使用 HEARTBEAT（推荐）

编辑 `C:\Users\caizheyu\.openclaw\workspace-hamburger\HEARTBEAT.md`，添加：

```markdown
## 1688 价格监控

**执行频率：** 每小时整点

**执行命令：**
```bash
cd C:\Users\caizheyu\.openclaw\workspace-hamburger\skills\1688-price-monitor
node price-alert.js
```
```

### 方法 2：使用 Windows 任务计划程序

1. 打开 **任务计划程序**
2. 创建基本任务
3. 名称：`1688 价格监控`
4. 触发器：每天，重复间隔 1 小时
5. 操作：启动程序
   - 程序：`node.exe`
   - 参数：`price-alert.js`
   - 起始于：`C:\Users\caizheyu\.openclaw\workspace-hamburger\skills\1688-price-monitor`

### 方法 3：使用 cron 配置

`cron-config.json` 已配置好每小时执行：

```json
{
  "schedule": "0 * * * *",
  "command": "node price-alert.js"
}
```

使用 cron 工具加载：
```bash
# 如果使用 node-cron 或其他 cron 工具
```

---

## 🧪 第四步：测试运行

### 手动执行一次

```bash
cd C:\Users\caizheyu\.openclaw\workspace-hamburger\skills\1688-price-monitor
node price-alert.js
```

**预期输出：**
```
============================================================
🔍 开始 1688 价格监控
📦 监控商品数：1
============================================================

📦 检查：十字链蛇骨链麻花链盒子链多样项链女钛钢镀 18K 金素链锁骨链饰品
  🔍 抓取价格中...
  💰 当前价格：¥50.5
  ✅ 变化在阈值内

============================================================
📊 监控完成
📦 检查商品：1
⚠️ 价格变化：0
============================================================
```

### 测试价格提醒

修改 `price-alert.js` 临时降低阈值测试：

```javascript
const threshold = 1; // 改为 1% 触发测试
```

或者手动修改历史价格制造变化。

---

## 📊 第五步：查看监控数据

### 查看价格历史

```bash
Get-Content data/price-history.csv
```

**输出示例：**
```csv
timestamp,target_id,product_name,price,price_range,min_order,supplier
2026-04-01T07:49:20.408Z,E8C471022EE3436066517E1737A63A36,"商品名称",50.5,"","",""
```

### 查看提醒记录

```bash
Get-Content data/alert-log.json
```

**输出示例：**
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

## ⚙️ 高级配置

### 安静时间配置

在 `config/monitored-products.json` 中：

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

安静时间内只发送紧急通知（价格变化 > 20%）。

### 通知频率限制

```json
{
  "settings": {
    "max_alerts_per_hour": 5,
    "max_alerts_per_day": 20,
    "cooldown_minutes": 60
  }
}
```

### 自定义通知渠道

支持多渠道通知：

```json
{
  "notifications": {
    "whatsapp": {
      "enabled": true,
      "target": "+8613800138000"
    },
    "email": {
      "enabled": false,
      "address": "your@email.com"
    },
    "telegram": {
      "enabled": false,
      "chat_id": "your_chat_id"
    }
  }
}
```

---

## ❓ 常见问题

### Q1: WhatsApp 收不到消息？

**检查清单：**
1. 确认 WhatsApp 号码格式正确（+8613800138000）
2. 测试发送：`openclaw message send --target +8613800138000 --message "测试"`
3. 检查 OpenClaw WhatsApp 插件状态

### Q2: 价格为空？

**可能原因：**
- 1688 页面结构变化
- 需要登录才能看到价格
- 页面加载超时

**解决方法：**
1. 手动打开商品链接确认价格可见
2. 更新 `fetch-price.js` 中的选择器
3. 增加超时时间

### Q3: 定时任务不执行？

**检查：**
1. HEARTBEAT.md 配置是否正确
2. OpenClaw 会话是否活跃
3. 查看日志确认执行情况

---

## 📱 WhatsApp 通知示例

**价格下降：**
```
📉 1688 价格提醒

📦 商品：十字链蛇骨链麻花链盒子链
💰 当前价格：¥45.5
📊 原价：¥50.5
📈 变化：-9.9%
🔗 链接：https://detail.1688.com/offer/633830968371.html

价格下降 9.9%，已低于目标价！
```

**价格降至目标价：**
```
🎯 1688 价格提醒

📦 商品：XXX 产品
💰 当前价格：¥42.0
🎯 目标价：¥45.0

价格降至目标价以下，建议立即采购！
```

---

**配置完成后，告诉我你的 WhatsApp 号码，我帮你测试发送！** 🍔
