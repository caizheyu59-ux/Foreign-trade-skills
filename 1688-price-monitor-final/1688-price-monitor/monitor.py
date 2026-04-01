#!/usr/bin/env python3
"""
1688 价格监控主程序
使用 OpenClaw browser 工具抓取 1688 商品价格

使用方法：
1. 作为 OpenClaw skill 调用
2. 或通过 browser 工具直接操作
"""

import json
import csv
from datetime import datetime
from pathlib import Path


class PriceMonitor:
    """1688 价格监控类"""
    
    def __init__(self):
        self.config_path = Path(__file__).parent / "config" / "monitored-products.json"
        self.data_path = Path(__file__).parent / "data" / "price-history.csv"
        self.data_path.parent.mkdir(exist_ok=True)
        
        # 1688 价格元素选择器（可能需要根据实际页面调整）
        self.selectors = {
            "price": ".price-title, .offer-price, [data-price]",
            "price_range": ".price-range, .sku-price",
            "min_order": ".min-order, .moq",
            "supplier": ".supplier-name, .company-name",
            "product_name": ".title, .product-name, h1"
        }
    
    def extract_price_from_snapshot(self, snapshot: dict) -> dict:
        """
        从页面快照中提取价格信息
        
        Args:
            snapshot: browser.snapshot 返回的页面状态
            
        Returns:
            价格信息字典
        """
        price_info = {
            "timestamp": datetime.now().isoformat(),
            "price": None,
            "price_range": None,
            "min_order": None,
            "supplier": None,
            "product_name": None
        }
        
        # 从 snapshot 中查找价格相关元素
        # snapshot 格式：{ "children": [...], "ref": "aria-xxx" }
        
        if "children" in snapshot:
            for child in snapshot["children"]:
                text = child.get("text", "").strip()
                role = child.get("role", "")
                name = child.get("name", "")
                
                # 尝试匹配价格
                if "price" in text.lower() or "¥" in text or "￥" in text:
                    price_info["price"] = self._parse_price(text)
                
                # 尝试匹配商品名称
                if role == "heading" or "title" in name.lower():
                    price_info["product_name"] = text[:100]
        
        return price_info
    
    def _parse_price(self, text: str) -> float:
        """从文本中解析价格数字"""
        import re
        # 匹配价格模式：¥15.00, ￥15.00, 15.00 元
        match = re.search(r'[¥￥]?\s*(\d+\.?\d*)\s*元?', text)
        if match:
            return float(match.group(1))
        return None
    
    def save_price_record(self, price_info: dict, url: str = ""):
        """保存价格记录到 CSV"""
        file_exists = self.data_path.exists()
        
        with open(self.data_path, "a", newline="", encoding="utf-8") as f:
            fieldnames = ["timestamp", "url", "product_name", "price", "price_range", 
                         "min_order", "supplier", "change_percent"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({**price_info, "url": url})
        
        print(f"💾 已保存到：{self.data_path}")
    
    def display_price_info(self, price_info: dict):
        """显示价格信息"""
        print("\n" + "="*60)
        print("📊 价格信息")
        print("="*60)
        print(f"商品名称：{price_info.get('product_name', 'N/A')}")
        print(f"当前价格：¥{price_info.get('price', 'N/A')}")
        print(f"价格区间：{price_info.get('price_range', 'N/A')}")
        print(f"最小起订：{price_info.get('min_order', 'N/A')}")
        print(f"供应商：{price_info.get('supplier', 'N/A')}")
        print(f"抓取时间：{price_info.get('timestamp', 'N/A')}")
        print("="*60 + "\n")
    
    def load_config(self) -> dict:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"products": [], "settings": {}}


# ============== OpenClaw Skill 入口 ==============

def monitor_price(url: str, name: str = None) -> dict:
    """
    监控单个商品价格
    
    Args:
        url: 1688 商品详情页 URL
        name: 商品名称（可选）
        
    Returns:
        价格信息字典
    """
    print(f"\n🔍 开始监控：{name or url}")
    print(f"URL: {url}\n")
    
    monitor = PriceMonitor()
    
    # 这里需要配合 browser 工具使用
    # 1. 先用 browser.open 打开页面
    # 2. 用 browser.snapshot 获取页面状态
    # 3. 用 extract_price_from_snapshot 提取价格
    
    # 示例流程（需要在 OpenClaw 中执行）：
    # browser.open(url) → browser.snapshot() → extract_price_from_snapshot()
    
    return {
        "status": "ready",
        "message": "请使用 browser 工具打开页面后调用 extract 方法",
        "url": url
    }


def batch_monitor(product_ids: list = None) -> list:
    """
    批量监控商品价格
    
    Args:
        product_ids: 商品 ID 列表，或从配置文件读取
        
    Returns:
        价格信息列表
    """
    monitor = PriceMonitor()
    config = monitor.load_config()
    
    products = product_ids or config.get("products", [])
    
    if not products:
        print("❌ 没有配置要监控的商品")
        return []
    
    print(f"📦 批量监控 {len(products)} 个商品\n")
    
    results = []
    for i, product in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}] {product.get('name', '未知商品')}")
        # result = monitor_price(product["url"], product.get("name"))
        # results.append(result)
    
    return results


def generate_report(days: int = 7) -> str:
    """
    生成价格监控报告
    
    Args:
        days: 报告天数
        
    Returns:
        报告文本
    """
    monitor = PriceMonitor()
    
    if not monitor.data_path.exists():
        return "暂无价格数据"
    
    # 读取 CSV 生成报告
    import pandas as pd
    df = pd.read_csv(monitor.data_path)
    
    report = f"\n{'='*60}\n"
    report += f"📈 1688 价格监控报告（过去{days}天）\n"
    report += f"{'='*60}\n\n"
    
    report += f"总记录数：{len(df)}\n"
    report += f"监控商品数：{df['product_name'].nunique()}\n\n"
    
    # 按商品分组统计
    for name, group in df.groupby("product_name"):
        report += f"📦 {name}\n"
        if len(group) > 1:
            price_change = group["price"].iloc[-1] - group["price"].iloc[0]
            change_pct = (price_change / group["price"].iloc[0]) * 100 if group["price"].iloc[0] else 0
            report += f"   当前价格：¥{group['price'].iloc[-1]:.2f}\n"
            report += f"   价格变化：{change_pct:+.1f}%\n"
        else:
            report += f"   当前价格：¥{group['price'].iloc[0]:.2f}\n"
        report += "\n"
    
    report += f"{'='*60}\n"
    
    return report


# CLI 入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python monitor.py <command> [args]")
        print("\n命令:")
        print("  monitor <url> [name]  - 监控单个商品")
        print("  batch                 - 批量监控")
        print("  report [days]         - 生成报告")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "monitor" and len(sys.argv) >= 3:
        url = sys.argv[2]
        name = sys.argv[3] if len(sys.argv) > 3 else None
        result = monitor_price(url, name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "batch":
        results = batch_monitor()
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif command == "report":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        report = generate_report(days)
        print(report)
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
