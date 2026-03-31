---
name: dg-1688
description: |
  1688 抓取规则包（DG 客户专用）。输入店铺链接或商品详情链接，按固定 DOM 规则提取 SKU 维度的图片、名称、价格，
  配合美元/人民币汇率与 0.65 / 0.7 两套报价系数，输出与 dg-template 一致的公司介绍区 + 表格数据。
  
  核心特性：
  - 横向 3 列布局（每行展示 3 个产品）
  - 产品名称加序号（避免重名，如 DG-A641-01）
  - 支持分离式 SKU 结构（颜色/尺码分开在不同区域）
  - 支持标准 SKU 结构（expand-view-item 列表）
  
  触发词：dg-1688、1688 DG 规则、生成 1688 报价单

compatibility: |
  依赖：浏览器自动化（web-access / CDP / Playwright 等）支持 evaluate 执行 JS；
  汇率可用手动填写或调用公开 API；Excel 生成配合 xlsxwriter。

---

# DG-1688 抓取规则包

本规则与 `dg-template.numbers`（公司介绍与版式参考）对齐；**公司介绍文案与排版以该模板为准**，抓取阶段只负责结构化字段与公式约定。

## 1. 输入类型

| 类型 | 示例特征 | 处理流程 |
| :--- | :--- | :--- |
| **商品详情页** | URL 含 `detail.1688.com/offer/…` 或 `…1688.com/offer/…` | 打开该页 → 等待 `#skuSelection` 渲染 → 执行提取脚本 |
| **店铺页** | 店铺域名 + `offerlist`、全部商品等 | 先按店铺列表抓取每条商品详情链接 → **对每个详情页重复**「商品详情页」流程 → 合并为多行（每 SKU 一行） |

## 2. 调用方式

### Python 直接调用

```python
from rules.dg_1688.build_quote_from_detail import build_quote

# 方式 1：使用默认汇率
output = build_quote("https://detail.1688.com/offer/xxx.html")
print(output)  # ./output/dg1688_template_quote_xxx.xlsx

# 方式 2：指定汇率
output = build_quote("https://detail.1688.com/offer/xxx.html", fx=7.2)
```

### 命令行调用

```bash
cd price-list-generator
python -c "from rules.dg_1688.build_quote_from_detail import build_quote; print(build_quote('https://detail.1688.com/offer/xxx.html'))"
```

## 3. 详情页 DOM 锚点（必须）

本规则支持两种 SKU 页面结构：

### 结构 A：标准 SKU 列表（expand-view-item）

**容器：**
```
#skuSelection .module-od-sku-selection.cart-gap
  └─ .expand-view-list-wrapper
      └─ .expand-view-item (每个规格一行)
```

### 结构 B：分离式 SKU（颜色/尺码分开）

**容器：**
```
#skuSelection .module-od-sku-selection.cart-gap
  ├─ .feature-item（颜色区）
  │   └─ .sku-filter-button（颜色按钮）
  │       ├─ img（颜色图片）
  │       └─ .label-name（颜色名称）
  └─ .feature-item（尺码区）
      └─ .expand-view-item（尺码行）
          ├─ .item-label（尺码名称）
          └─ .item-price-stock（价格）
```

### ⚠️ 重要：SKU 图片匹配规则（2026-03-31 更新）

**问题：** 1688 页面默认只显示 1 个 SKU 的主图，其他 SKU 的图片需要点击切换后才能获取。

**错误做法：**
- ❌ 直接从 SKU 块内的 `img` 提取（那是缩略图，不是产品主图）
- ❌ 只读取当前页面显示的 #gallery 图片（只会得到第 1 个 SKU 的图）
- ❌ 使用 `#gallery > div > div.od-gallery-preview > div.od-gallery-list-wapper > ul > li > div > img`（这个选择器在某些页面返回空）

**正确做法：**
1. ✅ 读取所有 SKU 列表（名称、价格）
2. ✅ **逐个点击每个 SKU 选项**
3. ✅ 点击后**立即从 `#gallery img.preview-img` 读取主图**
4. ✅ 将 SKU 名称与对应图片绑定
5. ✅ 等待 200ms 让主图切换完成

**代码示例：**
```javascript
// 点击 SKU
block.click();
// 等待主图切换
await sleep(200);
// 从 #gallery 读取主图（关键！）
const img = document.querySelector('#gallery img.preview-img') || 
            document.querySelector('#gallery img');
const imageUrl = img ? (img.getAttribute('data-src') || img.src) : '';
```

