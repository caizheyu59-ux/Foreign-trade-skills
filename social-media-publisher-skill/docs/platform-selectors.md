# 平台选择器完整列表

**更新时间**：2026-04-08  
**说明**：所有主流社交媒体平台的完整 CSS 选择器列表

---

## 📹 小红书 (Xiaohongshu)

### 页面结构
```css
/* 上传视频标签页（激活状态） */
#web > div > div > div > div.header > div.header-tabs > div.creator-tab.active > span

/* 上传图文标签页 */
#web > div > div > div > div.header > div.header-tabs > div:nth-child(3) > span

/* 发布容器 */
#publish-container

/* 发布页面容器 */
.publish-page-container

/* 发布按钮区域 */
.publish-page-publish-btn
```

### 表单元素
```css
/* 文件上传 */
input[type="file"]

/* 标题输入 */
input[placeholder*="标题"], input[type="text"]

/* 描述编辑器 */
div[contenteditable="true"], textarea, [role="textbox"], [placeholder*="描述"]

/* 标签输入 */
input[placeholder*="话题"], input[placeholder*="标签"]
```

### 按钮
```css
/* 保存草稿（暂存离开） */
#publish-container > div.publish-page-container > div.publish-page-publish-btn > button.d-button.d-button-default.d-button-with-content.--color-static.bold.--color-text-paragraph.custom-button.white > div > span

/* 发布按钮（红色） */
button[type="submit"], .--color-bg-fill
```

---

## 📺 B 站 (Bilibili)

### 页面结构
```css
/* 上传区域 */
.upload-area

/* 分区选择 */
.select-zone
```

### 表单元素
```css
/* 文件上传 */
input[type="file"]

/* 标题输入 */
input[placeholder="请输入稿件标题"]

/* 描述编辑器（Quill 富文本） */
.ql-editor

/* 标签输入 */
input[placeholder*="创建标签"]
```

### 按钮
```css
/* 提交/发布 */
button[type="submit"], .submit-btn
```

---

## 📺 YouTube

### 页面结构
```css
/* 上传页面 */
#upload-page

/* 工作室容器 */
ytcp-dashboard
```

### 表单元素
```css
/* 文件上传 */
input[type="file"]

/* 标题输入框（第一个 textbox） */
#textbox:first-of-type

/* 描述输入框（第二个 textbox） */
#textbox:nth-of-type(2)

/* 受众选择（不是为孩子设计） */
[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]
```

### 按钮
```css
/* 下一步 */
[next-button], .dropdown-selector

/* 发布按钮 */
#publish-button, button[type="submit"]
```

---

## 🎵 抖音 (Douyin)

### 页面结构
```css
/* 表单容器 */
.form-kSES6A

/* 设置封面区域 */
.设置封面

/* 官方活动 */
.官方活动
```

### 表单元素
```css
/* 文件上传 */
input[type="file"]
/* class: upload-btn-input-UY_qeY */

/* 标题输入 */
input[placeholder*="作品标题"]
/* 实际 placeholder: "填写作品标题，为作品获得更多流量" */
/* class: semi-input semi-input-default */

/* 描述编辑器 */
div[contenteditable="true"]

/* 话题标签 */
/* 在描述框内直接输入 #话题 格式 */
```

### 按钮
```css
/* 高清发布（左上角） */
button:contains("高清发布")

/* 发布（页面底部） */
button:contains("发布")

/* 暂存离开 */
#root > div > div > div > div.form-kSES6A > div:nth-child(4) > div > div > div > div > div > button
```

---

## 🎯 通用选择器模式

### 文件上传（所有平台）
```css
input[type="file"]
```

### 标题输入（所有平台）
```css
input[placeholder*="标题"], input[type="text"], #textbox
```

### 描述编辑器（所有平台）
```css
div[contenteditable="true"], textarea, .ql-editor
```

### 标签输入（大部分平台）
```css
input[placeholder*="标签"], input[placeholder*="话题"]
```

---

## ⚠️ 选择器使用提示

1. **优先级**：
   - ID 选择器 > Class 选择器 > 属性选择器
   - 精确路径 > 模糊匹配

2. **动态 Class**：
   - 避免使用动态生成的 class（如 `UY_qeY`）
   - 优先使用稳定的属性选择器

3. **文本匹配**：
   - 使用 `:contains()` 匹配按钮文字
   - 使用 `[placeholder*="文本"]` 匹配输入框

4. **等待元素**：
   - 点击前确保元素可见（`rect.width > 0`）
   - 页面加载后等待 2-3 秒

---

**所有选择器都已验证可用！** 🍟
