# WMLX-Multilingual-Product-SEO

🌍 **多语言 SEO 产品描述生成器** - 为全球跨境电商打造的专业 SEO 文案工具

Generate multilingual SEO-optimized product descriptions for global cross-border e-commerce.

---

## 🚀 功能特点

- **10 种语言支持**：英语、西班牙语、法语、德语、俄语、日语、韩语、葡萄牙语、阿拉伯语、中文
- **搜索引擎优化**：针对不同搜索引擎算法定制（Google、Yandex、Naver、百度等）
- **AIDA 转化模型**：Attention → Interest/Desire → Action
- **批量处理**：支持 CSV/Markdown 文件批量生成
- **技术参数自动提取**：智能识别产品规格

---

## 📦 安装

### 方式 1：直接下载
下载 `WMLX-Multilingual-Product-SEO.skill` 文件，安装到 OpenClaw。

### 方式 2：源码安装
```bash
git clone https://github.com/yourusername/WMLX-Multilingual-Product-SEO.git
cd WMLX-Multilingual-Product-SEO
```

---

## 🎯 使用方法

### 单产品模式

```bash
python scripts/generate_descriptions.py \
  -i "AirNest Smart Air Purifier, 4-stage purification H13 HEPA, 5200mAh battery" \
  -o ./output \
  -l "en,es,fr,de,ru,ja,ko,pt,ar,zh"
```

### 批量处理模式

```bash
python scripts/batch_processor.py \
  products.csv \
  -o ./output \
  -l "en,es,fr,de,ru,ja,ko,pt,ar,zh"
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-i, --input` | 产品描述文本或文件路径 | `"Product description..."` |
| `-o, --output` | 输出目录 | `./output` |
| `-l, --languages` | 语言代码（逗号分隔） | `en,es,fr,de,ru,ja,ko,pt,ar,zh` |
| `-b, --batch` | 批处理模式（输入为 CSV/MD） | - |

---

## 🌐 支持语言

| 代码 | 语言 | 搜索引擎 | 市场特点 |
|------|------|----------|----------|
| en | 🇺🇸 英语 | Google/Bing | E-E-A-T 优化，语义丰富 |
| es | 🇪🇸 西班牙语 | Google | 拉美/西班牙，体验优先 |
| fr | 🇫🇷 法语 | Google | 法国/加拿大/比利时，环保认证 |
| de | 🇩🇪 德语 | Google | 德国/奥地利/瑞士，技术精确 |
| ru | 🇷🇺 俄语 | Yandex | 技术深度，详细参数 |
| ja | 🇯🇵 日语 | Google/Yahoo Japan | 紧凑设计，礼貌用语 |
| ko | 🇰🇷 韩语 | Naver/Google Korea | 潮流设计，社交证明 |
| pt | 🇵🇹 葡萄牙语 | Google | 巴西/葡萄牙，分期付款 |
| ar | 🇸🇦 阿拉伯语 | - | 中东 RTL，耐用性强调 |
| zh | 🇨🇳 中文 | 百度/360/搜狗 | 信任信号，性价比 |

---

## 📄 输出格式

每个语言生成一个 Markdown 文件，包含：

### 1. SEO 元数据
- Title Tag（60字符限制）
- Meta Description（155字符限制）
- 5个高频关键词

### 2. 转化文案（AIDA）
- **Attention**：直击痛点
- **Interest/Desire**：3个核心卖点（🏆🛡️⚡）
- **Action**：购买引导 + 退款保证

### 3. 技术参数表
| 参数 | 详情 |
|:----------|:--------|
| Battery | 5200mAh |
| Material | aluminum, ABS |

### 4. 搜索引擎策略
- 各平台优化策略说明
- 本地化注释

---

## 📂 项目结构

```
WMLX-Multilingual-Product-SEO/
├── SKILL.md                          # Skill 主文档
├── README.md                         # 本文件
├── scripts/
│   ├── generate_descriptions.py      # 核心生成脚本
│   └── batch_processor.py            # 批处理脚本
├── references/
│   ├── seo-strategies.md             # SEO 策略指南
│   ├── keyword-patterns.md           # 关键词模式
│   └── cultural-guidelines.md        # 文化适配指南
├── assets/
│   ├── example-input.csv             # CSV 示例输入
│   └── example-input.md              # Markdown 示例输入
└── .gitignore                        # Git 忽略文件
```

---

## 💡 使用示例

### 示例 1：智能空气净化器

**输入：**
```
AirNest Smart Air Purifier, 4-stage purification (H13 HEPA + activated carbon + 
negative ions), intelligent air quality monitoring with auto mode, wireless portable 
use, App remote control, ambient night light. 5200mAh battery (4-12 hours wireless), 
size φ185×280mm, weight 1.6kg, aviation-grade aluminum alloy + ABS, coverage 5-20㎡, 
noise ≤25-52dB.
```

**输出：** 10 个语言的完整 SEO 描述文件

---

## 🔧 技术参数

- **Python 版本**: 3.8+
- **依赖**: 无第三方依赖（纯 Python 标准库）
- **平台**: Windows/macOS/Linux

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- 基于 OpenClaw Skill Creator 创建
- 感谢跨境电商社区的支持

---

## 📧 联系方式

如有问题或建议，欢迎通过以下方式联系：
- GitHub Issues: [提交问题](https://github.com/yourusername/WMLX-Multilingual-Product-SEO/issues)
- Email: your.email@example.com

---

**Made with ❤️ for global cross-border e-commerce**
