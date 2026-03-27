#!/usr/bin/env python3
"""
WMLX-Multilingual-Product-SEO 使用示例
Example usage of WMLX-Multilingual-Product-SEO
"""

import subprocess
import sys
from pathlib import Path

def example_single_product():
    """示例 1：单产品生成"""
    print("=" * 60)
    print("示例 1：单产品生成 (Single Product)")
    print("=" * 60)
    
    product = """AirNest Smart Air Purifier, 4-stage purification H13 HEPA activated carbon 
negative ions, intelligent monitoring auto mode, wireless portable, App control, 
ambient light. 5200mAh battery 4-12 hours, size 185x280mm, weight 1.6kg, 
aluminum alloy ABS, coverage 5-20 sqm, noise 25-52dB"""
    
    cmd = [
        sys.executable,
        "scripts/generate_descriptions.py",
        "-i", product,
        "-o", "./example-output",
        "-l", "en,es,fr,de,ru,ja,ko,pt,ar,zh"
    ]
    
    print(f"命令: {' '.join(cmd)}")
    print(f"产品: {product[:80]}...")
    print()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
    print("✅ 完成！输出目录: ./example-output")
    print()

def example_batch_processing():
    """示例 2：批量处理"""
    print("=" * 60)
    print("示例 2：批量处理 (Batch Processing)")
    print("=" * 60)
    
    cmd = [
        sys.executable,
        "scripts/batch_processor.py",
        "assets/example-input.csv",
        "-o", "./example-batch-output",
        "-l", "en,es,fr,de,ru,ja,ko,pt,ar,zh"
    ]
    
    print(f"命令: {' '.join(cmd)}")
    print(f"输入文件: assets/example-input.csv")
    print()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
    print("✅ 完成！输出目录: ./example-batch-output")
    print()

def example_custom_languages():
    """示例 3：指定语言"""
    print("=" * 60)
    print("示例 3：指定语言 (Custom Languages)")
    print("=" * 60)
    
    product = "Solar Camping Lantern, 5000mAh battery, IP65 waterproof, foldable"
    
    cmd = [
        sys.executable,
        "scripts/generate_descriptions.py",
        "-i", product,
        "-o", "./example-custom-output",
        "-l", "en,fr,ja,zh"  # 只生成英语、法语、日语、中文
    ]
    
    print(f"命令: {' '.join(cmd)}")
    print(f"产品: {product}")
    print(f"语言: en,fr,ja,zh")
    print()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
    print("✅ 完成！输出目录: ./example-custom-output")
    print()

def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "WMLX-Multilingual-Product-SEO" + " " * 17 + "║")
    print("║" + " " * 12 + "使用示例 / Usage Examples" + " " * 19 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # 检查脚本是否存在
    if not Path("scripts/generate_descriptions.py").exists():
        print("错误: 请先进入项目目录")
        print("Error: Please navigate to the project directory first")
        return
    
    # 运行示例
    example_single_product()
    example_batch_processing()
    example_custom_languages()
    
    print("=" * 60)
    print("所有示例完成！/ All examples completed!")
    print("=" * 60)
    print()
    print("可用语言代码 / Available language codes:")
    print("  en: English (英语)")
    print("  es: Spanish (西班牙语)")
    print("  fr: French (法语)")
    print("  de: German (德语)")
    print("  ru: Russian (俄语)")
    print("  ja: Japanese (日语)")
    print("  ko: Korean (韩语)")
    print("  pt: Portuguese (葡萄牙语)")
    print("  ar: Arabic (阿拉伯语)")
    print("  zh: Chinese (中文)")

if __name__ == "__main__":
    main()