**审计结论：**
- 部分页面 gallery 不在 cart-gap 容器内，图片**必须从页面级 #gallery 读取**
- 必须使用 `#gallery img.preview-img` 或 `#gallery img` 选择器
- 禁止使用 SKU 块内的 img（那是缩略图，不是产品图）

### 抓全规格（强制要求）

- **目标不是"抓到一行"，而是"抓到该产品所有规格行"。**
- 当容器只返回 0/1 行，必须执行兜底策略：
  1. 优先尝试分离式提取（`extract_sku_separated.js`）
  2. 从页面文本中批量解析"规格名 + 价格 + 库存"
  3. 以解析出的全部规格行为最终结果
- 任何详情页最终输出 `count` 必须等于该商品页面可见规格总数（允许因平台折叠导致轻微偏差，但不得只返回单行占位）

## 4. 提取字段

### 单块提取字段（按优先级）

| 字段 | 选择器 | 说明 |
| :--- | :--- | :--- |
| 图片 URL | `.sku-filter-button img` 或 `.expand-view-item .item-image-icon img` | 必须去掉 `_sum` 后缀还原为原图 URL |
| 名称 | `.label-name` 或 `.item-label` | 与图同一 SKU 块内；去首尾空白 |
| 价格 | `.item-price-stock` 或 `*[class*="price"]` | 解析为数字（元，CNY） |

### 产品名称处理

1. **提取编号**：从原始名称提取字母+数字组合
   - 例：`A641-钢色大号戒指-6号` → `A641`
2. **添加前缀**：`DG-{编号}`
   - 例：`DG-A641`
3. **添加序号**：避免重名，`{全局序号}`（01, 02, 03...）
   - 最终名称：`DG-A641-01`

### 价格计算

**CNY → USD 转换：**
```
USD = CNY / 0.65 / 7
结果保留 2 位小数，四舍五入
```

例：
- CNY 14.00 → USD 3.08
- CNY 15.50 → USD 3.41

## 5. 输出表结构

### 横向 3 列布局

```
第1行（图片行）:  [图片1] [链接1] [空] [图片2] [链接2] [空] [图片3] [链接3] [空]
第2行（数据行）:  [名称] [CNY] [USD] [名称] [CNY] [USD] [名称] [CNY] [USD]
```

**列定义（9列）：**

| 列 | 宽度 | 用途 |
| :--- | :--- | :--- |
| A | 18 | 图片1 |
| B | 10 | 链接1 / 数据行 CNY1（缩减）|
| C | 14 | 空1 / 数据行 USD1（加宽，绿色加粗 $）|
| D | 18 | 图片2 |
| E | 10 | 链接2 / CNY2 |
| F | 14 | 空2 / USD2 |
| G | 18 | 图片3 |
| H | 10 | 链接3 / CNY3 |
| I | 14 | 空3 / USD3 |

**公司介绍区（前 7 行）：**

| 行 | 左侧（A-C列） | 右侧（D-I列） |
| :--- | :--- | :--- |
| 1 | **DongGuan DG Jewelry Co,.Ltd**（深蓝底白字，全宽） | |
| 2 | （空白） | **Charms** |
| 3 | W: www.dgjewelry.cn | |
| 4 | P : +86 186 8869 1502 | 合并单元格显示完整描述 |
| 5 | E: sparrow@dgjewelry.cn | |
| 6 | Contact us for more Collection | （空白） |
| 7 | **Stainless steel Charms**（大标题，全宽） | |

## 5. 输出表结构

### 横向 3 列布局

```
第 1 行（图片行）:  [图片 1] [链接 1] [空] [图片 2] [链接 2] [空] [图片 3] [链接 3] [空]
第 2 行（数据行）:  [名称] [CNY] [USD] [名称] [CNY] [USD] [名称] [CNY] [USD]
```

**列定义（9 列）：**

| 列 | 宽度 | 用途 |
| :--- | :--- | :--- |
| A | 18 | 图片 1 |
| B | 10 | 链接 1 / 数据行 CNY1（缩减）|
| C | 14 | 空 1 / 数据行 USD1（加宽，绿色加粗 $）|
| D | 18 | 图片 2 |
| E | 10 | 链接 2 / CNY2 |
| F | 14 | 空 2 / USD2 |
| G | 18 | 图片 3 |
| H | 10 | 链接 3 / CNY3 |
| I | 14 | 空 3 / USD3 |

**公司介绍区（前 7 行）：**

