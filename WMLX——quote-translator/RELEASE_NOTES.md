# 🎉 quote-translator v2.0.0 发布说明

## 项目概述

**quote-translator** 是一个专业的报价单翻译工具，支持 Excel、HTML、Word 格式的多语言翻译，保留原始样式和格式。

## ✨ 核心特性

- 🌍 **11 种语言支持** - 中文、英语、日语、韩语、西班牙语、法语、德语、俄语、葡萄牙语、阿拉伯语、印地语
- 📊 **多格式支持** - Excel (.xlsx/.xls)、HTML、Word (.docx)
- 🎨 **保留原样式** - 样式、公式、格式、布局完全不变
- ⚡ **无需 API** - 内置翻译词库，开箱即用
- 🔧 **支持定制** - 可自定义翻译词库

## 🚀 快速使用

```bash
# 安装依赖
pip install -r requirements.txt

# 翻译 Excel 为日语
python scripts/translate_quote.py quotation.xlsx -l ja

# 翻译为中文
python scripts/translate_quote.py quotation.xlsx -l zh
```

## 📦 安装

```bash
# 从源码安装
pip install .

# 或直接使用
python scripts/translate_quote.py --help
```

## 📚 文档

- [README.md](README.md) - 完整使用说明
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南

## 🔄 更新日志

### v2.0.0 (2026-03-31)
- ✅ 重构为直接翻译模式，无需外部 API
- ✅ 支持 Excel 格式（.xlsx, .xlsm, .xls）
- ✅ 支持自定义翻译词库
- ✅ 优化文本识别逻辑
- ✅ 内置长文本翻译模板

## 📄 许可证

MIT License

---

**Made with ❤️ by 薯条 🍟**
