# 故障排除指南

**更新时间**：2026-04-08  
**说明**：常见问题和解决方案

---

## 🔄 错误恢复机制

### 自动保存进度

脚本会自动保存上传进度到 `.xhs-upload-state.json` 文件。

**保存的进度信息**：
- 当前步骤（open/upload/title/description/tags）
- 时间戳
- targetId（用于恢复会话）

### 从中断点继续

如果上传过程中断：

1. **检查进度文件**
   ```bash
   cat .xhs-upload-state.json
   ```

2. **查看中断步骤**
   ```json
   {
     "step": "description",
     "timestamp": 1712587200000,
     "targetId": "ABC123..."
   }
   ```

3. **手动恢复**
   - 如果是在填写内容时中断，重新运行脚本会自动检测并跳过已完成的步骤
   - 如果是页面关闭了，需要重新开始

### 清除进度文件

如果想重新开始：
```bash
rm .xhs-upload-state.json
# 或 Windows
del .xhs-upload-state.json
```

---

## ⚠️ 自动重试机制

脚本内置了自动重试功能：

- **重试次数**：最多 2 次
- **重试间隔**：1 秒
- **适用操作**：文件上传、内容填写、按钮点击

**示例输出**：
```
操作失败，重试 1/2: 未找到元素
操作失败，重试 2/2: 未找到元素
❌ 错误：未找到元素
```

---

## 📊 日志输出

脚本会输出详细的日志：

```
ℹ️  [13:50:00] 开始小红书视频上传流程
ℹ️  [13:50:01] 标题：AI 时代，如何让海外客户一眼信任你？
ℹ️  [13:50:01] 描述：AI 时代的信任贵如金...
ℹ️  [13:50:01] 标签：10 个
ℹ️  [13:50:02] 步骤 1/5: 打开上传页面...
✅  [13:50:05] 页面已打开：ABC123...
ℹ️  [13:50:05] 进度已保存：open
```

**日志级别**：
- `ℹ️` 信息
- `✅` 成功
- `⚠️` 警告
- `❌` 错误

---

## 🔌 连接问题

### 问题 1：CDP 连接失败

**错误信息**：
```
Error: ECONNREFUSED
Cannot connect to localhost:3456
```

**可能原因**：
1. Chrome 未开启远程调试
2. CDP Proxy 未启动
3. 端口被占用

**解决方案**：

1. **检查 Chrome 远程调试**
   ```bash
   # 访问 Chrome 内部页面
   chrome://inspect/#remote-debugging
   
   # 确保勾选 "Allow remote debugging"
   ```

2. **启动 CDP Proxy**
   ```bash
   node ~/.openclaw/skills/web-access/scripts/cdp-proxy.mjs
   ```

3. **检查端口占用**
   ```bash
   # Windows
   netstat -ano | findstr 3456
   
   # macOS/Linux
   lsof -i :3456
   ```

---

## 📹 文件上传问题

### 问题 2：无法上传视频

**错误信息**：
```
Cannot set file input
DOM.setFileInputFiles failed
```

**可能原因**：
1. 使用了 nodeId 而非 objectId
2. 文件路径不正确
3. 文件格式不支持

**解决方案**：

1. **使用 objectId**
   ```javascript
   // ✅ 正确方式
   const domQuery = await sendCDP('Runtime.evaluate', {
     expression: `document.querySelector('input[type="file"]')`,
     returnByValue: false,
   }, sessionId);
   
   const objectId = domQuery.result?.result?.objectId;
   await sendCDP('DOM.setFileInputFiles', { objectId, files: [videoPath] }, sessionId);
   
   // ❌ 错误方式（使用 nodeId 会失败）
   ```

2. **检查文件路径**
   ```bash
   # 确保文件存在
   ls "C:\Users\caizheyu\Desktop\video.mp4"
   ```

3. **检查文件格式**
   - 小红书：MP4, MOV, FLV
   - B 站：MP4, FLV, AVI
   - YouTube：MP4, MOV, AVI, WMV
   - 抖音：MP4, MOV

---

## ✍️ 文本填写问题

### 问题 3：YouTube 描述填写无效

