#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import xlsxwriter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from image_handler import process_image_for_excel


PROXY_BASE = "http://localhost:3456"
DEFAULT_FX = 6.91


def _normalize_hd_image_url(url: str) -> str:
    """去除缩略后缀，优先返回高清原图地址。"""
    u = (url or "").strip()
    if not u:
        return ""
    # 1688 缩略图格式：xxx.jpg_sum.jpg -> xxx.jpg（直接去掉 _sum.xxx 后缀）
    u = re.sub(r"_sum\.[a-z]+$", "", u, flags=re.IGNORECASE)
    u = re.sub(r"_\.webp$", "", u, flags=re.IGNORECASE)
    # 确保 URL 有扩展名
    if not re.search(r"\.[a-z]+$", u, flags=re.IGNORECASE):
        u += ".jpg"
    return u


def _parse_spec_price_pairs(text: str) -> List[Dict[str, Any]]:
    """通用规格解析：从页面文本中提取“规格名 + 价格 + 库存”"""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    out: List[Dict[str, Any]] = []
    seen = set()
    # 先命中同一行（最稳）
    noise_tokens = [
        "颜色",
        "商品",
        "评价",
        "属性",
        "详情",
        "客服",
        "包邮",
        "退货",
        "运费",
        "极速退款",
        "首件",
        "到手价",
        "已售",
        "发货",
        "保障",
        "服务",
        "包赔",
    ]

    def is_noise_name(s: str) -> bool:
        t = (s or "").strip()
        return (not t) or any(k in t for k in noise_tokens)

    def is_sku_like_name(s: str) -> bool:
        t = (s or "").strip()
        if not t:
            return False
        # 常见规格命名：P1234-xxx / F1714-xxx / AB12-xxx
        if re.search(r"[A-Za-z]\d{2,}", t):
            return True
        if "-" in t and re.search(r"\d", t):
            return True
        return False

    for i, ln in enumerate(lines):
        m = re.search(r"¥\s*([0-9]+(?:\.[0-9]+)?)\s*库存", ln)
        if not m:
            continue
        price = float(m.group(1))
        name = ln[: m.start()].strip() or (lines[i - 1] if i > 0 else "")
        name = re.sub(r"\s+", " ", name).strip()
        if is_noise_name(name) or not is_sku_like_name(name):
            continue
        key = (name, price)
        if key not in seen:
            seen.add(key)
            out.append({"name": name, "priceCny": price})

    # 跨行模式：规格名 -> ¥价格 -> 库存
    pending_name = None
    pending_price = None
    for ln in lines:
        # 规格名候选：包含字母/数字/中文且不含价格、库存等关键词
        is_name_like = bool(re.search(r"[A-Za-z0-9\u4e00-\u9fff]", ln)) and ("库存" not in ln and "¥" not in ln)
        if is_name_like and len(ln) <= 80 and not is_noise_name(ln):
            pending_name = ln
            continue

        m_price = re.search(r"¥\s*([0-9]+(?:\.[0-9]+)?)", ln)
        if m_price:
            pending_price = float(m_price.group(1))
            # 同行也可能有库存
            if "库存" in ln and pending_name and pending_price is not None:
                key = (pending_name, pending_price)
                if key not in seen and is_sku_like_name(pending_name):
                    seen.add(key)
                    out.append({"name": pending_name, "priceCny": pending_price})
                pending_name, pending_price = None, None
            continue

        if "库存" in ln and pending_name and pending_price is not None:
            key = (pending_name, pending_price)
            if key not in seen and is_sku_like_name(pending_name):
                seen.add(key)
                out.append({"name": pending_name, "priceCny": pending_price})
            pending_name, pending_price = None, None

    return out


def _proxy_get(path: str) -> Any:
    resp = requests.get(f"{PROXY_BASE}{path}", timeout=30)
    resp.raise_for_status()
    return resp.json()


