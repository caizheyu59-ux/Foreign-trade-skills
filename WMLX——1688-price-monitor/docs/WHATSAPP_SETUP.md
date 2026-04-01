# WhatsApp 配置指南

本文档介绍如何配置 WhatsApp 通知功能。

---

## 📱 方法一：OpenClaw 内置渠道（推荐）

### 1. 检查渠道状态

```bash
openclaw channels list
```

**预期输出：**
```
Chat channels:
- WhatsApp default: not linked, enabled
```

### 2. 登录 WhatsApp

```bash
openclaw channels login --channel whatsapp --account default
```

### 3. 扫描二维码

终端会显示二维码，使用手机 WhatsApp 扫描：

1. 打开 WhatsApp
2. 进入 **设置** → **已连接的设备**
3. 点击 **连接设备**
4. 扫描二维码

### 4. 验证连接

```bash
openclaw channels list
```

**成功输出：**
```
Chat channels:
- WhatsApp default: linked, enabled  ✅
```

### 5. 测试发送

```bash
openclaw message send --target "+86XXXXXXXXXXX" --message "🍔 1688 价格监控测试"
```

---

## 🔧 配置监控商品

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

**将 `target` 改为你的 WhatsApp 号码**（带国家码，如 +86 表示中国）。

---

## 📱 方法二：WhatsApp Business API

适用于企业用户，支持模板消息和批量发送。

### 1. 申请 API

访问：https://business.whatsapp.com/products/business-platform

### 2. 安装依赖

```bash
npm install axios
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
WHATSAPP_API_KEY=your_api_key
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_RECIPIENT=+86XXXXXXXXXXX
```

### 4. 更新发送脚本

修改 `price-alert.js` 中的 `sendWhatsApp` 方法：

```javascript
const axios = require('axios');

async sendWhatsApp(message) {
    const response = await axios.post(
        `https://graph.facebook.com/v17.0/${process.env.WHATSAPP_PHONE_ID}/messages`,
        {
            messaging_product: 'whatsapp',
            to: process.env.WHATSAPP_RECIPIENT,
            type: 'text',
            text: { body: message }
        },
        {
            headers: {
                'Authorization': `Bearer ${process.env.WHATSAPP_API_KEY}`,
                'Content-Type': 'application/json'
            }
        }
    );
    
    return response.data;
}
```

---

## 📱 方法三：Twilio WhatsApp API

### 1. 注册 Twilio

访问：https://www.twilio.com/whatsapp

### 2. 安装 SDK

```bash
npm install twilio
```

### 3. 配置凭证

```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
RECIPIENT_NUMBER=whatsapp:+86XXXXXXXXXXX
```

### 4. 更新发送脚本

```javascript
const twilio = require('twilio');

async sendWhatsApp(message) {
    const client = twilio(
        process.env.TWILIO_ACCOUNT_SID,
        process.env.TWILIO_AUTH_TOKEN
    );
    
    await client.messages.create({
        from: process.env.TWILIO_WHATSAPP_NUMBER,
        to: process.env.RECIPIENT_NUMBER,
        body: message
    });
    
    return true;
}
```

---

## 📋 通知模板

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

### 安静时间

在 `config/monitored-products.json` 中配置：

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

---

## ❓ 故障排除

### 问题 1：WhatsApp 未连接

**错误：** `WhatsApp account not connected`

**解决：**
1. 运行 `openclaw channels list` 检查状态
2. 重新登录：`openclaw channels login --channel whatsapp`
3. 确保扫描二维码成功

### 问题 2：消息发送失败

**错误：** `Failed to send message`

**解决：**
1. 检查网络连接
2. 验证 WhatsApp 账户状态
3. 确认接收人号码格式正确（带国家码）

### 问题 3：重复发送

**问题：** 同一价格变化多次发送

**解决：**
- 检查 `data/alert-log.json` 中的冷却时间
- 确保 `cooldown_minutes` 设置合理（建议 60 分钟）

---

## 🧪 测试命令

```bash
# 测试 WhatsApp 连接
openclaw channels list

# 测试发送
openclaw message send --target "+86XXXXXXXXXXX" --message "测试消息"

# 使用测试脚本
node test-whatsapp.js +86XXXXXXXXXXX
```

---

**版本：** 1.0.0  
**最后更新：** 2026-04-01