| 行 | 左侧（A-C 列） | 右侧（D-I 列） |
| :--- | :--- | :--- |
| 1 | **DongGuan DG Jewelry Co,.Ltd**（深蓝底白字，全宽） | |
| 2 | （空白） | **Charms** |
| 3 | W: www.dgjewelry.cn | |
| 4 | P : +86 186 8869 1502 | 合并单元格显示完整描述 |
| 5 | E: sparrow@dgjewelry.cn | |
| 6 | Contact us for more Collection | （空白） |
| 7 | **Stainless steel Charms**（大标题，全宽） | |

**图片处理：**
- 顶部裁剪 100px（去除编码水印）
- 等比例缩放适配单元格
- 高清原图（去掉 `_sum` 后缀）

**1688 链接（强制要求）：**
- ✅ 每个产品必须在图片行添加 1688 链接
- ✅ 链接位置：B/E/H 列（图片右侧）
- ✅ 链接文本："1688 Link"（蓝色下划线）
- ✅ 链接目标：商品详情页 URL
- ❌ 禁止遗漏链接

## 6. 浏览器内一键提取（eval）

### 标准提取脚本

将同目录下 `extract_sku_selection.js` 在详情页执行，返回：
```json
{
  "pageUrl": "https://detail.1688.com/offer/xxx.html",
  "title": "商品标题",
  "count": 9,
  "items": [
    {
      "imageUrl": "https://cbu01.alicdn.com/img/ibank/xxx.jpg",
      "name": "F1714-间金耳环-17mm",
      "priceCny": 14.0,
      "link": "https://detail.1688.com/offer/xxx.html"
    }
  ],
  "source": "strict"
}
```

### 分离式提取脚本

将 `extract_sku_separated.js` 在详情页执行，自动检测颜色/尺码分离结构，执行笛卡尔积组合。

返回：
```json
{
  "pageUrl": "https://detail.1688.com/offer/xxx.html",
  "title": "商品标题",
  "count": 12,
  "items": [...],
  "source": "separated_color_size",
  "colorsCount": 4,
  "sizesCount": 3
}
```

## 7. 图片高清化规则（强制）

- 若图片 URL 包含 `"_sum"`（例如 `xxx.jpg_sum.jpg`），必须去掉 `_sum`，还原为 `xxx.jpg`
- 若图片 URL 结尾为 `".jpg_.webp"` / `".png_.webp"` / `".jpeg_.webp"`，必须回退为原始 `jpg/png/jpeg`
- 最终写入报价单的图片链接必须是"高清原图链接"
- 写入 Excel 时**禁止压缩图片文件像素**；仅允许在 Excel 插入参数中做显示缩放
- 图片写入前必须先裁掉顶部 `100px`（去除编码水印区）

## 8. 与 price-list-generator 的衔接

- 抓取：使用 web-access（CDP 代理）导航 + eval
- Excel 生成：使用 xlsxwriter，直接写入公式和格式
- 输出路径：`./output/dg1688_template_quote_{timestamp}.xlsx`

## 9. 错误处理

| 场景 | 处理 |
| :--- | :--- |
| 页面无 SKU 数据 | 返回错误提示 |
| 图片下载失败 | 显示 "No Image" 占位符，继续生成 |
| 分离式结构检测失败 | 自动回退到标准提取 |
| 汇率参数缺失 | 使用默认值 7.0 |

## 10. 变更记录

| 版本 | 说明 |
| :--- | :--- |
| 1.0 | 初版：标准 SKU 提取、expand-view-item 选择器、汇率含义 |
| 1.1 | 新增：横向 3 列布局、产品名称加序号（DG-XXX-01）|
| 1.2 | 新增：分离式 SKU 结构支持（颜色/尺码笛卡尔积）|
| 1.3 | 新增：店铺筛选抓取实施步骤、自动化评估与半自动执行标准流程 |
| 1.4 | 新增：SKU 图片匹配规则（逐个点击获取）、产品名称格式改为 DG-{店铺缩写}-{序号}、强制要求 1688 链接 |

## 11. 店铺筛选抓取实施步骤（已验证）

适用场景：先从店铺页按条件筛出商品列表，再逐个进入详情页抓规格。

### 目标示例

- 店铺：`https://milishipin.1688.com/page/offerlist.htm?...`
- 筛选：`2026 新款` + `3月 上新`
- 输出：仅列表字段（产品名、价格、详情链接），**不生成报价单**

### 执行步骤（SOP）

1. 启动前检查（必须）  
   - 执行 `check-deps.sh`，确认 Node/Chrome/CDP Proxy 可用。

