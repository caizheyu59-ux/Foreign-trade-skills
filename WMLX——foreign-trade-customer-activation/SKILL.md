---
name: foreign-trade-customer-activation
description: 外贸客户激活系统 - 自动识别超过5天未回复的外贸客户，生成专业跟进话术，提高客户转化率。支持每日统计、多轮跟进、自动关闭等功能。
version: 1.0.0
author: Hamburger
source: openclaw-workspace
tags:
  - 外贸
  - 客户管理
  - CRM
  - 跟进
  - 销售
allowed-tools:
  - message
  - read
  - write
  - edit
  - exec
---

# 外贸客户激活系统

## 功能概述

自动识别超过5天未回复的外贸客户，每日统计并发送专业跟进消息，提高客户转化率。

## 核心功能

### 1. 客户状态监控
- 跟踪所有外贸客户的最后回复时间
- 自动识别超过5天未回复的客户
- 按优先级排序（最久未回复优先）

### 2. 每日统计报告
- 生成待激活客户列表
- 显示客户信息和未回复天数
- 发送给用户审核

### 3. 专业外贸话术
根据未回复天数自动选择话术类型：

**跟进话术（5-9天）：**
```
Hi [Name],

Hope this email finds you well. I wanted to follow up on my previous message regarding [产品].

I understand you might be busy. Just wanted to check if you had a chance to review my proposal?

Looking forward to your feedback.

Best regards,
[Your Name]
```

**催促话术（10-14天）：**
```
Hi [Name],

I hope you're doing well. I haven't heard back from you regarding [产品].

Just wondering if you're still interested? If not, no worries at all.

Please let me know either way.

Best regards,
[Your Name]
```

**最后机会话术（15天以上）：**
```
Hi [Name],

This will be my last follow-up regarding [产品].

If you're no longer interested, I completely understand and will close this inquiry.

If you are still interested but just busy, please let me know and I'll be happy to assist.

Best regards,
[Your Name]
```

## 安装步骤

### 1. 创建客户列表文件

在工作区创建 `foreign-trade-customers.md`：

```markdown
- [客户姓名] - [公司名称] - [国家]
  - 询盘产品: [产品名称]
  - 最后回复时间: [日期]
  - 联系方式: [WhatsApp/Email/Feishu]
  - 联系ID: [号码/邮箱]
  - 未回复天数: [天数]
  - 跟进次数: [次数]
  - 状态: [活跃/待激活/已关闭]
  - 备注: [重要信息]
```

### 2. 配置 Cron 任务

```bash
openclaw cron add \
  --name "foreign-trade-customer-activation" \
  --description "外贸客户激活：每天识别超过5天未回复的客户" \
  --cron "0 9 * * 1-5" \
  --message "请执行外贸客户激活任务..." \
  --session isolated \
  --announce \
  --channel whatsapp \
  --to [你的号码]
```

### 3. 配置说明

编辑 `HEARTBEAT.md` 自定义规则：
- 修改未回复天数阈值（默认5天）
- 调整每日发送上限（默认5个）
- 修改跟进次数限制（默认3次）
- 自定义话术模板

## 使用流程

### 每日自动运行

1. **上午9点** - 系统自动检查客户列表
2. **识别待激活客户** - 超过5天未回复的客户
3. **生成跟进话术** - 根据天数选择对应话术
4. **发送报告** - 通过 WhatsApp 发送给你审核
5. **等待批准** - 你选择要发送的客户
6. **自动发送** - 批准后发送专业话术

### 手动运行

```bash
# 立即运行客户激活检查
openclaw cron run [任务ID]

# 查看客户列表
cat foreign-trade-customers.md

# 更新客户信息
edit foreign-trade-customers.md
```

## 文件结构

```
workspace/
├── foreign-trade-customers.md     # 客户列表
├── HEARTBEAT.md                    # 系统配置
├── follow-up-log.md               # 跟进记录（自动生成）
└── skills/
    └── foreign-trade-customer-activation/
        └── SKILL.md               # 本文件
```

## 限制规则

- ✅ 每天最多发送5条激活消息
- ✅ 同一客户最多跟进3次
- ✅ 超过15天未回复自动标记为"已关闭"
- ✅ 只在工作日运行（周一至周五）
- ✅ 必须获得用户明确批准后才能发送

## 更新日志

### v1.0.0 (2026-03-20)
- 初始版本发布
- 支持客户状态监控
- 支持三级话术模板
- 支持每日自动运行

## 注意事项

1. 需要配置 WhatsApp 或 Feishu 消息通道
2. 客户列表需要手动维护更新
3. 所有消息发送前必须获得用户批准
4. 建议定期备份客户列表文件

## 技术支持

如有问题，请检查：
- Gateway 是否运行：`openclaw gateway status`
- WhatsApp 是否连接：`openclaw channels status`
- Cron 任务状态：`openclaw cron list`
