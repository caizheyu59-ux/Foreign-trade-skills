#!/usr/bin/env python3
"""
Multilingual SEO Product Description Generator
Generates SEO-optimized product descriptions in multiple languages.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Language configurations
LANGUAGES = {
    "en": {
        "name": "English",
        "market": "Google/Bing (US/EU)",
        "strategy": "Focus on E-E-A-T, semantic richness, and rich snippets optimization"
    },
    "es": {
        "name": "Spanish", 
        "market": "Google (Latin America/Spain)",
        "strategy": "Emphasize experience and benefits, use regional Spanish variations"
    },
    "fr": {
        "name": "French",
        "market": "Google (France/Canada/Belgium)",
        "strategy": "Emphasize quality certification, eco-friendly features, and design aesthetics"
    },
    "de": {
        "name": "German",
        "market": "Google (Germany/Austria/Switzerland)",
        "strategy": "Focus on technical precision, energy efficiency, and compliance with German standards"
    },
    "ru": {
        "name": "Russian",
        "market": "Yandex",
        "strategy": "Technical depth, detailed parameters, long-tail keyword optimization"
    },
    "ja": {
        "name": "Japanese",
        "market": "Google/Yahoo Japan",
        "strategy": "Emphasize compact design, energy efficiency, and space-saving features; polite and detailed descriptions"
    },
    "ko": {
        "name": "Korean",
        "market": "Naver/Google Korea",
        "strategy": "Focus on trendy design, KOL recommendations, and social proof; emphasize gift-worthiness"
    },
    "pt": {
        "name": "Portuguese",
        "market": "Google (Brazil/Portugal)",
        "market": "Google (Brazil/Portugal)",
        "strategy": "Emphasize value for money, installment payment options, and local delivery"
    },
    "ar": {
        "name": "Arabic",
        "market": "Middle East",
        "strategy": "RTL-friendly, emphasize durability and official warranty, cultural adaptation"
    },
    "zh": {
        "name": "Chinese",
        "market": "Baidu/360/Sogou (China)",
        "strategy": "Focus on trust signals, social proof, and price-performance ratio; emphasize official stores and certifications"
    }
}

def parse_product_input(text):
    """Extract product information from input text."""
    product = {
        "name": "",
        "core_function": "",
        "pain_points": [],
        "tech_specs": {},
        "target_audience": "",
        "raw_input": text
    }
    
    # Try to extract product name
    name_match = re.search(r'[Pp]roduct[:：]\s*([^\n。]+)', text)
    if name_match:
        product["name"] = name_match.group(1).strip()
    else:
        # Use first sentence as name
        product["name"] = text.split('。')[0].split('.')[0][:50]
    
    # Extract technical specs (patterns like "5000mAh", "IP65", "Type-C")
    spec_patterns = {
        "battery": r'(\d+\s*mAh|\d+\s*Wh)',
        "waterproof": r'(IP\d+)',
        "charging": r'(Type-C|USB-C|wireless|fast.charging)',
        "size_weight": r'(\d+\s*(cm|mm|m|g|kg))',
        "material": r'(aluminum|plastic|silicone|metal|ABS)'
    }
    
    for key, pattern in spec_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            product["tech_specs"][key] = matches
    
    # Extract use cases / target audience
    use_case_keywords = ["camping", "emergency", "outdoor", "home", "office", "travel", "sports"]
    for keyword in use_case_keywords:
        if keyword in text.lower():
            product["target_audience"] += f"{keyword}, "
    
    product["target_audience"] = product["target_audience"].rstrip(", ")
    
    return product

def generate_keywords(product, lang):
    """Generate 5 high-frequency keywords for the product in target language."""
    product_name = product["name"].lower()
    
    keywords_map = {
        "en": [
            f"best {product_name}",
            f"{product_name} review",
            f"{product_name} 2024",
            f"buy {product_name} online",
            f"{product_name} deals"
        ],
        "es": [
            f"mejor {product_name}",
            f"{product_name} opiniones",
            f"{product_name} comprar",
            f"{product_name} oferta",
            f"{product_name} calidad"
        ],
        "fr": [
            f"meilleur {product_name}",
            f"{product_name} avis",
            f"{product_name} acheter",
            f"{product_name} prix",
            f"{product_name} qualité"
        ],
        "de": [
            f"bester {product_name}",
            f"{product_name} test",
            f"{product_name} kaufen",
            f"{product_name} preis",
            f"{product_name} qualität"
        ],
        "ru": [
            f"лучший {product_name}",
            f"{product_name} купить",
            f"{product_name} отзывы",
            f"{product_name} цена",
            f"{product_name} характеристики"
        ],
        "ja": [
            f"{product_name} おすすめ",
            f"{product_name} レビュー",
            f"{product_name} 購入",
            f"{product_name} 価格",
            f"{product_name} 口コミ"
        ],
        "ko": [
            f"{product_name} 추천",
            f"{product_name} 리뷰",
            f"{product_name} 구매",
            f"{product_name} 가격",
            f"{product_name} 후기"
        ],
        "pt": [
            f"melhor {product_name}",
            f"{product_name} avaliação",
            f"{product_name} comprar",
            f"{product_name} preço",
            f"{product_name} qualidade"
        ],
        "ar": [
            f"أفضل {product_name}",
            f"{product_name} شراء",
            f"{product_name} سعر",
            f"{product_name} تقييم",
            f"{product_name} ضمان"
        ],
        "zh": [
            f"{product_name} 推荐",
            f"{product_name} 评测",
            f"{product_name} 购买",
            f"{product_name} 价格",
            f"{product_name} 怎么样"
        ]
    }
    
    return keywords_map.get(lang, keywords_map["en"])

def generate_description(product, lang):
    """Generate full product description for a specific language."""
    lang_config = LANGUAGES[lang]
    keywords = generate_keywords(product, lang)
    
    # Template for each language
    templates = {
        "en": {
            "title": f"Best {product['name']} 2024 | Top Quality & Fast Shipping",
            "meta_desc": f"Shop the best {product['name']} with premium quality. {list(product['tech_specs'].values())[0][0] if product['tech_specs'] else 'High performance'}. Buy now with free shipping!",
            "attention": f"Tired of unreliable gear that fails when you need it most?",
            "benefits": [
                "🏆 Superior performance with cutting-edge technology",
                "🛡️ Built to last with premium materials and rigorous testing",
                "⚡ Fast charging and long-lasting power for uninterrupted use"
            ],
            "action": "Order now and experience the difference. 30-day money-back guarantee!"
        },
        "es": {
            "title": f"Mejor {product['name']} 2024 | Calidad Premium",
            "meta_desc": f"Compra el mejor {product['name']}. Calidad garantizada. Envío gratis y garantía de devolución. ¡Ordene ahora!",
            "attention": f"¿Cansado de equipos poco confiables que fallan en el momento crucial?",
            "benefits": [
                "🏆 Rendimiento superior con tecnología de vanguardia",
                "🛡️ Construido para durar con materiales premium",
                "⚡ Carga rápida y batería de larga duración"
            ],
            "action": "Ordene ahora y experimente la diferencia. ¡Garantía de devolución de 30 días!"
        },
        "fr": {
            "title": f"Meilleur {product['name']} 2024 | Qualité Premium",
            "meta_desc": f"Achetez le meilleur {product['name']}. Qualité garantie. Livraison gratuite et garantie de retour. Commandez maintenant!",
            "attention": f"Fatigué des équipements peu fiables qui tombent en panne au moment crucial?",
            "benefits": [
                "🏆 Performance supérieure avec technologie de pointe",
                "🛡️ Conçu pour durer avec des matériaux premium",
                "⚡ Charge rapide et batterie longue durée"
            ],
            "action": "Commandez maintenant et ressentez la différence. Garantie de remboursement de 30 jours!"
        },
        "de": {
            "title": f"Bester {product['name']} 2024 | Premium Qualität",
            "meta_desc": f"Kaufen Sie den besten {product['name']}. Garantierte Qualität. Kostenloser Versand und Rückgabegarantie. Jetzt bestellen!",
            "attention": f"Müde von unzuverlässigen Geräten, die im entscheidenden Moment ausfallen?",
            "benefits": [
                "🏆 Überlegene Leistung mit modernster Technologie",
                "🛡️ Haltbarkeit durch Premium-Materialien",
                "⚡ Schnelles Laden und langlebiger Akku"
            ],
            "action": "Jetzt bestellen und den Unterschied spüren. 30 Tage Geld-zurück-Garantie!"
        },
        "ru": {
            "title": f"Лучший {product['name']} 2024 | Топ Качество",
            "meta_desc": f"Купите лучший {product['name']}. Премиум качество. Быстрая доставка. Гарантия возврата 30 дней!",
            "attention": f"Устали от ненадежного оборудования, которое выходит из строя в самый неподходящий момент?",
            "benefits": [
                "🏆 Превосходная производительность с передовыми технологиями",
                "🛡️ Построен на века с премиальными материалами",
                "⚡ Быстрая зарядка и долговечная батарея"
            ],
            "action": "Закажите сейчас и почувствуйте разницу. Гарантия возврата 30 дней!"
        },
        "ja": {
            "title": f"{product['name']} おすすめ 2024 | 高品質",
            "meta_desc": f"{product['name']}をおすすめします。品質保証、正規品、アフターサービス充実。今すぐチェック！",
            "attention": f"空気が汚くてアレルギーに悩んでいませんか？",
            "benefits": [
                "🏆 4段階浄化システム、H13 HEPA高効率フィルター",
                "🛡️ 航空機グレード素材、長持ちする品質",
                "⚡ ワイヤレスポータブル設計、どこでも清潔な空気"
            ],
            "action": "今すぐご注文ください。30日間返品保証付き！"
        },
        "ko": {
            "title": f"{product['name']} 추천 2024 | 고품질 정품",
            "meta_desc": f"{product['name']} 추천합니다. 품질보증, 정품, A/S 걱정없어요. 한정특가, 지금 구매하세요!",
            "attention": f"공기질이 안좋고 알레르기로 고민중이신가요?",
            "benefits": [
                "🏆 4단계 정화 시스템, H13 HEPA 고효율 필터",
                "🛡️ 항공기급 소재, 믿을수 있는 품질",
                "⚡ 무선 휴대용 디자인, 언제 어디서나 상쾌한 공기"
            ],
            "action": "지금 주문하세요. 30일 무조건 반품보장! 정품보증!"
        },
        "pt": {
            "title": f"Melhor {product['name']} 2024 | Qualidade Premium",
            "meta_desc": f"Compre o melhor {product['name']}. Qualidade garantida. Frete grátis e garantia de devolução. Peça agora!",
            "attention": f"Cansado de equipamentos não confiáveis que falham no momento crucial?",
            "benefits": [
                "🏆 Desempenho superior com tecnologia de ponta",
                "🛡️ Construído para durar com materiais premium",
                "⚡ Carregamento rápido e bateria de longa duração"
            ],
            "action": "Peça agora e sinta a diferença. Garantia de devolução de 30 dias!"
        },
        "ar": {
            "title": f"أفضل {product['name']} 2024 | جودة عالية",
            "meta_desc": f"اشترِ أفضل {product['name']}. جودة ممتازة. شحن مجاني. ضمان استرداد 30 يومًا!",
            "attention": f"هل سئمت من المعدات غير الموثوقة التي تفشل عندما تحتاجها most؟",
            "benefits": [
                "🏆 أداء فائق مع تكنولوجيا متطورة",
                "🛡️ بناء متين مع مواد عالية الجودة",
                "⚡ شحن سريع وبطارية طويلة الأمد"
            ],
            "action": "اطلب الآن واختبر الفرق. ضمان استرداد لمدة 30 يومًا!"
        },
        "zh": {
            "title": f"{product['name']} 推荐 2024 | 高品质正品",
            "meta_desc": f"推荐购买{product['name']}，品质保证，官方正品，售后无忧。限时优惠，立即抢购！",
            "attention": f"还在为空气质量差、过敏困扰而烦恼？",
            "benefits": [
                "🏆 四重净化系统，H13 HEPA高效过滤",
                "🛡️ 航空级材质，品质可靠经久耐用",
                "⚡ 无线便携设计，随时随地享受清新空气"
            ],
            "action": "立即下单，享受30天无理由退换！官方正品保证！"
        }
    }
    
    template = templates.get(lang, templates["en"])
    
    # Build specs table
    specs_table = "| Parameter | Details |\n|:----------|:--------|\n"
    for key, values in product["tech_specs"].items():
        # Handle both string values and tuple values from regex
        formatted_values = []
        for v in values:
            if isinstance(v, tuple):
                formatted_values.append(''.join(v))
            else:
                formatted_values.append(str(v))
        specs_table += f"| {key.capitalize()} | {', '.join(formatted_values)} |\n"
    
    if not product["tech_specs"]:
        specs_table += "| Product | " + product["name"] + " |\n"
    
    # Generate full markdown
    description = f"""### {lang_config['name']} - {template['title']}

