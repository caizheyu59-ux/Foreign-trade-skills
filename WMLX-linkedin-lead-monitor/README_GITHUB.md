# LinkedIn 潜客监控系统

> 🍟 自动监控 LinkedIn 潜客动态，AI 识别商机，飞书即时推送

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/linkedin-lead-monitor)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📋 项目简介

**LinkedIn 潜客监控系统** 是一款面向 B2B 外贸销售和跨境电商的智能监控工具，可自动追踪目标潜客的 LinkedIn 动态，识别商机优先级，并通过飞书即时推送跟进建议。

### 核心功能

- ✅ **自动监控** - 7x24 小时监控潜客 LinkedIn 动态
- ✅ **商机识别** - AI 分析动态内容，识别高优先级商机
- ✅ **飞书推送** - 实时推送潜客动态报告
- ✅ **智能去重** - 自动过滤已推送内容，避免重复
- ✅ **持续监控** - 支持后台持续运行，定时检查

### 使用场景

| 场景 | 说明 |
|------|------|
| B2B 外贸销售 | 监控目标公司采购负责人动态，把握最佳接触时机 |
| 跨境电商 BD | 发现潜在客户的采购需求和业务扩张信号 |
| 海外业务拓展 | 跟踪决策人职位变动，及时调整跟进策略 |

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- Windows / macOS / Linux
- 飞书账号（接收推送）
- LinkedIn 账号（用于登录）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/linkedin-lead-monitor.git
cd linkedin-lead-monitor
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

#### 3. 配置环境

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件（填写你的账号信息）
# Windows: notepad .env
# macOS/Linux: nano .env
```

#### 4. 检查配置

```bash
python scripts/check_config.py
```

#### 5. 登录 LinkedIn

```bash
python scripts/cli.py login
```

在打开的浏览器中手动登录 LinkedIn，会话会自动保存。

#### 6. 添加潜客

```bash
python scripts/cli.py add --url "https://www.linkedin.com/in/潜客 URL" --name "姓名" --priority high
```

#### 7. 开始监控

```bash
# 单次检查
python scripts/cli.py check

# 持续监控（每 30 分钟）
python scripts/cli.py watch --interval 30
```

---

## 📁 项目结构

```
linkedin-lead-monitor/
├── .env.example              # 配置模板
├── .gitignore                # Git 忽略文件
├── README.md                 # 本文档
├── SKILL.md                  # 完整使用文档
├── BUGFIX_TODO.md            # 已知问题和改进计划
├── requirements.txt          # Python 依赖
├── data/                     # 数据目录（不提交到 Git）
│   ├── leads.db              # SQLite 数据库
│   └── state/                # 浏览器状态
└── scripts/
    ├── cli.py                # 命令行工具
    ├── monitor.py            # 监控核心逻辑
    ├── notify.py             # 消息推送模块
    └── check_config.py       # 配置检查工具
```

---

## ⚙️ 配置说明

### 必填配置（.env 文件）

```bash
# LinkedIn 账号
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# 飞书用户 ID
FEISHU_USER_ID=ou_xxxxxxxxxxxxxxxxxxxxxxxxx
```

### 可选配置

```bash
# 飞书 Webhook（备用）
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx

# Chrome 用户数据（复用已登录的 Chrome）
CHROME_USER_DATA=/path/to/chrome/profile

# 监控间隔（分钟）
CHECK_INTERVAL_MINUTES=30
```

---

## 📊 命令行工具

### 潜客管理

```bash
# 添加潜客
python scripts/cli.py add --url <URL> --name <姓名> [--priority high|medium|low]

# 查看列表
python scripts/cli.py list

# 删除潜客
python scripts/cli.py remove --name <姓名>

# 批量导入（CSV）
python scripts/cli.py import --file leads.csv
```

### 监控执行

```bash
# 单次检查
python scripts/cli.py check

# 检查特定潜客
python scripts/cli.py check --name "姓名"

# 持续监控
python scripts/cli.py watch --interval 30
```

### 系统工具

```bash
# 配置检查
python scripts/check_config.py

# 手动登录
python scripts/cli.py login

# 查看状态
python scripts/cli.py status
```

---

## 📬 推送规则

### 优先级分类

| 优先级 | 触发条件 | 推送方式 |
|--------|----------|----------|
| 🔴 **高** | 职位变动、公司变更、融资/扩张 | 飞书即时推送 |
| 🟡 **中** | 高优先级潜客的新动态 | 飞书即时推送 |
| 🟢 **低** | 普通动态 | 计入报告，不单独推送 |

### 报告格式

```
📊 LinkedIn 潜客动态报告

潜客：Jolin Ren
公司：XXX 公司
时间：2026-04-02 15:00

最新动态（5 条）:
1. 任巧玲 - B2B Social Media & AI Lead Generation...
2. 越来越多的企业重视社媒，需要在社媒上开发...
3. 越来越多的企业重视社媒，需要在社媒上开发...
4. 任巧玲 - B2B Social Media & AI Lead Generation...
5. Today's global trade briefing is not about more in...

💡 建议：点赞互动 + 关注动态 + 寻找沟通时机

主页：https://www.linkedin.com/in/renqiaoling20200108/
```

---

## 🔧 故障排查

### 常见问题

**Q: 浏览器启动失败？**
```bash
playwright install chromium
```

**Q: LinkedIn 登录失败？**
```bash
python scripts/cli.py login
# 在浏览器中手动完成登录
```

**Q: 飞书推送失败？**
- 检查 `FEISHU_USER_ID` 是否正确
- 确保 OpenClaw 飞书集成已配置
- 或配置 `FEISHU_WEBHOOK_URL` 使用飞书机器人

**Q: 动态抓取为空？**
- 确保 LinkedIn 已登录
- 潜客可能没有公开动态
- 检查网络连接

详细故障排查请查看 [SKILL.md](SKILL.md)

---

## 🔒 安全注意事项

### 1. 账号安全

- ⚠️ 建议使用专门的 LinkedIn 监控账号
- ⚠️ 不要频繁登录/退出，避免触发风控
- ⚠️ 设置合理的检查间隔（≥15 分钟）

### 2. 数据安全

- 🔒 `.env` 文件不要提交到 Git
- 🔒 定期备份数据库文件
- 🔒 敏感信息使用环境变量

### 3. 合规使用

- ✅ 遵守 LinkedIn 服务条款
- ✅ 仅监控已建立业务联系的潜客
- ✅ 不要用于骚扰或垃圾营销

---

## 📝 更新日志

### v1.0.0 (2026-04-02)

- ✅ 初始版本发布
- ✅ LinkedIn 自动登录
- ✅ 动态抓取与去重
- ✅ 飞书推送集成
- ✅ 配置检查工具
- ✅ 完整文档

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m "Add some AmazingFeature"`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 📞 联系方式

- 作者：薯条 🍟
- 所属团队：Kingsway Video 产品运营

---

**🍟 如果觉得项目有用，请给个 Star！**
