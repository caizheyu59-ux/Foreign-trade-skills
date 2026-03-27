---
name: wmlx-multilingual-product-seo
description: Generate multilingual SEO-optimized product descriptions for cross-border e-commerce. Supports English, Spanish, Russian, and Arabic with search engine-specific optimization (Google/Bing, Yandex, Middle East markets). Use when users need to create SEO-friendly product copy for international markets, batch generate product descriptions, or optimize content for specific search engines and regional preferences.
---

# Multilingual SEO Product Description Generator

Generate professional, SEO-optimized product descriptions in multiple languages for cross-border e-commerce.

## Supported Languages & Markets

- **English (en)**: Google/Bing (US/EU) - E-E-A-T focus, semantic richness
- **Spanish (es)**: Google (Latin America/Spain) - Experience and benefits
- **French (fr)**: Google (France/Canada/Belgium) - Quality certification, eco-friendly
- **German (de)**: Google (Germany/Austria/Switzerland) - Technical precision, energy efficiency
- **Russian (ru)**: Yandex - Technical depth, parameter focus
- **Japanese (ja)**: Google/Yahoo Japan - Compact design, energy efficiency, polite descriptions
- **Korean (ko)**: Naver/Google Korea - Trendy design, KOL recommendations, social proof
- **Portuguese (pt)**: Google (Brazil/Portugal) - Value for money, installment options
- **Arabic (ar)**: Middle East - RTL-friendly, durability emphasis, cultural adaptation
- **Chinese (zh)**: Baidu/360/Sogou (China) - Trust signals, social proof, price-performance

## Core Workflow

### Phase 1: Intelligence Processing
1. Extract from user input: [Core Function], [Pain Point Solved], [Tech Specs], [Target Audience]
2. Auto-generate 5 high-frequency search keywords per language based on seed terms

### Phase 2: Standard Output Template

For each language, generate:

#### 1. SEO Metadata
- **Title Tag** (Max 60 chars): Core keyword + click-worthy hook
- **Meta Description** (Max 155 chars): Value summary + CTA

#### 2. Conversion Copy (AIDA Model)
- **[Attention]**: First sentence hits the user's pain point directly
- **[Interest/Desire]**:
  - 🏆 *[Benefit 1]*
  - 🛡️ *[Benefit 2 - Quality/Durability]*
  - ⚡ *[Benefit 3 - Convenience/Tech]*
- **[Action]**: Guiding purchase recommendation

#### 3. Specifications Table
Markdown table with technical parameters

#### 4. Search Engine Strategy
Brief explanation of localization choices (local idioms, platform-specific optimizations)

## Execution Modes

### Single Product Mode
Process one product with detailed input.

### Batch Processing Mode
Read from `input.csv` or `products.md`, create folders per product, generate `[language].md` files.

## Quality Constraints

1. **NO machine translation**: Use local e-commerce terminology, not literal translations
2. **Concise & powerful**: No fluff, every word counts
3. **HTML/Markdown friendly**: Standard formatting for web use

## Scripts

- `scripts/generate_descriptions.py`: Core generation script supporting single/batch modes
- `scripts/batch_processor.py`: Process CSV/MD files for bulk generation

## References

- `references/seo-strategies.md`: Detailed search engine optimization strategies per platform
- `references/keyword-patterns.md`: High-converting keyword patterns by language/market
- `references/cultural-guidelines.md`: Cultural adaptation guidelines for Arabic and other markets

## Usage Examples

**Single product:**
```
Product: Solar camping lantern. 5000mAh battery, foldable, Type-C fast charging, IP65 waterproof, for camping and emergency power outages.
```

**Batch processing:**
```
Process all products in input.csv and generate descriptions for EN, ES, FR, DE, RU, JA, KO, PT, AR, ZH
```

**Language codes:**
- `en` - English
- `es` - Spanish  
- `fr` - French
- `de` - German
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `pt` - Portuguese
- `ar` - Arabic
- `zh` - Chinese
