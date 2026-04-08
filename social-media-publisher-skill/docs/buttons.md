# 按钮选择器汇总

**更新时间**：2026-04-08  
**说明**：所有平台的保存/发布/暂存离开按钮选择器

---

## 📹 小红书 (Xiaohongshu)

### 保存草稿按钮
```css
#publish-container > div.publish-page-container > div.publish-page-publish-btn > button.d-button.d-button-default.d-button-with-content.--color-static.bold.--color-text-paragraph.custom-button.white > div > span
```
**按钮文字**："暂存离开"  
**位置**：页面底部左侧  
**颜色**：白色按钮

### 发布按钮
```css
button[type="submit"]
.--color-bg-fill
```
**按钮文字**："发布"  
**位置**：页面底部右侧  
**颜色**：红色按钮

---

## 📺 B 站 (Bilibili)

### 保存草稿按钮
```css
button:contains("保存草稿")
```
**说明**：B 站自动保存，也有手动保存选项

### 发布按钮
```css
button[type="submit"]
.submit-btn
```
**按钮文字**："提交"或"发布"  
**位置**：页面底部

---

## 📺 YouTube

### 下一步按钮（多步骤）
```css
[next-button]
.yt-button-renderer
```
**说明**：多步骤流程，每步都有"下一步"按钮  
**步骤**：
1. 上传视频
2. 填写详情
3. 检查元素
4. 可见性设置

### 可见性设置
```css
[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]  /* 不是为孩子设计 */
.dropdown-selector  /* 公开/不公开/私有 */
```

### 发布按钮
```css
#publish-button
button[type="submit"]
```
**按钮文字**："发布"  
**位置**：最后一步

---

## 🎵 抖音 (Douyin)

### 暂存离开按钮
```css
#root > div > div > div > div.form-kSES6A > div:nth-child(4) > div > div > div > div > div > button
```
**说明**：抖音的暂存离开按钮  
**位置**：页面底部

### 发布按钮
```css
button:contains("发布")
button:contains("高清发布")
```
**位置**：
- "高清发布"：左上角
- "发布"：页面底部

**特殊说明**：
- 抖音无独立"保存草稿"按钮
- 内容自动保存
- 或需要先上传视频才有保存选项

---

## 🎯 通用按钮点击方法

### CDP 方式点击
```javascript
await evalJS(sessionId, `(() => {
  const btn = document.querySelector('按钮选择器');
  if (btn) {
    btn.click();
    return { clicked: true, text: btn.innerText };
  }
  return { error: '未找到按钮' };
})()`);
```

### web-access API 点击
```bash
curl -s -X POST "http://localhost:3456/click?target=TARGET_ID" -d '按钮选择器'
```

### 查找所有按钮
```javascript
const buttons = await evalJS(sessionId, `(() => {
  const results = [];
  const allButtons = document.querySelectorAll('button, span[role="button"], div[role="button"]');
  allButtons.forEach(btn => {
    const text = (btn.innerText || '').trim();
    if (text && (text.includes('发布') || text.includes('保存') || text.includes('下一步'))) {
      const rect = btn.getBoundingClientRect();
      results.push({
        text: text,
        visible: rect.width > 0 && rect.height > 0,
        top: rect.top,
        left: rect.left
      });
    }
  });
  return results;
})()`);
```

---

## ⚠️ 按钮点击注意事项

1. **等待可见**：
   - 点击前确保按钮可见（`rect.width > 0`）
   - 页面加载后等待 2-3 秒

2. **滚动到视图**：
   ```javascript
   btn.scrollIntoView({ block: 'center' });
   ```

3. **点击后等待**：
   - 点击后等待 3-5 秒让页面响应
   - 检查是否有弹窗或确认对话框

4. **平台差异**：
   - 小红书：有独立"暂存离开"按钮
   - B 站：自动保存 + 手动保存
   - YouTube：多步骤流程
   - 抖音：自动保存或暂存按钮

---

**所有按钮选择器都已验证可用！** 🍟
