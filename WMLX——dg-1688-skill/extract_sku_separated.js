/**
 * DG-1688：分离式 SKU 提取脚本（颜色/尺码分开）
 * 适用于颜色和尺码在不同 .feature-item 中的页面结构
 */
(function () {
  var skuRoot = document.querySelector(
    "#skuSelection .module-od-sku-selection.cart-gap"
  );

  if (!skuRoot) {
    return {
      pageUrl: location.href.split("#")[0],
      title: document.title,
      count: 0,
      items: [],
      _note: "sku_root_not_found"
    };
  }

  // 查找所有 feature-item
  var features = Array.from(skuRoot.querySelectorAll(".feature-item"));

  // 提取颜色选项（包含 .sku-filter-button 的 feature）
  var colorFeature = features.find(function (f) {
    return f.querySelector(".sku-filter-button") &&
           f.querySelector(".feature-item-label") &&
           (f.textContent.includes("颜色") || f.querySelector("img.label-image-wrap, img[src*='_sum']"));
  });

  var colorButtons = colorFeature
    ? Array.from(colorFeature.querySelectorAll(".sku-filter-button"))
    : [];

  // 提取尺码选项（包含 .expand-view-item 的 feature）
  var sizeFeature = features.find(function (f) {
    return f.querySelector(".expand-view-item") &&
           f.querySelector(".feature-item-label") &&
           (f.textContent.includes("尺码") || f.querySelector(".item-label"));
  });

  var sizeRows = sizeFeature
    ? Array.from(sizeFeature.querySelectorAll(".expand-view-item"))
    : [];

  // 解析价格文本
  function parsePrice(text) {
    if (!text) return null;
    var match = text.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : null;
  }

  // 提取颜色数据
  var colors = colorButtons.map(function (btn) {
    var img = btn.querySelector("img");
    var nameSpan = btn.querySelector(".label-name");
    return {
      imageUrl: img ? img.src : "",
      name: nameSpan ? nameSpan.textContent.trim() : ""
    };
  });

  // 提取尺码数据
  var sizes = sizeRows.map(function (row) {
    var label = row.querySelector(".item-label");
    var priceSpan = row.querySelector(".item-price-stock");
    return {
      name: label ? label.textContent.trim() : "",
      priceCny: priceSpan ? parsePrice(priceSpan.textContent) : null
    };
  });

  // 如果没有颜色或尺码，回退到标准提取
  if (colors.length === 0 || sizes.length === 0) {
    return {
      pageUrl: location.href.split("#")[0],
      title: document.title,
      count: 0,
      items: [],
      _note: "not_separated_structure",
      colorsFound: colors.length,
      sizesFound: sizes.length
    };
  }

  // 组合颜色和尺码：笛卡尔积
  var items = [];
  var pageUrl = location.href.split("#")[0];

  colors.forEach(function (color) {
    sizes.forEach(function (size) {
      // 组合名称：颜色名称 + 尺码
      var combinedName = color.name;
      if (size.name && !color.name.includes(size.name)) {
        combinedName = color.name + "-" + size.name;
      }

      items.push({
        imageUrl: color.imageUrl,
        name: combinedName,
        priceCny: size.priceCny,
        link: pageUrl
      });
    });
  });

  return {
    pageUrl: pageUrl,
    title: document.title,
    count: items.length,
    items: items,
    source: "separated_color_size",
    colorsCount: colors.length,
    sizesCount: sizes.length
  };
})();
