# 飞书配置指南

本文档介绍如何配置飞书通知功能。

---

## 📱 方法一：OpenClaw 内置渠道

### 1. 检查渠道状态

```bash
openclaw channels list
```

### 2. 登录飞书

```bash
openclaw channels login --channel feishu --account default
```

### 3. 授权连接

按提示完成飞书授权。

### 4. 验证连接

```bash
openclaw channels list
```

**成功输出：**
```
Chat channels:
- Feishu default: linked, enabled  ✅
```

### 5. 测试发送

```bash
openclaw message send --channel feishu --target "你的飞书用户 ID" --message "🍔 1688 价格监控测试"
```

---

## 🤖 方法二：飞书机器人 Webhook（推荐）

适用于群聊通知，无需授权。

### 1. 创建飞书群

1. 打开飞书
2. 创建群聊（或选择现有群）
3. 进入群设置

### 2. 添加自定义机器人

1. 群设置 → **机器人** → **添加机器人**
2. 选择 **自定义机器人**
3. 点击 **添加**

### 3. 配置机器人

- **名称：** 1688 价格监控
- **头像：** （可选）
- **安全设置：** 选择 **自定义关键词**
- **关键词：** 添加 `价格提醒`、`1688` 等

### 4. 获取 Webhook URL

复制 Webhook 地址，格式：
```
https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 5. 配置到项目

创建 `.env` 文件：

```bash
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

或在 `config/monitored-products.json` 中配置：

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

### 6. 更新发送脚本

添加飞书发送方法：

```javascript
const axios = require('axios');

async sendFeishu(message) {
    const webhookUrl = process.env.FEISHU_WEBHOOK_URL;
    
    const response = await axios.post(webhookUrl, {
        msg_type: 'text',
        content: {
            text: message
        }
    });
    
    return response.data;
}
```

---

## 📊 飞书消息格式

### 文本消息

```json
{
    "msg_type": "text",
    "content": {
        "text": "📉 1688 价格提醒\n\n商品：十字链\n价格：¥45.5\n变化：-9.9%"
    }
}
```

### 富文本消息（推荐）

```json
{
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "1688 价格提醒",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": "📦 商品："
                        },
                        {
                            "tag": "text",
                            "text": "十字链蛇骨链麻花链盒子链"
                        }
                    ],
                    [
                        {
                            "tag": "text",
                            "text": "💰 当前价格："
                        },
                        {
                            "tag": "text",
                            "text": "¥45.5"
                        }
                    ],
                    [
                        {
                            "tag": "text",
                            "text": "📈 变化："
                        },
                        {
                            "tag": "text",
                            "text": "-9.9%"
                        }
                    ]
                ]
            }
        }
    }
}
```

### 卡片消息（最美观）

```json
{
    "msg_type": "interactive",
    "card": {
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "📉 1688 价格提醒"
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**商品：** 十字链蛇骨链麻花链盒子链\n**当前价格：** ¥45.5\n**原价：** ¥50.5\n**变化：** -9.9%"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "查看详情"
                        },
                        "url": "https://detail.1688.com/offer/633830968371.html",
                        "type": "default"
                    }
                ]
            }
        ]
    }
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

---

## ⚙️ 配置示例

### config/monitored-products.json

```json
{
  "notifications": {
    "whatsapp": {
      "enabled": false,
      "target": "+86XXXXXXXXXXX"
    },
    "feishu": {
      "enabled": true,
      "type": "webhook",
      "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "msg_type": "interactive"
    }
  }
}
```

---

## 🧪 测试命令

### 测试 Webhook

```bash
curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "🍔 1688 价格监控测试"
    }
  }'
```

### 使用测试脚本

创建 `test-feishu.js`：

```javascript
const axios = require('axios');

async function testFeishu() {
    const webhookUrl = process.env.FEISHU_WEBHOOK_URL;
    
    const response = await axios.post(webhookUrl, {
        msg_type: 'text',
        content: {
            text: '🍔 1688 价格监控测试\n\n如果你收到这条消息，说明飞书通知已配置成功！'
        }
    });
    
    console.log('✅ 飞书消息已发送');
    console.log('响应:', response.data);
}

testFeishu();
```

运行：

```bash
node test-feishu.js
```

---

## ❓ 故障排除

### 问题 1：Webhook 发送失败

**错误：** `400 Bad Request`

**解决：**
1. 检查 Webhook URL 是否正确
2. 确认 JSON 格式正确
3. 验证安全设置中的关键词

### 问题 2：消息被拦截

**原因：** 未包含安全关键词

**解决：**
- 在消息中包含配置的关键词（如 `价格提醒`）
- 或修改机器人安全设置为 IP 白名单

### 问题 3：飞书渠道未连接

**解决：**
1. 运行 `openclaw channels list` 检查状态
2. 重新登录：`openclaw channels login --channel feishu`
3. 完成授权流程

---

## 📊 高级功能

### @提及用户

在卡片消息中添加 `@` 功能：

```json
{
    "msg_type": "interactive",
    "card": {
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "价格变化提醒，请查看 <at user_id=\"xxxxxx\"></at>"
                }
            }
        ]
    }
}
```

### 定时发送

结合定时任务，在指定时间发送日报：

```javascript
// 每天 9:00 发送价格日报
async function sendDailyReport() {
    const report = generateDailyReport();
    await sendFeishu(report);
}
```

---

## 📚 参考文档

- [飞书开放平台](https://open.feishu.cn/document/home)
- [自定义机器人](https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN)
- [消息卡片](https://open.feishu.cn/document/ukTMukTMukTM/uUjNz4SN24jL1ITM)

---

**版本：** 1.0.0  
**最后更新：** 2026-04-01
