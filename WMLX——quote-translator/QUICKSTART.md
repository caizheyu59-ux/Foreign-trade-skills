# 🚀 快速开始指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 测试翻译

```bash
# 翻译 Excel 文件为日语
python scripts/translate_quote.py your_quote.xlsx -l ja

# 翻译为中文
python scripts/translate_quote.py your_quote.xlsx -l zh

# 翻译为西班牙语
python scripts/translate_quote.py your_quote.xlsx -l es
```

## 3. 使用自定义词库（可选）

```bash
python scripts/translate_quote.py your_quote.xlsx -l ja -c example_translations.json
```

## 4. 查看帮助

```bash
python scripts/translate_quote.py --help
```

## 5. 支持的语言

- `zh` - 中文
- `en` - 英语
- `ja` - 日语
- `ko` - 韩语
- `es` - 西班牙语
- `fr` - 法语
- `de` - 德语
- `ru` - 俄语
- `pt` - 葡萄牙语
- `ar` - 阿拉伯语
- `hi` - 印地语

## 6. 支持的格式

- Excel: `.xlsx`, `.xlsm`, `.xls`
- HTML: `.html`, `.htm`
- Word: `.docx`

---

**就这么简单！** 🍟