2. 打开店铺页并定位筛选项  
   - 在页面中先 `eval` 检查是否存在文本：`2026 新款`、`3月 上新`。
   - 再通过点击叶子节点触发筛选（禁止直接拼 URL 假设已筛选）。

3. 筛选态验证  
   - 校验页面文本包含筛选面包屑（如 `2026 新款 > 3月 上新`）。
   - 校验分页信息（如 `1/4`），用于后续翻页终止条件。

4. 抓取当前页商品列表（推荐 Fiber 方案）  
   - 使用 `img.main-picture` + React Fiber 回溯 `props.data` 提取：
     - `id`（用于拼接详情页链接）
     - `title`
     - `price`
   - 详情链接规范化：`https://detail.1688.com/offer/{id}.html`

5. 点击“下一页”并翻页抓取  
   - 必须通过页面按钮点击翻页（`下一页`），不可直接假设 `pageNum` 可用。
   - 每页做去重（按 `id`）。
   - 终止条件：
     - 下一页按钮不存在/disabled
     - 页码达到末页（如 `4/4`）
     - 出现验证码拦截

6. 输出列表供人工确认  
   - 输出 JSON 到 `tmp/`（如 `tmp/milishipin_2026_3month_products.json`）。
   - 字段固定：`name`, `priceCny`, `link`。

7. 列表确认后再进入下一步  
   - 才执行“逐个详情页抓规格（标准/分离式）→ 生成报价单”。

## 12. 自动化评估（可行性与边界）

### 结论

- **可以做成自动化，但建议采用“半自动 + 断点续跑”模式。**
- 原因：1688 风控（滑块验证码）无法稳定全自动绕过，需保留人工验证检查点。

### 可自动化比例（经验值）

- 无验证码时：约 90%+ 流程可自动完成（筛选、翻页、提取、去重、落盘）。
- 遇验证码时：自动流程需暂停，人工过验证后继续（恢复后可继续自动跑）。

### 自动化难点

1. 风控不确定性  
   - 同一流程在不同时间/频率下触发验证码概率不同。

2. DOM 结构动态变化  
   - 店铺列表页常见动态渲染，纯 CSS 选择器稳定性一般。
   - Fiber 提取更稳，但依赖前端实现细节，需保留回退路径。

3. 筛选状态不总是体现在 URL  
   - 不能只看 URL，必须用页面文本/分页信息做状态校验。

### 推荐自动化形态（生产可用）

1. **阶段 A：列表抓取器（可独立运行）**
   - 输入：店铺 URL + 筛选文本（一级/二级）
   - 输出：`tmp/{shop}_{filter}_products.json`
   - 内置：验证码检测、分页抓取、去重、断点保存

2. **阶段 B：规格抓取器**
   - 输入：阶段 A 的产品链接列表
   - 输出：规格明细 JSON（支持标准/分离式结构）

3. **阶段 C：报价生成器**
   - 输入：规格明细 JSON
   - 输出：Excel 报价单

### 已落地脚本（可直接运行）

`rules/dg-1688/scripts/run_shop_filter_pipeline.py`  
功能：店铺筛选列表抓取（点击筛选 + 翻页 + 断点续跑）

示例：

```bash
cd price-list-generator
./venv/bin/python rules/dg-1688/scripts/run_shop_filter_pipeline.py \
  --shop-url "https://milishipin.1688.com/page/offerlist.htm?spm=a2615.7691456.wp_pc_common_topnav.0" \
  --first-filter "2026 新款" \
  --second-filter "3月 上新" \
  --output "./tmp/milishipin_2026_3month_products.json"
```

若中途出现验证码，人工验证后续跑：

```bash
./venv/bin/python rules/dg-1688/scripts/run_shop_filter_pipeline.py \
  --shop-url "https://milishipin.1688.com/page/offerlist.htm?spm=a2615.7691456.wp_pc_common_topnav.0" \
  --resume
```

### 验证码处理规范（必须）

- 检测到验证码时：
  - 立即停止当前批次并保存已抓结果；
  - 输出明确提示“请人工过验证后继续”；
  - 支持从上次页码/最后商品 ID 恢复执行。

### 成功标准（店铺筛选模式）

- 筛选条件命中（页面文本可验证）；
- 列表总数与分页覆盖一致（如 `1/4` 全部抓完）；
- 每条记录至少包含：`name`、`priceCny`、`detail link`；
- 无重复详情链接（按 offerId 去重）。