**错误信息**：
```
描述为空
Description not saved
```

**可能原因**：
- 使用了错误的方法填写描述

**解决方案**：

**必须使用 execCommand**：
```javascript
// ✅ 正确方式
const editor = document.querySelector('#textbox:nth-of-type(2)');
editor.focus();
document.execCommand('insertText', false, '描述内容');

// ❌ 错误方式（无效）
editor.innerText = '描述内容';  // 无效！
editor.innerHTML = '描述内容';  // 无效！
editor.value = '描述内容';      // 无效！
```

---

### 问题 4：B 站描述填写失败

**错误信息**：
```
Cannot set innerText of null
```

**可能原因**：
- Quill 编辑器未加载完成

**解决方案**：

1. **等待编辑器加载**
   ```javascript
   await new Promise(r => setTimeout(r, 3000)); // 等待 3 秒
   
   const editor = document.querySelector('.ql-editor');
   if (editor) {
     editor.innerText = '描述内容';
   }
   ```

2. **检查选择器**
   ```javascript
   // 确认 Quill 编辑器存在
   const editor = document.querySelector('.ql-editor');
   console.log('Editor found:', !!editor);
   ```

---

### 问题 5：抖音标签不显示

**错误信息**：
```
标签未添加
Hashtag not added
```

**可能原因**：
- 使用了错误的标签输入方式

**解决方案**：

**抖音在描述框内直接输入 #话题**：
```javascript
// ✅ 正确方式
const editor = document.querySelector('div[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, ' #外贸独立站');

// ❌ 错误方式（抖音没有单独的标签输入框）
const tagInput = document.querySelector('input[placeholder*="标签"]');  // 不存在！
```

---

## 🔘 按钮点击问题

### 问题 6：找不到保存按钮

**错误信息**：
```
Button not found
Cannot click element
```

**可能原因**：
1. 按钮选择器错误
2. 按钮未加载完成
3. 平台 UI 更新

**解决方案**：

1. **查找所有按钮**
   ```javascript
   const buttons = await evalJS(sessionId, `(() => {
     const results = [];
     const allButtons = document.querySelectorAll('button, span[role="button"]');
     allButtons.forEach(btn => {
       const text = (btn.innerText || '').trim();
       if (text && (text.includes('发布') || text.includes('保存'))) {
         results.push({ text: text });
       }
     });
     return results;
   })()`);
   
   console.log('Found buttons:', buttons);
   ```

2. **使用正确的选择器**
   - 见 `docs/buttons.md`

3. **等待按钮可见**
   ```javascript
   await new Promise(r => setTimeout(r, 3000));
   ```

---

## 🔐 登录问题

### 问题 7：登录失效

**错误信息**：
```
Please login
需要登录
```

**可能原因**：
- Chrome 登录会话过期

**解决方案**：

1. **手动重新登录**
   - 在 Chrome 中打开平台网站
   - 重新登录账号
   - 保持登录状态

2. **检查 Cookie**
   ```javascript
   const cookies = await evalJS(sessionId, `document.cookie`);
   console.log('Has cookies:', cookies.length > 0);
   ```

---

## 📊 性能问题

### 问题 8：操作超时

**错误信息**：
```
Timeout: CDP command failed
30000ms timeout exceeded
```

**可能原因**：
1. 网络速度慢
2. 页面加载慢
3. 服务器响应慢

**解决方案**：

1. **增加等待时间**
   ```javascript
   await new Promise(r => setTimeout(r, 10000)); // 等待 10 秒
   ```

2. **检查网络**
   ```bash
   ping creator.xiaohongshu.com
   ```

3. **重试操作**
   - 等待页面完全加载
   - 重新执行命令

---

## 🆘 获取帮助

如果以上方案都无法解决问题：

1. **检查日志**
   ```bash
   # 查看 CDP Proxy 日志
   tail -f /tmp/cdp-proxy.log
   ```

2. **收集信息**
   - 错误信息截图
   - Chrome 版本
   - 平台名称
   - 操作步骤

3. **提交 Issue**
   - GitHub 仓库：（待创建）
   - 包含以上信息

---

**祝你问题早日解决！** 🍟
