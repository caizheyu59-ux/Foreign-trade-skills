# quote-translator - 报价单翻译器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)]()

> 🌍 读取现有报价单文件（Excel/HTML/Word），仅翻译文字内容，保留原始样式、格式、公式，输出同格式的多语言报价单。

---

## ✨ 特性亮点

- ✅ **保留原样式** - Excel 格式、CSS、布局、字体、颜色、公式完全不变
- ✅ **仅翻译文字** - 不改动任何格式、结构、图片
- ✅ **多格式支持** - Excel (.xlsx/.xls)、HTML、Word (.docx)
- ✅ **11 种语言** - 中文、英语、西班牙语、印地语、阿拉伯语、法语、俄语、葡萄牙语、德语、日语、韩语
- ✅ **无需 API** - 内置翻译词库，开箱即用
- ✅ **支持定制** - 可为特定客户/产品定制翻译词库

---

## 🚀 快速开始

### 安装依赖

```bash
pip install openpyxl beautifulsoup4 lxml python-docx
```

### 基本用法

```bash
# 翻译 Excel 报价单为日语
python scripts/translate_quote.py quotation.xlsx -l ja

# 翻译 HTML 报价单为西班牙语
python scripts/translate_quote.py quote.html -l es

# 翻译 Word 报价单为法语
python scripts/translate_quote.py quote.docx -l fr

# 指定输出路径
python scripts/translate_quote.py quote.xlsx -l de -o german_quote.xlsx

# 使用自定义翻译词库
python scripts/translate_quote.py quote.xlsx -l ja -c my_translations.json
```

### Python 代码调用

```python
from scripts.translate_quote import translate_excel, translate_html, translate_word

# 翻译 Excel
output_path, count = translate_excel('quotation.xlsx', 'ja')
print(f"翻译了 {count} 个单元格")

# 翻译 HTML
output_path, count = translate_html('quote.html', 'es')

# 翻译 Word
output_path, count = translate_word('quote.docx', 'fr')
```

---

## 📋 支持的语言

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| `zh` | 中文 | `en` | 英语 |
| `es` | 西班牙语 | `hi` | 印地语 |
| `ar` | 阿拉伯语 | `fr` | 法语 |
| `ru` | 俄语 | `pt` | 葡萄牙语 |
| `de` | 德语 | `ja` | 日语 |
| `ko` | 韩语 | | |

---

## 📁 支持的文件格式

| 格式 | 扩展名 | 保留内容 |
|------|--------|----------|
| **Excel** | `.xlsx`, `.xlsm`, `.xls` | ✅ 样式、公式、格式、合并单元格、条件格式 |
| **HTML** | `.html`, `.htm` | ✅ CSS 样式、布局、字体、颜色 |
| **Word** | `.docx` | ✅ 字体、颜色、表格、段落格式 |

---

## 🎨 自定义翻译词库

创建 `my_translations.json`：

```json
{
  "ja": {
    "Charms": "チャーム",
    "Stainless steel Charms": "ステンレススチールチャーム",
    "Contact us for more Collection": "その他のコレクションについてはお問い合わせください"
  },
  "es": {
    "Charms": "Dijes",
    "Stainless steel Charms": "Dijes de acero inoxidable"
  }
}
```

使用：
```bash
python scripts/translate_quote.py quote.xlsx -l ja -c my_translations.json
```

---

## 📝 使用案例

### 案例 1：珠宝报价单多语言版本

```bash
# 生成中文版
python scripts/translate_quote.py dg1688_template_quote.xlsx -l zh

# 生成日语版
python scripts/translate_quote.py dg1688_template_quote.xlsx -l ja

# 生成西班牙语版
python scripts/translate_quote.py dg1688_template_quote.xlsx -l es
```

### 案例 2：阿拉伯语报价单（RTL 布局）

```bash
python scripts/translate_quote.py quotation.html -l ar
```

输出自动添加 `dir="rtl"` 属性，文字从右到左排列。

---

## ⚠️ 注意事项

### ✅ 适合的场景
- 报价单、产品目录、价格表
- 包含产品描述、公司介绍的文档
- 需要保留原格式的正式文件

### ⚠️ 限制
- **图片中的文字不翻译** - 仅翻译文本内容
- **复杂表格建议校对** - 翻译后建议人工检查
- **专业术语建议定制词库** - 行业特定术语添加到自定义词库

---

## 🔄 更新日志

### v2.0.0 (2026-03-31)
- ✅ 重构为直接翻译模式，无需外部 API
- ✅ 支持 Excel 格式（.xlsx, .xlsm, .xls）
- ✅ 支持自定义翻译词库
- ✅ 优化文本识别逻辑（跳过网址、邮箱、产品编号）
- ✅ 内置长文本翻译模板

### v1.0.0 (2026-03-31)
- 初始版本
- 依赖 DeepL/Google Translate API

---

## 🛠️ 开发

### 添加新语言

在 `scripts/translate_quote.py` 的 `BASE_TRANSLATIONS` 字典中添加新语言。

### 添加长文本模板

在 `LONG_TEXT_TRANSLATIONS` 字典中添加长文本翻译。

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📬 联系方式

- 问题反馈：提交 Issue
- 功能建议：提交 Feature Request

---

**Made with ❤️ by 薯条 🍟**