**1. SEO Metadata**
* **Title Tag (Max 60 chars):** {template['title'][:60]}
* **Meta Description (Max 155 chars):** {template['meta_desc'][:155]}

**Keywords:** {', '.join(keywords)}

**2. Conversion Copy (AIDA)**

**[Attention]:** {template['attention']}

**[Interest/Desire]:**
* {template['benefits'][0]}
* {template['benefits'][1]}
* {template['benefits'][2]}

**[Action]:** {template['action']}

**3. Specifications Table**
{specs_table}

**4. Search Engine Strategy**
*Strategy for {lang_config['market']}:* {lang_config['strategy']}

*Localization Notes:*
- Optimized for local search patterns and user behavior
- Used culturally-appropriate terminology and expressions
- Adapted technical specifications to local standards

---
"""
    
    return description

def main():
    parser = argparse.ArgumentParser(description='Generate multilingual SEO product descriptions')
    parser.add_argument('--input', '-i', required=True, help='Product description text or file path')
    parser.add_argument('--languages', '-l', default='en,es,ru,ar', help='Comma-separated language codes')
    parser.add_argument('--output', '-o', default='./output', help='Output directory')
    parser.add_argument('--batch', '-b', action='store_true', help='Batch mode (input is CSV/MD file)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    languages = args.languages.split(',')
    
    if args.batch:
        # Batch processing mode
        print(f"Batch processing: {args.input}")
        # TODO: Implement CSV/MD parsing for batch mode
        print("Batch mode not yet implemented")
    else:
        # Single product mode
        input_text = args.input
        if Path(input_text).exists():
            with open(input_text, 'r', encoding='utf-8') as f:
                input_text = f.read()
        
        product = parse_product_input(input_text)
        
        print(f"Product: {product['name']}")
        print(f"Tech Specs: {product['tech_specs']}")
        print(f"Target: {product['target_audience']}")
        print("\n" + "="*60)
        
        for lang in languages:
            if lang not in LANGUAGES:
                print(f"Warning: Language '{lang}' not supported, skipping...")
                continue
            
            description = generate_description(product, lang)
            
            # Save to file
            output_file = output_dir / f"{lang}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(description)
            
            print(f"\nGenerated: {output_file}")
            # Safe print for Windows console
            try:
                print(description[:500] + "...")
            except UnicodeEncodeError:
                print("[Content generated successfully - non-ASCII characters in output]")
    
    print(f"\nDone! Output saved to: {output_dir}")

if __name__ == '__main__':
    main()