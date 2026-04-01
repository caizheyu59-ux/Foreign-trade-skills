# WhatsApp 通知配置指南

## 📱 配置 WhatsApp 通知

### 方法 1：使用 OpenClaw Message 工具（推荐）

OpenClaw 已集成 WhatsApp 支持，直接配置即可使用。

#### 1. 检查 WhatsApp 连接状态

```bash
openclaw message status
```

#### 2. 配置 WhatsApp 目标

编辑 `config/monitored-products.json`：

```json
{
  "notifications": {
    "whatsapp": {
      "enabled": true,
      "target": "whatsapp"
    }
  }
}
```

#### 3. 测试发送

```bash
openclaw message send --target whatsapp --message "🍔 1688 价格监控测试消息"
```

---

### 方法 2：使用 WhatsApp Business API

如果需要更高级的功能（如模板消息、批量发送）：

#### 1. 申请 WhatsApp Business API

访问：https://business.whatsapp.com/products/business-platform

#### 2. 配置 API 凭证

创建 `.env` 文件：

```bash
WHATSAPP_API_KEY=your_api_key
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_RECIPIENT=+8613800138000
```

#### 3. 更新发送脚本

修改 `price-alert.js` 中的 `sendWhatsApp` 方法：

```javascript
async sendWhatsApp(message) {
    const axios = require('axios');
    
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

### 方法 3：使用 Twilio WhatsApp API

#### 1. 注册 Twilio

访问：https://www.twilio.com/whatsapp

#### 2. 安装 Twilio SDK

```bash
npm install twilio
```

#### 3. 配置凭证

```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
RECIPIENT_NUMBER=whatsapp:+8613800138000
```

#### 4. 更新发送脚本

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

## 🔔 通知模板

### 价格下降提醒

```
📉 1688 价格提醒

📦 商品：十字链蛇骨链麻花链盒子链
💰 当前价格：¥45.5
📊 原价：¥50.5
📈 变化：-9.9%
🔗 链接：https://detail.1688.com/offer/633830968371.html

价格下降 9.9%，已低于目标价！
```

### 价格上涨提醒

```
📈 1688 价格提醒

📦 商品：XXX 产品
💰 当前价格：¥120.0
📊 原价：¥100.0
📈 变化：+20.0%
🔗 链接：https://...

价格上涨 20.0%，超过阈值！
```

### 目标价提醒

```
🎯 1688 价格提醒

📦 商品：XXX 产品
💰 当前价格：¥42.0
🎯 目标价：¥45.0
🔗 链接：https://...

价格降至目标价以下，建议立即采购！
```

---

## ⚙️ 通知设置

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

## 🧪 测试

### 测试发送

```bash
cd skills/1688-price-monitor
node -e "
const PriceAlert = require('./price-alert');
const alert = new PriceAlert();
alert.sendWhatsApp('🍔 测试消息：1688 价格监控已就绪');
"
```

### 预期输出

```
✅ WhatsApp 消息已发送
```

---

## 📊 查看发送记录

```bash
# 查看提醒日志
Get-Content data/alert-log.json | ConvertFrom-Json

# 查看价格历史
Get-Content data/price-history.csv
```

---

## ❓ 故障排除

### 问题 1：WhatsApp 未连接

**错误：** `WhatsApp account not connected`

**解决：**
1. 运行 `openclaw message status` 检查状态
2. 按照提示连接 WhatsApp 账户
3. 扫描二维码完成配对

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

**版本:** 1.0.0  
**最后更新:** 2026-04-01
