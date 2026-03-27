#!/usr/bin/env python3
"""
Batch processor for multilingual SEO product descriptions.
Reads CSV or Markdown files and generates descriptions for all products.
"""

import argparse
import csv
import os
import re
from pathlib import Path

from generate_descriptions import parse_product_input, generate_description, LANGUAGES


def parse_csv_file(filepath):
    """Parse CSV file and return list of products."""
    products = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = {
                "name": row.get("name", ""),
                "description": row.get("description", ""),
                "category": row.get("category", ""),
                "raw_input": f"Product: {row.get('name', '')}. {row.get('description', '')}"
            }
            products.append(product)
    return products


def parse_md_file(filepath):
    """Parse Markdown file with product list."""
    products = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by product entries (assuming ## or - Product: format)
    entries = re.split(r'\n## |\n- \[.*?\]|\n\n(?=Product:)', content)
    
    for entry in entries:
        entry = entry.strip()
        if not entry or len(entry) < 10:
            continue
        
        # Clean up entry
        if entry.startswith("Product:"):
            entry = entry[8:].strip()
        
        products.append({
            "raw_input": entry,
            "name": entry.split('.')[0][:50] if '.' in entry else entry[:50]
        })
    
    return products


def create_product_folder(base_dir, product_name):
    """Create sanitized folder name for product."""
    # Sanitize folder name
    safe_name = re.sub(r'[^\w\s-]', '', product_name).strip()
    safe_name = re.sub(r'[-\s]+', '-', safe_name)
    safe_name = safe_name[:50]  # Limit length
    
    folder_path = Path(base_dir) / safe_name
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def main():
    parser = argparse.ArgumentParser(description='Batch process products for multilingual SEO descriptions')
    parser.add_argument('input_file', help='Input CSV or Markdown file')
    parser.add_argument('--output', '-o', default='./output', help='Output directory')
    parser.add_argument('--languages', '-l', default='en,es,ru,ar', help='Comma-separated language codes')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1
    
    # Detect file type and parse
    if input_path.suffix.lower() == '.csv':
        products = parse_csv_file(input_path)
    elif input_path.suffix.lower() in ['.md', '.markdown', '.txt']:
        products = parse_md_file(input_path)
    else:
        print(f"Error: Unsupported file type: {input_path.suffix}")
        print("Supported: .csv, .md, .markdown, .txt")
        return 1
    
    print(f"Found {len(products)} products in {input_path}")
    
    languages = args.languages.split(',')
    output_base = Path(args.output)
    output_base.mkdir(parents=True, exist_ok=True)
    
    # Process each product
    for i, product_data in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}] Processing: {product_data.get('name', 'Unknown')[:40]}...")
        
        # Parse product details
        product = parse_product_input(product_data['raw_input'])
        if not product['name']:
            product['name'] = product_data.get('name', f'Product-{i}')
        
        # Create product folder
        product_folder = create_product_folder(output_base, product['name'])
        
        # Generate descriptions for each language
        for lang in languages:
            if lang not in LANGUAGES:
                continue
            
            try:
                description = generate_description(product, lang)
                output_file = product_folder / f"{lang}.md"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(description)
                
                print(f"  [OK] {LANGUAGES[lang]['name']}")
            except Exception as e:
                print(f"  [ERR] {LANGUAGES[lang]['name']}: {e}")
        
        print(f"  Saved to: {product_folder}")
    
    print(f"\nBatch complete! {len(products)} products processed.")
    print(f"Output: {output_base.absolute()}")
    return 0


if __name__ == '__main__':
    exit(main())
