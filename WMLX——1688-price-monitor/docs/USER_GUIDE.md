# 1688 价格监控系统 - 用户操作指南

本文档详细介绍如何使用 1688 价格监控系统。

---

## 📋 目录

1. [快速开始](#快速开始)
2. [配置监控商品](#配置监控商品)
3. [配置通知渠道](#配置通知渠道)
4. [运行监控](#运行监控)
5. [查看数据](#查看数据)
6. [常见问题](#常见问题)

---

## 🚀 快速开始

### 5 分钟配置流程

```bash
# 1. 进入项目目录
cd skills/1688-price-monitor

# 2. 安装依赖
npm install

# 3. 配置 WhatsApp 号码
# 编辑 config/monitored-products.json，修改 target 为你的号码

# 4. 连接 WhatsApp
openclaw channels login --channel whatsapp --account default

# 5. 测试运行
node price-alert.js
```

完成！系统会立即检查商品价格并发送通知。

---

## ⚙️ 配置监控商品

### 编辑配置文件

打开 `config/monitored-products.json`：

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

### 字段说明

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `id` | ✅ | 商品唯一标识 | `product-001` |
| `name` | ✅ | 商品名称（用于通知显示） | `十字链...` |
| `url` | ✅ | 1688 商品详情页链接 | `https://...` |
| `target_price` | ❌ | 目标采购价 | `45.00` |
| `notify_threshold` | ❌ | 价格变化通知阈值（%） | `5` |

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

## 📱 配置通知渠道

### WhatsApp（推荐）

#### 1. 连接 WhatsApp

```bash
openclaw channels login --channel whatsapp --account default
```

扫描二维码完成连接。

#### 2. 配置接收号码

编辑 `config/monitored-products.json`：

```json
{
  "notifications": {
    "whatsapp": {
      "enabled": true,
      "target": "+86XXXXXXXXXXX"
    }
  }
}
```

**将 `target` 改为你的 WhatsApp 号码**（带国家码）。

#### 3. 测试发送

```bash
openclaw message send --target "+86XXXXXXXXXXX" --message "测试消息"
```

---

### 飞书

#### 1. 创建飞书机器人

1. 打开飞书 → 创建群聊
2. 群设置 → 机器人 → 添加机器人
3. 选择 **自定义机器人**
4. 复制 Webhook URL

#### 2. 配置 Webhook

编辑 `config/monitored-products.json`：

```json
{
  "notifications": {
    "feishu": {
      "enabled": true,
      "type": "webhook",
      "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  }
}
```

#### 3. 测试发送

```bash
curl -X POST "你的 Webhook URL" \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"测试消息"}}'
```

---

## ▶️ 运行监控

### 手动执行

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

### 自动执行（定时任务）

编辑 OpenClaw 工作区根目录的 `HEARTBEAT.md`：

```markdown
## 1688 价格监控

**执行频率：** 每小时整点

**执行命令：**
```bash
cd skills/1688-price-monitor
node price-alert.js
```
```

OpenClaw 会自动每小时执行一次。

---

## 📊 查看数据

### 价格历史

```bash
# PowerShell
Get-Content data/price-history.csv

# 或使用 Excel 打开
start data/price-history.csv
```

**CSV 格式：**
```csv
timestamp,target_id,product_name,price,price_range,min_order,supplier
2026-04-01T07:49:20.408Z,...,"十字链...",50.5,"","",""
```

### 提醒记录

```bash
Get-Content data/alert-log.json | ConvertFrom-Json
```

**JSON 格式：**
```json
[
  {
    "productId": "product-001",
    "productName": "十字链...",
    "timestamp": 1712073600000,
    "oldPrice": 50.5,
    "newPrice": 45.0,
    "changePercent": -10.89
  }
]
```

### 统计信息

```bash
# 今日监控次数
Get-Content data/price-history.csv | Select-String (Get-Date -Format "yyyy-MM-dd") | Measure-Object

# 平均价格
Get-Content data/price-history.csv | ConvertFrom-Csv | Measure-Object -Property price -Average
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

## 📱 通知示例

### WhatsApp 消息

```
📉 1688 价格提醒

📦 商品：十字链蛇骨链麻花链盒子链
💰 当前价格：¥45.5
📊 原价：¥50.5
📈 变化：-9.9%
🔗 链接：https://detail.1688.com/offer/633830968371.html

价格下降 9.9%，已低于目标价！
```

### 飞书消息

```
📉 1688 价格提醒

📦 商品：十字链蛇骨链麻花链盒子链
💰 当前价格：¥45.5
📊 原价：¥50.5
📈 变化：-9.9%

价格下降 9.9%，已低于目标价！
```

---

## ❓ 常见问题

### Q1: WhatsApp 收不到消息？

**检查清单：**
1. ✅ 号码格式正确（`+86XXXXXXXXXXX`）
2. ✅ WhatsApp 已连接：`openclaw channels list`
3. ✅ 测试发送：`openclaw message send --target "+86..." --message "测试"`

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
3. 查看日志：`Get-Content data/alert-log.json`

### Q4: 如何修改检查频率？

编辑 `config/monitored-products.json`：

```json
{
  "settings": {
    "check_interval_hours": 2  // 改为 2 小时
  }
}
```

### Q5: 如何关闭安静时间？

编辑 `config/monitored-products.json`：

```json
{
  "settings": {
    "quiet_hours": null  // 禁用安静时间
  }
}
```

---

## 🛠️ 高级用法

### 导出数据

```bash
# 导出为 Excel
Get-Content data/price-history.csv | ConvertFrom-Csv | Export-Excel price-report.xlsx

# 导出为 JSON
Get-Content data/price-history.csv | ConvertFrom-Csv | ConvertTo-Json | Out-File price-history.json
```

### 价格趋势分析

创建 `analyze.js`：

```javascript
const fs = require('fs');
const csv = require('csv-parser');

const prices = [];

fs.createReadStream('data/price-history.csv')
    .pipe(csv())
    .on('data', (row) => {
        prices.push({
            date: row.timestamp,
            price: parseFloat(row.price)
        });
    })
    .on('end', () => {
        const avg = prices.reduce((sum, p) => sum + p.price, 0) / prices.length;
        const min = Math.min(...prices.map(p => p.price));
        const max = Math.max(...prices.map(p => p.price));
        
        console.log('价格统计:');
        console.log('平均价格:', avg.toFixed(2));
        console.log('最低价格:', min.toFixed(2));
        console.log('最高价格:', max.toFixed(2));
    });
```

运行：

```bash
node analyze.js
```

---

## 📚 相关文档

- [WhatsApp 配置指南](./WHATSAPP_SETUP.md)
- [飞书配置指南](./FEISHU_SETUP.md)
- [部署指南](./DEPLOYMENT.md)
- [故障排除](./TROUBLESHOOTING.md)

---

**版本：** 1.0.0  
**最后更新：** 2026-04-01
