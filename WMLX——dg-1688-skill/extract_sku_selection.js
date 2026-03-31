/**
 * DG-1688：详情页 SKU 区提取脚本
 * 在 1688 商品详情页执行（browser evaluate / CDP eval）
 * 选择器：#skuSelection .module-od-sku-selection.cart-gap .expand-view-item
 */
(function () {
  var skuRoot = document.querySelector(
    "#skuSelection .module-od-sku-selection.cart-gap"
  );
  function numFromPriceText(s) {
    if (!s) return null;
    var t = String(s).replace(/\s+/g, "");
    var m = t.match(/[\d.]+/g);
    if (!m || !m.length) return null;
    var last = m[m.length - 1];
    var n = parseFloat(last);
    return isNaN(n) ? null : n;
  }

  // 从规格行内取缩略图（在 .expand-view-item 内找 img）
  // 注意：URL 规范化（去掉 _sum 后缀）在 Python 端统一处理
  function imgUrlFromSpecRow(el) {
    if (!el) return "";
    // 优先找 item-image-icon 内的 img，或任意带 src 的 img
    var img = el.querySelector(".item-image-icon img, img.ant-image-img, img[src*='_sum']");
    if (!img) return "";
    var url = (
      img.getAttribute("data-src") ||
      img.getAttribute("data-lazy-src") ||
      img.currentSrc ||
      img.src ||
      ""
    ).trim();
    // 返回原始 URL（_sum 后缀处理在 Python 端做）
    return url;
  }

  function nameFromBlock(el) {
    // 优先找 .item-label
    var label = el.querySelector(".item-label");
    if (label) {
      return label.textContent.trim();
    }
    // 兜底：找文本节点
    var t = "";
    var candidates = el.querySelectorAll(
      '[class*="title"], [class*="name"], [class*="sku"], span, p, div'
    );
    for (var i = 0; i < candidates.length; i++) {
      var c = candidates[i];
      if (el.contains(c) && c.children.length === 0) {
        var x = (c.textContent || "").replace(/\s+/g, " ").trim();
        if (x && x.length > t.length && !/^¥/.test(x) && !/^\d/.test(x))
          t = x;
      }
    }
    return t.slice(0, 500);
  }

  function priceFromBlock(el) {
    // 优先找 .item-price-stock
    var priceEl = el.querySelector(".item-price-stock, [class*='price']");
    if (priceEl) {
      return numFromPriceText(priceEl.textContent);
    }
    return null;
  }

  // 关键修正：直接找 .expand-view-item 作为规格行
  var items = [];
  var pageUrl = location.href.split("#")[0];

  if (skuRoot) {
    var specRows = Array.from(skuRoot.querySelectorAll(".expand-view-item"));
    if (specRows.length) {
      for (var j = 0; j < specRows.length; j++) {
        var row = specRows[j];
        items.push({
          imageUrl: imgUrlFromSpecRow(row),
          name: nameFromBlock(row),
          priceCny: priceFromBlock(row),
          link: pageUrl,
        });
      }
    }
  }

  if (!items.length) {
    items.push({
      imageUrl: "",
      name: document.title || "",
      priceCny: null,
      link: pageUrl,
      _note: skuRoot ? "no_expand_view_item_found" : "sku_root_not_found",
    });
  }

  return {
    pageUrl: pageUrl,
    title: document.title,
    count: items.length,
    items: items,
  };
})();
