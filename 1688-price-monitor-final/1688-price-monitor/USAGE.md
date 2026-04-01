# 1688 价格监控技能 - 使用说明

## 📦 技能位置

```
~/.openclaw/workspace-hamburger/skills/1688-price-monitor/
```

## 🚀 快速开始

### 方法 1：在 OpenClaw 对话中使用（推荐）

直接告诉我：

```
帮我监控这个 1688 商品的价格：https://detail.1688.com/offer/XXX.html
```

我会：
1. 使用 browser 工具打开页面
2. 抓取价格信息
3. 保存到数据文件
4. 显示结果

### 方法 2：批量监控

1. 编辑 `config/monitored-products.json` 添加商品列表
2. 告诉我："批量监控 1688 商品价格"

### 方法 3：生成报告

告诉我："生成 1688 价格监控报告"

---

## 📁 文件结构

```
1688-price-monitor/
├── SKILL.md                      # 技能定义
├── monitor.py                    # 监控主程序
├── README.md                     # 简要说明
├── USAGE.md                      # 使用说明（本文件）
├── requirements.txt              # Python 依赖
├── config/
│   └── monitored-products.json   # 监控商品配置
└── data/
    └── price-history.csv         # 价格历史记录（自动生成）
```

---

## 🔧 配置说明

### config/monitored-products.json

```json
{
  "products": [
    {
      "id": "product-001",
      "name": "商品名称",
      "url": "https://detail.1688.com/offer/123456789.html",
      "target_price": 15.00,
      "currency": "CNY",
      "check_frequency": "daily",
      "notify_threshold": 10
    }
  ],
  "settings": {
    "browser": "chromium",
    "headed": false,
    "output_format": "csv"
  }
}
```

**字段说明：**
- `id`: 商品唯一标识
- `name`: 商品名称
- `url`: 1688 商品详情页链接
- `target_price`: 目标采购价
- `check_frequency`: 检查频率 (daily/weekly/monthly)
- `notify_threshold`: 价格变动通知阈值（百分比）

---

## 📊 输出数据格式

### price-history.csv

```csv
timestamp,url,product_name,price,price_range,min_order,supplier,change_percent
2026-04-01T10:00:00,https://...,示例商品，15.00,12.00-18.00,100,XX 公司，-5.2
```

---

## 🛠️ 常见问题

### Q: 浏览器无法打开页面？
A: 确保 Chrome 浏览器已安装，并且 OpenClaw 浏览器服务已启动

### Q: 价格抓取不到？
A: 1688 页面结构可能变化，需要调整选择器。查看 `monitor.py` 中的 `selectors` 配置

### Q: 需要登录才能看到价格？
A: 使用 Chrome 扩展的 profile 模式，可以复用你的登录状态

### Q: 如何设置定时监控？
A: 可以配置 OpenClaw 的 HEARTBEAT.md，每天定时执行监控任务

---

## 📈 进阶用法

### 1. 价格变化通知

在技能中添加消息通知功能：

```python
def notify_price_change(self, old_price: float, new_price: float):
    change = (new_price - old_price) / old_price * 100
    if abs(change) > self.notify_threshold:
        # 发送消息通知
        print(f"⚠️ 价格变化超过{self.notify_threshold}%: {change:+.1f}%")
```

### 2. 多平台对比

扩展技能支持 Temu、Amazon 等平台：

```python
def compare_prices(self, product_name: str):
    price_1688 = self.get_1688_price(product_name)
    price_temu = self.get_temu_price(product_name)
    price_amazon = self.get_amazon_price(product_name)
    
    return {
        "1688": price_1688,
        "temu": price_temu,
        "amazon": price_amazon,
        "best": min(price_1688, price_temu, price_amazon)
    }
```

### 3. 价格趋势图

使用 matplotlib 生成价格趋势图：

```python
import matplotlib.pyplot as plt

def plot_price_trend(self, product_id: str):
    df = pd.read_csv(self.data_path)
    product_df = df[df['product_id'] == product_id]
    
    plt.figure(figsize=(10, 6))
    plt.plot(product_df['timestamp'], product_df['price'])
    plt.title(f"价格趋势：{product_id}")
    plt.savefig(f"data/trend_{product_id}.png")
```

---

## 🎯 下一步

1. **添加商品** - 编辑 `config/monitored-products.json`
2. **测试监控** - 告诉我一个 1688 商品链接
3. **查看报告** - 运行 `python monitor.py report`

---

**版本:** 1.0.0  
**最后更新:** 2026-04-01
