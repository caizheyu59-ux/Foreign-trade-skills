# GitHub 上传指南

本文档介绍如何将 1688 价格监控系统上传到 GitHub。

---

## 📋 上传前检查清单

### ✅ 文件检查

- [ ] README.md - 项目说明
- [ ] LICENSE - 开源许可证
- [ ] .gitignore - Git 忽略规则
- [ ] docs/ - 完整文档目录
- [ ] config/monitored-products.json.example - 配置示例
- [ ] package.json - Node.js 配置

### ✅ 安全检查

- [ ] 已删除 `.env` 文件
- [ ] 已删除 `config/monitored-products.json`（包含真实手机号）
- [ ] 已删除 `data/` 目录中的敏感数据
- [ ] 已检查代码中无硬编码的密码/API Key

### ✅ Git 检查

- [ ] 所有文件已提交
- [ ] 提交信息清晰
- [ ] 分支为 `main` 或 `master`

---

## 🚀 上传步骤

### 步骤 1：在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name:** `1688-price-monitor`
   - **Description:** 1688 商品价格监控系统，自动监控价格变化并推送 WhatsApp/飞书通知
   - **Visibility:** Public（公开）或 Private（私有）
   - **❌ 不要勾选** "Add a README file"
   - **❌ 不要勾选** "Add .gitignore"
   - **❌ 不要勾选** "Choose a license"
3. 点击 **Create repository**

### 步骤 2：添加远程仓库

在终端执行：

```bash
cd 你的 OpenClaw 工作区\skills\1688-price-monitor

# 替换为你的 GitHub 用户名
git remote add origin https://github.com/your-username/1688-price-monitor.git

# 验证
git remote -v
```

**预期输出：**
```
origin  https://github.com/your-username/1688-price-monitor.git (fetch)
origin  https://github.com/your-username/1688-price-monitor.git (push)
```

### 步骤 3：重命名分支

```bash
git branch -M main
```

### 步骤 4：推送到 GitHub

```bash
git push -u origin main
```

**预期输出：**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX KiB | XX MiB/s, done.
Total XX (delta XX), reused XX (delta XX)
remote: Resolving deltas: 100% (XX/XX), done.
To https://github.com/your-username/1688-price-monitor.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### 步骤 5：验证上传

访问你的 GitHub 仓库：
```
https://github.com/your-username/1688-price-monitor
```

确认所有文件已上传：
- ✅ README.md
- ✅ LICENSE
- ✅ docs/ 目录
- ✅ config/ 目录
- ✅ 所有脚本文件

---

## 🔧 常见问题

### 问题 1：认证失败

**错误：** `Authentication failed`

**解决：**

**使用 HTTPS：**
```bash
# 使用 Personal Access Token 代替密码
git push -u origin main
# 输入 GitHub 用户名和 Token
```

**创建 Token：**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. 勾选 `repo` 权限
4. 复制 Token（只显示一次）

**使用 SSH（推荐）：**
```bash
# 生成 SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 添加到 GitHub
# GitHub → Settings → SSH and GPG keys → New SSH key
# 粘贴 ~/.ssh/id_ed25519.pub 的内容

# 修改远程仓库
git remote set-url origin git@github.com:your-username/1688-price-monitor.git

# 推送
git push -u origin main
```

### 问题 2：仓库已存在

**错误：** `remote origin already exists`

**解决：**
```bash
git remote remove origin
git remote add origin https://github.com/your-username/1688-price-monitor.git
```

### 问题 3：文件太大

**错误：** `File too large`

**解决：**
```bash
# 查找大文件
git rev-list --objects --all | git cat-file --filter='blob(>10M)' --batch-check='%(objectname) %(objecttype) %(rest)'

# 从 Git 历史中删除大文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch 大文件路径" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push origin main --force
```

### 问题 4：推送被拒绝

**错误：** `Updates were rejected because the remote contains work that you do not have`

**解决：**
```bash
# 拉取远程更改
git pull origin main

# 解决冲突后推送
git push -u origin main

# 或强制推送（谨慎使用）
git push -u origin main --force
```

---

## 📝 更新仓库

### 日常更新

```bash
# 提交更改
git add .
git commit -m "描述更改内容"

# 推送到 GitHub
git push origin main
```

### 发布新版本

```bash
# 打标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0
```

然后在 GitHub Releases 页面创建 Release。

---

## 📊 仓库优化

### 添加主题标签

在 GitHub 仓库页面：
1. Settings → About
2. 添加 topics：`1688` `price-monitor` `openclaw` `whatsapp` `feishu` `ecommerce`

### 添加描述

编辑 About 部分：
```
🔍 1688 商品价格监控系统 | 自动监控价格变化 | WhatsApp/飞书实时通知 | OpenClaw Skill
```

### 添加网站链接

如果有演示页面或文档网站，添加到 About 部分。

---

## 🎯 下一步

上传完成后：

1. **分享仓库链接** - 发给需要的人
2. **配置 GitHub Actions** - 自动化测试和部署
3. **添加 Issue 模板** - 方便用户反馈问题
4. **编写贡献指南** - CONTRIBUTING.md

---

## 📚 参考资源

- [GitHub 文档](https://docs.github.com/)
- [Git 入门指南](https://git-scm.com/book/zh/v2)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

---

**版本：** 1.0.0  
**最后更新：** 2026-04-01
