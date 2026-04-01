# 1688 价格监控 - 快速开始

## ✅ 已验证的工作流

### 方法 1：使用 Node.js 脚本（推荐）

**前置条件：**
- Node.js 18+
- OpenClaw 浏览器已启动

**步骤：**

1. **安装依赖**
```bash
cd skills/1688-price-monitor
npm install ws
```

2. **打开 1688 商品页面**

在 OpenClaw 中执行：
```
browser.open https://detail.1688.com/offer/633830968371.html
```

或使用 browser 工具打开页面。

3. **获取页面 targetId**
```bash
curl -s http://127.0.0.1:18800/json/list
```

找到对应的页面 ID（如 `E8C471022EE3436066517E1737A63A36`）

4. **执行价格抓取**
```bash
node fetch-price.js <targetId>
```

**示例：**
```bash
node fetch-price.js E8C471022EE3436066517E1737A63A36
```

**输出：**
```
🔗 Connected to CDP

📊 1688 商品价格信息
============================================================
📦 商品标题：东莞市谜丽饰品有限公司
💰 价格：¥50.5
📈 价格区间：N/A
📋 最小起订：N/A
🏭 供应商：N/A
============================================================

💾 已保存到：data/price-history.csv
```

---

### 方法 2：在 OpenClaw 对话中使用

直接告诉我：
```
帮我监控这个 1688 商品的价格：https://detail.1688.com/offer/XXX.html
```

我会：
1. 用 browser 工具打开页面
2. 获取 targetId
3. 执行 fetch-price.js 抓取价格
4. 显示结果并保存

---

### 方法 3：批量监控

1. 编辑 `config/monitored-products.json` 添加商品列表
2. 运行批量脚本：

```bash
node batch-monitor.js
```

---

## 📁 输出文件

### data/price-history.csv

```csv
timestamp,target_id,product_name,price,price_range,min_order,supplier
2026-04-01T07:49:20.408Z,E8C471022EE3436066517E1737A63A36,"商品名称",50.5,"","",""
```

---

## 🔧 故障排除

### 问题 1：无法连接 CDP

**错误：** `WebSocket error: connect ECONNREFUSED`

**解决：**
1. 确保 OpenClaw 浏览器已启动
2. 检查 CDP 端口：`curl http://127.0.0.1:18800/json/list`
3. 重启浏览器：`browser.stop` 然后 `browser.start`

### 问题 2：价格为空

**原因：** 1688 页面结构可能变化，或需要登录

**解决：**
1. 检查页面是否需要登录
2. 使用 Chrome 扩展模式（profile="chrome"）
3. 更新 `fetch-price.js` 中的选择器

### 问题 3：npm 安装失败

**错误：** `Cannot find module 'ws'`

**解决：**
```bash
cd skills/1688-price-monitor
npm install ws
```

---

## 📊 测试案例

**商品链接：** https://detail.1688.com/offer/633830968371.html

**抓取结果：**
- 商品：东莞市谜丽饰品有限公司
- 价格：¥50.5
- 时间：2026-04-01 15:49

---

**版本:** 1.0.0  
**最后测试:** 2026-04-01
