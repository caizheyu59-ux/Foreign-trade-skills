# 外贸客户激活系统 (Foreign Trade Customer Activation)

[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.2.26+-blue.svg)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/yourusername/foreign-trade-customer-activation)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> 自动识别超过5天未回复的外贸客户，生成专业跟进话术，提高客户转化率。

---

## 📖 功能概述

外贸客户激活系统是一个专为外贸从业者设计的 OpenClaw Skill，帮助您：

- 🎯 **自动识别** - 智能识别超过5天未回复的客户
- 📊 **每日统计** - 自动生成待激活客户报告
- 💬 **专业话术** - 根据未回复天数自动生成三级跟进话术
- ✅ **人工审核** - 所有消息发送前必须获得您的批准
- 📈 **提高转化** - 系统化跟进，减少客户流失

---

## 🚀 快速开始

### 安装要求

- OpenClaw >= 2026.2.26
- 已配置 WhatsApp 或 Feishu 消息通道
- Cron 任务支持

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/foreign-trade-customer-activation.git
cd foreign-trade-customer-activation
```

#### 2. 复制到 OpenClaw Skills 目录

**Windows:**
```powershell
copy /Y "SKILL.md" "%USERPROFILE%\.openclaw\workspace\skills\foreign-trade-customer-activation\"
copy /Y "_meta.json" "%USERPROFILE%\.openclaw\workspace\skills\foreign-trade-customer-activation\"
```

**macOS/Linux:**
```bash
mkdir -p ~/.openclaw/workspace/skills/foreign-trade-customer-activation
cp SKILL.md _meta.json ~/.openclaw/workspace/skills/foreign-trade-customer-activation/
```

#### 3. 创建客户列表文件

在工作区创建 `foreign-trade-customers.md`：

```markdown
- John Smith - ABC Trading Co. - USA
  - 询盘产品: LED Display Screens
  - 最后回复时间: 2026-03-15
  - 联系方式: WhatsApp
  - 联系ID: +1 555 123 4567
  - 未回复天数: 5
  - 跟进次数: 0
  - 状态: 待激活
  - 备注: 询盘100台LED屏幕，等待报价反馈
```

#### 4. 配置 Cron 任务

```bash
openclaw cron add \
  --name "foreign-trade-customer-activation" \
  --description "外贸客户激活：每天识别超过5天未回复的客户" \
  --cron "0 9 * * 1-5" \
  --message "请执行外贸客户激活任务..." \
  --session isolated \
  --announce \
  --channel whatsapp \
  --to "你的手机号"
```

---

## 📋 使用指南

### 每日自动运行流程

```
上午 9:00  → 系统自动检查客户列表
          → 识别超过5天未回复的客户
          → 生成专业跟进话术
          → 发送报告给您审核
          → 等待您的批准
          → 批准后自动发送
```

### 客户列表格式

```markdown
- [客户姓名] - [公司名称] - [国家]
  - 询盘产品: [产品名称]
  - 最后回复时间: [YYYY-MM-DD]
  - 联系方式: [WhatsApp/Email/Feishu]
  - 联系ID: [号码/邮箱]
  - 未回复天数: [天数]
  - 跟进次数: [次数]
  - 状态: [活跃/待激活/已关闭]
  - 备注: [重要信息]
```

---

## 💬 三级跟进话术

### 🔵 跟进话术（5-9天未回复）

```
Hi [Name],

Hope this email finds you well. I wanted to follow up on my previous 
message regarding [产品].

I understand you might be busy. Just wanted to check if you had a 
chance to review my proposal?

Looking forward to your feedback.

Best regards,
[Your Name]
```

### 🟡 催促话术（10-14天未回复）

```
Hi [Name],

I hope you're doing well. I haven't heard back from you regarding [产品].

Just wondering if you're still interested? If not, no worries at all.

Please let me know either way.

Best regards,
[Your Name]
```

### 🔴 最后机会话术（15天以上未回复）

```
Hi [Name],

This will be my last follow-up regarding [产品].

If you're no longer interested, I completely understand and will close 
this inquiry.

If you are still interested but just busy, please let me know and I'll 
be happy to assist.

Best regards,
[Your Name]
```

---

## ⚙️ 配置说明

### 修改跟进规则

编辑 `HEARTBEAT.md` 文件：

```markdown
## 限制规则

- 每天最多发送5条激活消息    # 修改此数字调整每日上限
- 同一客户最多跟进3次         # 修改此数字调整跟进次数
- 超过15天未回复自动关闭      # 修改此天数调整关闭阈值
- 只在工作日运行（周一到周五）
```

### 自定义话术模板

编辑 `SKILL.md` 文件中的话术部分，修改为您自己的风格。

---

## 📊 系统限制

| 限制项 | 默认值 | 说明 |
|--------|--------|------|
| 每日发送上限 | 5条 | 防止过度打扰客户 |
| 单客户跟进次数 | 3次 | 避免重复骚扰 |
| 自动关闭天数 | 15天 | 超过此天数自动标记为已关闭 |
| 运行时间 | 工作日 9:00 AM | 周末不运行 |
| 消息审核 | 必须批准 | 所有消息发送前需人工确认 |

---

## 🗂️ 文件结构

```
foreign-trade-customer-activation/
├── README.md              # 本文件
├── SKILL.md               # Skill 主文件
├── _meta.json             # Skill 元数据
├── LICENSE                # MIT 许可证
├── foreign-trade-customers.md    # 客户列表示例
└── HEARTBEAT.md           # 配置说明
```

---

## 🔧 故障排除

### 常见问题

**Q: Skill 未显示在技能列表中**

```bash
# 检查 skill 位置
ls ~/.openclaw/workspace/skills/foreign-trade-customer-activation

# 重新扫描技能
openclaw skills check
```

**Q: Cron 任务未运行**

```bash
# 检查 Cron 任务状态
openclaw cron list

# 手动运行测试
openclaw cron run [任务ID]
```

**Q: 消息发送失败**

```bash
# 检查 WhatsApp 连接
openclaw channels status

# 重新连接 WhatsApp
openclaw channels login --channel whatsapp
```

---

## 📝 更新日志

### v1.0.0 (2026-03-20)

- ✅ 初始版本发布
- ✅ 支持客户状态监控
- ✅ 支持三级话术模板
- ✅ 支持每日自动运行
- ✅ 支持人工审核机制

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - 强大的 AI 自动化平台
- 所有贡献者和用户

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: [提交问题](https://github.com/yourusername/foreign-trade-customer-activation/issues)
- Email: your.email@example.com

---

**Made with ❤️ by Hamburger** 🍔