def _proxy_eval(target_id: str, js_expr: str) -> Any:
    resp = requests.post(
        f"{PROXY_BASE}/eval",
        params={"target": target_id},
        data=js_expr.encode("utf-8"),
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data.get("value")


def _find_or_open_target(detail_url: str) -> str:
    targets = _proxy_get("/targets")
    for t in targets:
        u = str(t.get("url", ""))
        if "detail.1688.com/offer/" in u and detail_url.split("?")[0] in u and "punish" not in u:
            tid = t.get("targetId")
            if tid:
                return tid
    tid = _proxy_get(f"/new?url={detail_url}").get("targetId")
    if not tid:
        raise RuntimeError("无法打开 1688 详情页 target")
    return tid


def _page_probe(target_id: str) -> Dict[str, Any]:
    return _proxy_eval(
        target_id,
        """(function(){
          var hasSkuRoot = !!document.querySelector('#skuSelection .module-od-sku-selection.cart-gap');
          var hasGallery = !!document.querySelector('#gallery img');
          var txt = (document.body && document.body.innerText) || '';
          return {
            href: location.href || '',
            title: document.title || '',
            readyState: document.readyState || '',
            hasSkuRoot: hasSkuRoot,
            hasGallery: hasGallery,
            bodyTextLen: txt.length || 0
          };
        })()""",
    ) or {}


def _wait_for_detail_ready(target_id: str, detail_url: str, timeout_s: float = 12.0) -> Dict[str, Any]:
    expect = (detail_url or "").split("?")[0]
    deadline = time.time() + timeout_s
    last: Dict[str, Any] = {}
    while time.time() < deadline:
        last = _page_probe(target_id)
        href = str(last.get("href", ""))
        ready = str(last.get("readyState", ""))
        href_ok = bool(href and href != "about:blank" and expect in href)
        dom_ok = bool(last.get("hasSkuRoot") or last.get("hasGallery") or int(last.get("bodyTextLen", 0)) > 1000)
        if href_ok and ready in ("interactive", "complete") and dom_ok:
            return last
        time.sleep(0.4)
    return last


def _extract_items_by_rule(target_id: str) -> Dict[str, Any]:
    # 优先检测分离式 SKU 结构（颜色/尺码分开）
    separated_extractor = Path(__file__).with_name("extract_sku_separated.js").read_text(encoding="utf-8")
    separated_result = _proxy_eval(target_id, separated_extractor) or {}
    sep_items = separated_result.get("items", [])
    if len(sep_items) > 1:
        separated_result["source"] = "separated_color_size"
        return separated_result

    # 标准提取
    extractor = Path(__file__).with_name("extract_sku_selection.js").read_text(encoding="utf-8")
    result = _proxy_eval(target_id, extractor) or {}

    items = result.get("items", []) if isinstance(result, dict) else []

    if items:
        one = items[0]
        # 严格命中多条时直接返回；单条时继续做文本探测，避免漏抓。
        if len(items) > 1 and not ("验证码" in str(one.get("name", "")) or "punish" in str(one.get("link", ""))):
            result["source"] = "strict"
            return result
        # 单条但有有效数据（图片/价格）时，直接返回，不做 fallback
        if len(items) == 1:
            has_image = bool(one.get("imageUrl"))
            has_price = bool(one.get("priceCny"))
            if has_image or has_price:
                result["source"] = "strict_single"
                return result

    # Fallback: 仅解析规格名称与价格，不在这里做图片兜底，避免错图。
    probe = _proxy_eval(
        target_id,
        """(function(){
          return {
            title: document.title || '',
            pageUrl: location.href.split('#')[0],
            text: (document.body && document.body.innerText) || ''
          };
        })()""",
    )
    text = str((probe or {}).get("text", ""))
    page_url = str((probe or {}).get("pageUrl", ""))

    pairs = _parse_spec_price_pairs(text)
    dedup: List[Dict[str, Any]] = []
    for idx, sp in enumerate(pairs):
        n = sp["name"]
        price = sp["priceCny"]
        dedup.append(
            {
                "imageUrl": "",
                "name": n,
                "priceCny": float(price),
                "link": page_url,
            }
        )
    if dedup:
        return {"pageUrl": page_url, "items": dedup, "count": len(dedup), "source": "fallback_text"}
    if isinstance(result, dict):
        result["source"] = "strict_single_or_empty"
        return result
    return {"pageUrl": page_url, "items": [], "count": 0, "source": "empty"}


def _extract_items_by_clicking_sku(target_id: str) -> Dict[str, Any]:
    """
    【重要】逐个点击 SKU 获取对应产品图 - 确保颜色与图片正确匹配
    
    工作流程：
    1. 读取所有 SKU 列表（名称、价格）
    2. 逐个点击每个 SKU 选项
    3. 点击后立即从 #gallery img.preview-img 读取主图
    4. 将 SKU 名称与对应图片绑定
    
    审计结论：
    - 部分页面 gallery 不在 cart-gap 容器内，图片必须从页面级 #gallery 读取
    - 必须使用 #gallery img.preview-img 或 #gallery img 选择器
    - 禁止使用 SKU 块内的 img（那是缩略图，不是产品图）
    """
    # 步骤 1：读取所有 SKU 列表
    base = _proxy_eval(
        target_id,
        """(function(){
          var root = document.querySelector('#skuSelection .module-od-sku-selection.cart-gap');
          var blocks = root ? Array.from(root.querySelectorAll('div.expand-view-list-wrapper > div')) : [];
          var rows = blocks.map(function(b, idx){
            var name = '';
            var nameNode = b.querySelector('[class*="title"], [class*="name"], span, p, div');
            if (nameNode) name = (nameNode.textContent || '').replace(/\\s+/g,' ').trim();
            if (!name) name = (b.textContent || '').replace(/\\s+/g,' ').trim().slice(0,80);
            var priceTxt = '';
            var pnode = b.querySelector('[class*="price"], em, strong, [class*="amount"]');
            if (pnode) priceTxt = (pnode.textContent || '').trim();
            if (!priceTxt) priceTxt = (b.textContent || '').trim();
            var m = priceTxt.match(/[\\d.]+/g);
            var p = m && m.length ? parseFloat(m[m.length-1]) : null;
            return {index: idx, name: name, priceCny: isNaN(p)?null:p};
          });
          return {count: rows.length, pageUrl: location.href.split('#')[0], rows: rows};
        })()""",
    )
    rows = (base or {}).get("rows", [])
    page_url = (base or {}).get("pageUrl", "")
    
    # 如果只有 1 个或 0 个 SKU，使用 fallback 模式
    if not rows or len(rows) <= 1:
        probe = _proxy_eval(
            target_id,
            """(function(){
              return {
                pageUrl: location.href.split('#')[0],
                text: (document.body && document.body.innerText) || '',
                galleryImages: Array.from(
                  document.querySelectorAll('#gallery > div > div.od-gallery-preview > div.od-gallery-list-wapper > ul > li > div > img')
                ).map(function(img){
                  return (img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || img.currentSrc || img.src || '').trim();
                }).filter(Boolean)
              };
            })()""",
        ) or {}
        pairs = _parse_spec_price_pairs(str(probe.get("text", "")))
        gallery_images = [_normalize_hd_image_url(u) for u in probe.get("galleryImages", []) if isinstance(u, str)]
        items = []
        for i, sp in enumerate(pairs):
            items.append(
                {
                    "imageUrl": gallery_images[i] if i < len(gallery_images) else "",
                    "name": sp["name"],
                    "priceCny": sp["priceCny"],
                    "link": page_url,
                }
            )
        return {"pageUrl": page_url, "items": items, "count": len(items)}

    # 步骤 2+3：逐个点击 SKU，获取对应主图
    items: List[Dict[str, Any]] = []
    for row in rows:
        idx = int(row.get("index", 0))
        
        # 点击 SKU 选项
        _proxy_eval(
            target_id,
            f"""(function(){{
              var root = document.querySelector('#skuSelection .module-od-sku-selection.cart-gap');
              var blocks = root ? Array.from(root.querySelectorAll('div.expand-view-list-wrapper > div')) : [];
              var b = blocks[{idx}];
              if(!b) return false;
              b.click();
              var inner = b.querySelector('input,button,label,span,div');
              if(inner && inner.click) inner.click();
              return true;
            }})()""",
        )
        time.sleep(0.2)  # 等待主图切换
        
        # 从 #gallery 读取主图（关键：必须用这个选择器）
        img = _proxy_eval(
            target_id,
            """(function(){
              function pick(el){
                if(!el) return '';
                return (el.getAttribute('data-src') || el.getAttribute('data-lazy-src') || el.currentSrc || el.src || '').trim();
              }
              // 优先使用 preview-img 类的主图
              var n = document.querySelector('#gallery img.preview-img');
              var u = pick(n);
              // 如果没有 preview-img，尝试 #gallery 下的第一个 img
              if(!u){
                var fallback = document.querySelector('#gallery img');
                u = pick(fallback);
              }
              // 过滤掉 icon/svg
              if(!u || /\\.svg(?:$|\\?)/i.test(u)){
                return '';
              }
              return u;
            })()""",
        )
        items.append(
            {
                "imageUrl": _normalize_hd_image_url(img or ""),
                "name": row.get("name", ""),
                "priceCny": row.get("priceCny"),
                "link": page_url,
            }
        )

    # 去重（按 名称+价格）
    dedup = []
    seen = set()
    for it in items:
        k = (str(it.get("name", "")).strip(), str(it.get("priceCny")))
        if k in seen:
            continue
        seen.add(k)
        dedup.append(it)
    return {"pageUrl": page_url, "items": dedup, "count": len(dedup)}


def _items_quality(items: List[Dict[str, Any]]) -> tuple[int, int, int]:
    with_image = sum(1 for i in items if str(i.get("imageUrl", "")).strip())
    with_name = sum(1 for i in items if str(i.get("name", "")).strip())
    with_price = sum(1 for i in items if i.get("priceCny") not in (None, "", "私密价"))
    return with_image, with_name, with_price


def _prefer_better_items(primary: List[Dict[str, Any]], candidate: List[Dict[str, Any]]) -> bool:
    if not candidate:
        return False
    p = _items_quality(primary)
    c = _items_quality(candidate)
    # 优先有图，其次有名称，再次有价格，再看条目数
    if c[0] != p[0]:
        return c[0] > p[0]
    if c[1] != p[1]:
        return c[1] > p[1]
    if c[2] != p[2]:
        return c[2] > p[2]
    return len(candidate) > len(primary)


def _render_dg_quote(items: List[Dict[str, Any]], data: Dict[str, Any], detail_url: str, output_path: str, shop_name: str = "") -> str:
    wb = xlsxwriter.Workbook(output_path)
    ws = wb.add_worksheet("Quotation")

    # 新布局：3列一组，共3组 = 9列（图片|链接|空）x3
    ws.set_column("A:A", 18)   # 图片1
    ws.set_column("B:B", 10)   # 链接1 -> 数据行作为CNY列(窄)
    ws.set_column("C:C", 14)   # 空1 -> 数据行作为USD列(宽，显示$)
    ws.set_column("D:D", 18)   # 图片2
    ws.set_column("E:E", 10)   # 链接2 -> CNY
    ws.set_column("F:F", 14)   # 空2 -> USD
    ws.set_column("G:G", 18)   # 图片3
    ws.set_column("H:H", 10)   # 链接3 -> CNY
    ws.set_column("I:I", 14)   # 空3 -> USD

    _write_header(ws, wb)

    base = wb.add_format({"align": "center", "valign": "vcenter", "border": 1})
    name_fmt = wb.add_format({"align": "center", "valign": "vcenter", "border": 1, "bold": True})
    cny_fmt = wb.add_format({"align": "center", "valign": "vcenter", "border": 1, "num_format": "0.00"})
    usd_fmt = wb.add_format({"align": "center", "valign": "vcenter", "border": 1, "font_color": "#0B7A0B", "bold": True, "num_format": '"$"#,##0.00'})
    link_fmt = wb.add_format({"align": "center", "valign": "vcenter", "border": 1, "font_color": "#0563C1", "underline": 1})

    def extract_shop_code(shop_name: str) -> str:
        """从店铺名提取缩写"""
        if not shop_name:
            return "XXX"
        shop_mappings = {
            "汇欣奇": "HXQ",
            "汇欣奇玩具厂": "HXQ",
            "汕头市澄海区汇欣奇玩具厂": "HXQ",
        }
        for key, code in shop_mappings.items():
            if key in shop_name:
                return code
        chars = [c for c in shop_name if c.isalnum()]
        if chars:
            return "".join(chars[:3]).upper()
        return "XXX"

    def extract_code(index: int = 0, shop_code: str = "XXX") -> str:
        """生成产品编码：DG-{店铺缩写}-{序号} 例：DG-HXQ-01"""
        return f"DG-{shop_code}-{index:02d}"

    # 提取店铺缩写
    shop_code = extract_shop_code(shop_name)

    def calc_usd(price_cny: float) -> float:
        if not price_cny:
            return 0.0
        return round(price_cny / 0.65 / 7, 2)

    start_row = 7  # header占7行(0-6)，数据从第8行(索引7)开始
    for group_idx in range(0, len(items), 3):
        group_items = items[group_idx:group_idx + 3]
        img_row = start_row + (group_idx // 3) * 2
        data_row = img_row + 1
        ws.set_row(img_row, 120)
        ws.set_row(data_row, 24)

        for i, item in enumerate(group_items):
            col_offset = i * 3
            image_url_raw = (item.get("imageUrl") or "").strip()
            image_url = _normalize_hd_image_url(image_url_raw)

            if image_url:
                img_path, w, h = process_image_for_excel(image_url, "./tmp/images")
                if img_path and Path(img_path).exists():
                    # Windows 兼容性：将反斜杠转换为正斜杠，确保 xlsxwriter 正确识别路径
                    img_path_normalized = str(Path(img_path).as_posix())
                    box_w, box_h = 140.0, 100.0
                    scale = min(1.0, box_w / w, box_h / h) if w and h else 1.0
                    ws.insert_image(
                        img_row,
                        col_offset,
                        img_path_normalized,
                        {"x_offset": 5, "y_offset": 5, "x_scale": scale, "y_scale": scale, "positioning": 1},
                    )
                else:
                    ws.write_url(img_row, col_offset, image_url, link_fmt, string="Image URL")
            else:
                ws.write(img_row, col_offset, "No Image", base)

            link = (item.get("link") or data.get("pageUrl") or detail_url).strip()
            if link.startswith(("http://", "https://")):
                ws.write_url(img_row, col_offset + 1, link, link_fmt, string="1688 Link")
            else:
                ws.write(img_row, col_offset + 1, link, base)
            ws.write(img_row, col_offset + 2, "", base)

            raw_name = (item.get("name") or "").strip()
            global_index = group_idx + i + 1
            product_code = extract_code(global_index, shop_code)
            ws.write(data_row, col_offset, product_code, name_fmt)

            price_cny = item.get("priceCny")
            if isinstance(price_cny, (int, float)):
                ws.write_number(data_row, col_offset + 1, float(price_cny), cny_fmt)
                ws.write_number(data_row, col_offset + 2, calc_usd(float(price_cny)), usd_fmt)
            else:
                ws.write_blank(data_row, col_offset + 1, None, base)
                ws.write_blank(data_row, col_offset + 2, None, base)

    wb.close()
    return output_path


def build_quote_from_items(
    items: List[Dict[str, Any]],
    output_path: Optional[str] = None,
    page_url: str = "",
) -> str:
    """将聚合后的规格 items 直接按 DG 模板渲染成单份报价单。"""
    if not items:
        raise RuntimeError("items is empty")
    output_path = output_path or f"./output/dg1688_template_quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return _render_dg_quote(items=items, data={"pageUrl": page_url}, detail_url=page_url, output_path=output_path)


def _write_header(ws, wb) -> None:
    # 适配9列横向布局的header
    # 第1行：公司标题（深蓝背景，白色大字）
    blue = wb.add_format(
        {"bold": True, "font_color": "white", "bg_color": "#0B2E73", "align": "center", "valign": "vcenter", "font_size": 22}
    )
    ws.merge_range("A1:I1", "DongGuan DG Jewelry Co,.Ltd", blue)
    ws.set_row(0, 50)

    # 格式定义
    label = wb.add_format({"bold": True, "font_color": "#0B2E73", "font_size": 11, "valign": "vcenter"})
    normal = wb.add_format({"font_size": 11, "font_color": "#1b2a4a", "valign": "vcenter", "text_wrap": True})
    section = wb.add_format({"bold": True, "font_size": 20, "font_color": "#0B2E73", "align": "center", "valign": "vcenter"})
    charms_fmt = wb.add_format({"bold": True, "font_size": 14, "font_color": "#0B2E73", "align": "center", "valign": "vcenter"})

    # 第2行：左侧空，右侧 Charms
    ws.merge_range("A2:C2", "", wb.add_format({"bg_color": "white"}))
    ws.merge_range("D2:I2", "Charms", charms_fmt)
    ws.set_row(1, 28)

    # 第3-5行：左侧 W/P/E，右侧合并显示描述
    ws.merge_range("A3:C3", "W: www.dgjewelry.cn", label)
    ws.set_row(2, 22)
    ws.merge_range("A4:C4", "P : +86 186 8869 1502", label)
    ws.set_row(3, 22)
    ws.merge_range("A5:C5", "E: sparrow@dgjewelry.cn", label)
    ws.set_row(4, 22)

    # 右侧3-5行合并，显示完整描述
    ws.merge_range(
        "D3:I5",
        "As a jewelry, a pendant not only has a decorative role, but also carries a rich moral and symbolic meaning. Here are some pendants and charms.\n\nWith our rich experience, OEM & ODM services are also welcome here, send us your design or idea, we will make your idea come into reality.",
        normal,
    )

    # 第6行：左侧 Contact us，右侧空白
    ws.merge_range("A6:C6", "Contact us for more Collection", label)
    ws.merge_range("D6:I6", "", normal)
    ws.set_row(5, 26)

    # 第7行：分类标题
    ws.merge_range("A7:I7", "Stainless steel Charms", section)
    ws.set_row(6, 40)



def extract_quote_items(detail_url: str, fx: float = DEFAULT_FX) -> List[Dict[str, Any]]:
    """提取详情页规格并转换为通用 ProductDict（用于合并总报价单）。"""
    target_id = _find_or_open_target(detail_url)
    probe = _wait_for_detail_ready(target_id, detail_url)
    href = str(probe.get("href", ""))
    if not href or href == "about:blank":
        # 强制新开一次页签并再等待，降低命中空白页概率
        target_id = _proxy_get(f"/new?url={detail_url}").get("targetId")
        if not target_id:
            raise RuntimeError("无法打开 1688 详情页 target（second try）")
        _wait_for_detail_ready(target_id, detail_url)

    data = _extract_items_by_rule(target_id)
    items = data.get("items", []) if isinstance(data, dict) else []

    # 尝试点击式提取，并按数据质量选择更优结果，而不是仅看条目数
    clicked = _extract_items_by_clicking_sku(target_id)
    clicked_items = clicked.get("items", []) if isinstance(clicked, dict) else []
    if _prefer_better_items(items, clicked_items):
        data = clicked
        items = clicked_items

    if not items:
        raise RuntimeError("未抓取到 SKU 数据，请确认页面已加载规格区域。")

    product_rows: List[Dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        raw_name = (item.get("name") or "").strip() or f"DG-ITEM-{idx:02d}"
        image_url = _normalize_hd_image_url((item.get("imageUrl") or "").strip())
        raw_price = item.get("priceCny")
        usd_price = None
        if isinstance(raw_price, (int, float)):
            usd_price = round(float(raw_price) / 0.65 / 7, 2)
        product_rows.append(
            {
                "sku": f"DG-{idx:04d}",
                "name": raw_name,
                "image_url": image_url,
                "price": usd_price if usd_price is not None else "",
                "specs": "",
                "moq": 1,
                "remarks": f"CNY: {raw_price}" if raw_price not in (None, "") else "",
                "source": "web",
                "detail_link": (item.get("link") or data.get("pageUrl") or detail_url),
            }
        )

    return product_rows


def build_quote(detail_url: str, fx: float = DEFAULT_FX) -> str:
    target_id = _find_or_open_target(detail_url)
    probe = _wait_for_detail_ready(target_id, detail_url)
    href = str(probe.get("href", ""))
    if not href or href == "about:blank":
        target_id = _proxy_get(f"/new?url={detail_url}").get("targetId")
        if not target_id:
            raise RuntimeError("无法打开 1688 详情页 target（second try）")
        _wait_for_detail_ready(target_id, detail_url)

    # 优先使用 strict 规则提取（直接从 .expand-view-item 读取）
    data = _extract_items_by_rule(target_id)
    items = data.get("items", []) if isinstance(data, dict) else []

    clicked = _extract_items_by_clicking_sku(target_id)
    clicked_items = clicked.get("items", []) if isinstance(clicked, dict) else []
    if _prefer_better_items(items, clicked_items):
        data = clicked
        items = clicked_items
    if not items:
        raise RuntimeError("未抓取到 SKU 数据，请确认页面已加载规格区域。")

    output_path = f"./output/dg1688_template_quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    _render_dg_quote(items=items, data=data, detail_url=detail_url, output_path=output_path, shop_name=data.get("shop", ""))

    preview = {
        "url": detail_url,
        "count": len(items),
        "output": output_path,
        "first_rows": items[:5],
    }
    preview_path = Path("./tmp/dg1688_template_preview.json")
    preview_path.write_text(json.dumps(preview, ensure_ascii=False, indent=2), encoding="utf-8")

    return output_path

if __name__ == "__main__":
    test_url = "https://detail.1688.com/offer/633830968371.html"
    out = build_quote(test_url, DEFAULT_FX)
    print(out)
