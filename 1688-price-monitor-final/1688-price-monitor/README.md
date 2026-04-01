# 1688 价格监控技能

自动监控 1688 商品价格变化，生成价格趋势报告。

## 安装

```bash
cd 1688-price-monitor
pip install -r requirements.txt
```

## 配置

编辑 `config/monitored-products.json`，添加要监控的商品：

```json
{
  "products": [
    {
      "id": "product-001",
      "name": "商品名称",
      "url": "https://detail.1688.com/offer/123456789.html",
      "target_price": 15.00,
      "check_frequency": "daily"
    }
  ]
}
```

## 使用

### 监控单个商品

```bash
python monitor.py --url "https://detail.1688.com/offer/xxx.html" --name "商品名称"
```

### 批量监控

```bash
python monitor.py --batch
```

### 生成报告

```bash
python monitor.py --report --days 7
```

### 显示浏览器窗口（调试用）

```bash
python monitor.py --url "https://..." --headed
```

## 输出

价格数据保存在 `data/price-history.csv`

## 依赖

- browser-use CLI
- Python 3.10+
