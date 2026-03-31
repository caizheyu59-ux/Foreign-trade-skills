# DG-1688 Skill - 1688 产品抓取与报价单生成器

DG 客户专用的 1688 产品抓取规则包，可自动从 1688 商品详情页提取 SKU 信息（图片、名称、价格），生成符合 DG 模板要求的专业 Excel 报价单。

## 文件结构

```
dg-1688-skill/
├── README.md                      # 本说明文档
├── SKILL.md                       # 详细规则文档
├── build_quote_from_detail.py     # 核心抓取与生成脚本
├── extract_sku_selection.js       # 标准 SKU 提取脚本
├── extract_sku_separated.js       # 分离式 SKU 提取脚本
├── image_handler.py               # 图片处理模块
└── requirements.txt               # Python 依赖
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 基本用法

```python
from build_quote_from_detail import build_quote

# 生成报价单（自动使用默认汇率 6.91）
output = build_quote("https://detail.1688.com/offer/706593264336.html")
print(f"报价单已生成：{output}")
```

### 3. 指定汇率

```python
output = build_quote("https://detail.1688.com/offer/706593264336.html", fx=7.2)
```

## 核心功能

### 1. 自动抓取 SKU 信息
- 产品名称
- 产品图片（自动匹配每个 SKU 对应的图片）
- 价格（CNY）
- 商品链接

### 2. 智能图片处理
- 逐个点击 SKU 获取对应主图
- 自动去除缩略图后缀
- 顶部裁剪 100px（去除编码水印）
- 等比缩放适配 Excel 单元格

### 3. 产品名称自动生成
- 格式：DG-{店铺缩写}-{序号}
- 示例：DG-HXQ-01, DG-HXQ-02
- 内置店铺映射：汇欣奇 → HXQ

### 4. 价格自动转换
- CNY → USD 公式：USD = CNY / 0.65 / 7
- 保留 2 位小数
- 美元符号绿色加粗显示

### 5. 1688 链接自动附加
- 每个产品自动添加 1688 链接
- 蓝色下划线样式
- 点击直接跳转到商品页面

## 输出示例

生成的 Excel 报价单包含：

### 公司介绍区（前 7 行）
- A1:I1  DongGuan DG Jewelry Co,.Ltd（深蓝底白字）
- D2:I2  Charms
- A3:C5  联系方式（网站、电话、邮箱）
- D3:I5  公司描述
- A7:I7  Stainless steel Charms（分类标题）

### 产品数据区（横向 3 列布局）
```
第 1 行（图片行）:  [图片] [1688 Link] [空] [图片] [1688 Link] [空] ...
第 2 行（数据行）:  [DG-HXQ-01] [¥17.00] [$3.74] [DG-HXQ-02] [¥17.00] [$3.74] ...
```

## 重要规则

### 1. SKU 图片匹配（强制）
- 禁止直接从 SKU 块内的 img 提取（那是缩略图）
- 必须逐个点击每个 SKU 选项
- 点击后从 #gallery img.preview-img 读取主图
- 等待 200ms 让主图切换完成

### 2. 1688 链接（强制）
- 每个产品必须在图片行添加 1688 链接
- 链接位置：B/E/H 列（图片右侧）
- 链接文本："1688 Link"（蓝色下划线）

### 3. 图片高清化（强制）
- 去掉 _sum 后缀
- 去掉 _.webp 后缀
- 顶部裁剪 100px

## 变更记录

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.4 | 2026-03-31 | SKU 图片匹配规则、产品名称格式改为 DG-{店铺缩写}-{序号}、强制 1688 链接 |

## 技术支持

遇到问题请查看详细规则文档 SKILL.md。
