# Contributing to WMLX-Multilingual-Product-SEO

首先，感谢您考虑为 WMLX-Multilingual-Product-SEO 做出贡献！正是像您这样的人使得这个工具变得更好。

## 如何贡献

### 报告 Bug

如果您发现了 bug，请通过 GitHub Issues 报告，并包含以下信息：

- 问题的清晰描述
- 重现步骤
- 预期行为 vs 实际行为
- 您的环境信息（操作系统、Python 版本等）
- 相关的错误日志或截图

### 建议新功能

我们欢迎新功能建议！请通过 GitHub Issues 提交，并描述：

- 您想要的功能
- 为什么这个功能有用
- 您设想的实现方式

### 提交代码

1. **Fork 仓库**
   ```bash
   git clone https://github.com/yourusername/WMLX-Multilingual-Product-SEO.git
   cd WMLX-Multilingual-Product-SEO
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行更改**
   - 确保代码符合项目风格
   - 添加必要的注释
   - 更新相关文档

4. **测试**
   - 确保所有现有功能正常工作
   - 测试新功能
   - 验证多语言输出

5. **提交**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **推送并创建 Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 代码风格

- 遵循 PEP 8 Python 代码风格
- 使用有意义的变量名
- 添加 docstrings 到函数和类
- 保持代码简洁明了

## 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响代码运行的变动）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: add Italian language support
fix: resolve encoding issue in Japanese output
docs: update README with new examples
```

## 添加新语言

如果您想添加对新语言的支持，请：

1. 在 `scripts/generate_descriptions.py` 中的 `LANGUAGES` 字典添加语言配置
2. 在 `generate_keywords()` 函数中添加该语言的关键词模板
3. 在 `generate_description()` 函数中的 `templates` 字典添加文案模板
4. 更新 `README.md` 和 `SKILL.md` 中的语言列表
5. 在 `references/` 中添加该语言的文化指南（可选）
6. 测试生成该语言的描述

## 文档

- 更新 README.md 如果添加了新功能
- 更新 CHANGELOG.md 记录变更
- 添加或更新示例代码

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们作为贡献者和维护者承诺：

- 尊重不同的观点和经验
- 接受建设性的批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 我们的标准

有助于创造积极环境的行为包括：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

不可接受的行为包括：

- 使用性暗示语言或图像
- 挑衅、侮辱/贬损性评论，以及个人或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息
- 其他在专业环境中被认为不适当的行为

## 问题？

如果您有任何问题，请随时：

- 打开一个 GitHub Issue
- 联系维护者

## 许可证

通过贡献您的代码，您同意将其许可为 MIT 许可证。

再次感谢！🙏
