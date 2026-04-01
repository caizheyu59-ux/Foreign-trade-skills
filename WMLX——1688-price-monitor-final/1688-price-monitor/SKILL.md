---
name: 1688-price-monitor
description: |
  1688 商品价格监控技能。使用 browser-use 或 web-access 自动抓取 1688 商品价格，监控价格变化并生成报告。
  
  适用场景：
  - 监控 1688 供应商价格变化
  - 批量抓取商品当前价格
  - 生成价格趋势报告
  - 竞品价格分析
  
  核心功能：
  1. monitor_price: 监控单个商品价格
  2. batch_monitor: 批量监控多个商品
  3. generate_report: 生成价格监控报告
  4. compare_prices: 对比不同供应商价格

compatibility: |
  依赖：browser-use CLI 或 web-access Skill
  前置条件：
  - 已安装 browser-use CLI (browser-use doctor 验证)
  - 或已配置 web-access Skill
  - 配置文件位于 ./config/monitored-products.json
---

# 1688 价格监控技能

## 快速开始

### 1. 前置准备

确保已安装 browser-use CLI：
```bash
browser-use doctor
```

### 2. 配置监控商品列表

在 `config/monitored-products.json` 中添加要监控的商品：

```json
{
  "products": [
    {
      "id": "product-001",
      "name": "示例商品",
      "url": "https://detail.1688.com/offer/123456789.html",
      "target_price": 15.00,
      "currency": "CNY",
      "check_frequency": "daily"
    }
  ]
}
```

### 3. 执行监控

```bash
# 监控单个商品
python monitor.py --url "https://detail.1688.com/offer/xxx.html"

# 批量监控
python monitor.py --batch

# 生成报告
python monitor.py --report
```

## 核心工作流

### Phase 1: 打开商品页面
使用 browser-use 打开 1688 商品详情页

### Phase 2: 抓取价格信息
- 提取当前价格
- 提取 SKU 价格区间
- 提取起订量
- 提取供应商信息

### Phase 3: 记录与对比
- 记录到本地数据库/CSV
- 对比历史价格
- 检测价格变化

### Phase 4: 生成报告
- 价格变化趋势
- 异常价格提醒
- 供应商对比分析

## 配置说明

### config/monitored-products.json

```json
{
  "products": [
    {
      "id": "唯一标识",
      "name": "商品名称",
      "url": "1688 商品链接",
      "target_price": 目标价格,
      "currency": "CNY",
      "check_frequency": "daily|weekly|monthly",
      "notify_threshold": 价格变动百分比阈值
    }
  ],
  "settings": {
    "browser": "chromium",
    "headed": false,
    "proxy": null,
    "output_format": "csv"
  }
}
```

## 输出格式

### CSV 报告
```
日期，商品 ID，商品名称，当前价格，原价，价格变化，供应商，URL
2026-04-01,product-001，示例商品，15.00,18.00,-16.7%,XX 公司，https://...
```

### JSON 数据
```json
{
  "timestamp": "2026-04-01T10:00:00Z",
  "product_id": "product-001",
  "current_price": 15.00,
  "original_price": 18.00,
  "change_percent": -16.7,
  "supplier": "XX 公司",
  "url": "https://..."
}
```

## 注意事项

1. **1688 反爬**: 建议设置合理的请求间隔，避免被封 IP
2. **登录状态**: 部分价格需要登录后可见，可使用 browser-use 的 profile 模式
3. **SKU 复杂度**: 1688 商品可能有多个 SKU 价格，需明确抓取规则
4. **数据准确性**: 建议定期人工核对关键商品价格

## 扩展功能

- [ ] 邮件/消息通知价格变化
- [ ] 价格趋势图表生成
- [ ] 多平台价格对比（1688 vs Temu vs Amazon）
- [ ] 自动采购建议

---

**版本:** 1.0.0
**最后更新:** 2026-04-01
