# 贡献指南

欢迎参与 quote-translator 项目的开发！

## 如何贡献

### 报告问题

发现 Bug 或有功能建议？请提交 Issue：

1. 搜索现有 Issue，避免重复
2. 使用清晰的标题和描述
3. 提供复现步骤（如果是 Bug）
4. 说明期望行为和实际行为

### 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 代码风格
- 添加必要的注释
- 确保代码有适当的错误处理
- 更新文档说明新功能

### 添加新语言

1. 在 `scripts/translate_quote.py` 的 `BASE_TRANSLATIONS` 中添加翻译词库
2. 在 `SUPPORTED_LANGUAGES` 列表中添加语言代码
3. 在 `LANGUAGE_NAMES` 中添加语言名称
4. 测试翻译效果
5. 更新 README.md 文档

### 添加长文本模板

1. 在 `LONG_TEXT_TRANSLATIONS` 中添加原文和多种语言翻译
2. 确保翻译准确、专业
3. 测试翻译匹配逻辑
4. 更新文档说明

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/quote-translator.git
cd quote-translator

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install openpyxl beautifulsoup4 lxml python-docx

# 运行测试
python scripts/translate_quote.py --help
```

## 发布流程

1. 更新 `CHANGELOG.md`
2. 更新版本号（在 README.md 和脚本中）
3. 提交更改并打标签
4. 推送到 GitHub
5. 创建 GitHub Release

## 联系方式

- 问题反馈：提交 Issue
- 讨论交流：GitHub Discussions

感谢你的贡献！🍟
