# 报价单翻译器 - Quote Translator

**读取现有报价单文件（Excel/HTML/Word），仅翻译文字内容，保留原始样式、格式、公式，输出同格式的多语言报价单。**

---

## 🎯 核心特点

- ✅ **保留原样式** - Excel 格式、CSS、布局、字体、颜色、公式完全不变
- ✅ **仅翻译文字** - 不改动任何格式、结构、图片
- ✅ **多格式支持** - Excel (.xlsx/.xls)、HTML、Word (.docx)
- ✅ **11 种语言** - 中文、英语、西班牙语、印地语、阿拉伯语、法语、俄语、葡萄牙语、德语、日语、韩语
- ✅ **无需 API** - 内置翻译能力，开箱即用
- ✅ **支持定制** - 可为特定客户/产品定制翻译词库

---

## 📋 支持语言

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| `zh` | 中文 | `en` | 英语 |
| `es` | 西班牙语 | `hi` | 印地语 |
| `ar` | 阿拉伯语 | `fr` | 法语 |
| `ru` | 俄语 | `pt` | 葡萄牙语 |
| `de` | 德语 | `ja` | 日语 |
| `ko` | 韩语 | | |

---

## 🚀 使用方式

### 方式 1：直接告诉 AI（推荐）

直接告诉我文件路径和目标语言，我帮你翻译：

> "把 C:\Users\...\quote.xlsx 翻译成日语"
> "翻译这个 Excel 报价单为西班牙语"
> "生成阿拉伯语版本的报价单"

### 方式 2：使用脚本

```bash
python scripts/translate_quote.py <报价单文件> -l <语言代码> [-o 输出路径]
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-l, --lang` | 目标语言 (zh/en/es/hi/ar/fr/ru/pt/de/ja/ko) | `en` |
| `-o, --output` | 输出文件路径 | 自动生成（原文件名_lang.扩展名） |
| `-c, --custom` | 自定义翻译词库 JSON 文件 | 无 |

### 示例

```bash
# 翻译 Excel 报价单为日语
python scripts/translate_quote.py quotation.xlsx -l ja

# 翻译 HTML 报价单为西班牙语，指定输出路径
python scripts/translate_quote.py quote.html -l es -o spanish_quote.html

# 翻译 Word 报价单为法语
python scripts/translate_quote.py quote.docx -l fr

# 使用自定义翻译词库
python scripts/translate_quote.py quote.xlsx -l de -c my_translations.json

# 翻译为阿拉伯语（自动 RTL 布局）
python scripts/translate_quote.py quote.html -l ar
```

---

## 📁 支持的文件格式

| 格式 | 扩展名 | 保留内容 |
|------|--------|----------|
| **Excel** | `.xlsx`, `.xlsm`, `.xls` | ✅ 样式、公式、格式、合并单元格、条件格式 |
| **HTML** | `.html`, `.htm` | ✅ CSS 样式、布局、字体、颜色 |
| **Word** | `.docx` | ✅ 字体、颜色、表格、段落格式 |

---

## 🔧 工作原理

### Excel 文件
1. 使用 `openpyxl` 加载工作簿，保留所有样式和公式
2. 遍历所有工作表和单元格
3. 识别需要翻译的文本（跳过网址、邮箱、产品编号等）
4. 翻译文本内容，保留单元格格式
5. 保存为新文件

### HTML 文件
1. 解析 HTML 结构（使用 BeautifulSoup）
2. 提取所有文本节点（跳过 `<script>`、`<style>` 标签）
3. 翻译文本内容
4. 保持原有 HTML 结构不变，仅替换文本
5. 阿拉伯语自动添加 `dir="rtl"` 属性

### Word 文件
1. 解析 Word 文档（使用 python-docx）
2. 遍历所有段落和表格
3. 翻译文本内容
4. 保持原有样式（字体、颜色、边框等）

---

## 📦 依赖安装

```bash
pip install openpyxl beautifulsoup4 lxml python-docx python-dotenv
```

---

## 🎨 定制翻译词库

如果需要为特定产品/客户定制翻译，可以创建自定义词库：

**创建 `my_translations.json`：**
```json
{
  "en": {
    "Charms": "吊坠",
    "Stainless steel Charms": "不锈钢吊坠",
    "Contact us for more Collection": "联系我们获取更多系列"
  },
  "ja": {
    "Charms": "チャーム",
    "Stainless steel Charms": "ステンレススチールチャーム",
    "Contact us for more Collection": "その他のコレクションについてはお問い合わせください"
  }
}
```

**使用自定义词库：**
```bash
python scripts/translate_quote.py quote.xlsx -l ja -c my_translations.json
```

---

## ⚠️ 注意事项

### ✅ 适合的场景
- 报价单、产品目录、价格表
- 包含产品描述、公司介绍的文档
- 需要保留原格式的正式文件

### ⚠️ 限制
- **图片中的文字不翻译** - 仅翻译文本内容，图片内文字需手动处理
- **复杂表格建议校对** - 嵌套表格、合并单元格等复杂结构建议翻译后人工检查
- **专业术语建议定制词库** - 行业特定术语建议添加到自定义词库确保准确

---

## 📂 文件结构

```
quote-translator/
├── SKILL.md                  # 技能说明（本文件）
├── README.md                 # 详细文档
├── .env.example              # API 配置示例（可选）
├── scripts/
│   ├── translate_quote.py    # 主脚本
│   └── templates/            # 翻译模板（可选）
│       ├── jewelry.json      # 珠宝行业模板
│       └── electronics.json  # 电子产品模板
└── examples/                 # 示例文件（可选）
```

---

## 📝 使用案例

### 案例 1：珠宝报价单多语言版本

**原始文件**：`dg1688_template_quote.xlsx`（英文）

**需求**：生成中文、日语、西班牙语版本

**操作**：
```bash
python scripts/translate_quote.py dg1688_template_quote.xlsx -l zh
python scripts/translate_quote.py dg1688_template_quote.xlsx -l ja
python scripts/translate_quote.py dg1688_template_quote.xlsx -l es
```

**输出**：
- `dg1688_template_quote_zh.xlsx`（中文）
- `dg1688_template_quote_ja.xlsx`（日语）
- `dg1688_template_quote_es.xlsx`（西班牙语）

### 案例 2：HTML 报价单阿拉伯语版本

**原始文件**：`quotation.html`（英文）

**需求**：生成阿拉伯语版本（RTL 布局）

**操作**：
```bash
python scripts/translate_quote.py quotation.html -l ar
```

**输出**：`quotation_ar.html`（自动添加 `dir="rtl"` 属性）

---

## 🔄 版本历史

### v2.0.0 (2026-03-31)
- ✅ 重构为直接翻译模式，无需外部 API
- ✅ 支持 Excel 格式（.xlsx, .xlsm, .xls）
- ✅ 支持自定义翻译词库
- ✅ 优化文本识别逻辑（跳过网址、邮箱、产品编号）
- ❌ 移除对外部翻译 API 的依赖

### v1.0.0 (2026-03-31)
- 初始版本
- 支持 HTML、Word、Markdown
- 依赖 DeepL/Google Translate API

---

## 📍 技能位置

```
C:\Users\caizheyu\.openclaw\workspace\skills\quote-translator\
```

---

## 💡 快速开始

**最简单的方式**：

直接告诉我：
> "把这份报价单翻译成 [语言]"

我会自动处理，生成翻译后的文件！🍟

---

**创建时间**：2026-03-31  
**作者**：薯条 🍟  
**版本**：v2.0.0
