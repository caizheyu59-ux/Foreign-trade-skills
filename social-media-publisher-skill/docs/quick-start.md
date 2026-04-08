# 5 分钟快速开始指南

**适合人群**：第一次使用本技能的用户  
**预计时间**：5 分钟

---

## 步骤 1：安装技能（1 分钟）

将技能包复制到 OpenClaw skills 目录：

```bash
# Windows PowerShell
Copy-Item -Recurse social-media-publisher-skill ~/.openclaw/skills/

# macOS/Linux
cp -r social-media-publisher-skill ~/.openclaw/skills/
```

---

## 步骤 2：配置 Chrome（1 分钟）

1. 打开 Chrome 浏览器
2. 访问：`chrome://inspect/#remote-debugging`
3. 勾选：✅ **"Allow remote debugging for this browser instance"**
4. 保持 Chrome 打开状态

---

## 步骤 3：登录平台（1 分钟）

在 Chrome 中登录你要发布的平台：

- 小红书：https://creator.xiaohongshu.com/
- B 站：https://member.bilibili.com/
- YouTube：https://studio.youtube.com/
- 抖音：https://creator.douyin.com/

**重要**：保持登录状态，不要关闭标签页！

---

## 步骤 4：准备内容（1 分钟）

创建内容文件（如 `content.txt`）：

```
1. 短标题
AI 时代，如何让海外客户一眼信任你？

4. 第一人称摘要
AI 时代的信任贵如金：
现在的 B2B 行业，信任就是命脉。

怎么玩转这个功能：
客户可以实时切换不同的镜头。

标签：#外贸独立站 #跨境电商
```

准备视频文件：
- 格式：MP4
- 大小：根据平台要求
- 路径：记住完整路径

---

## 步骤 5：开始发布（1 分钟）

对 AI 助手说：

```
发布视频到小红书，视频在 C:\Users\caizheyu\Desktop\video.mp4，内容在 C:\Users\caizheyu\Desktop\content.txt
```

AI 会自动：
1. 打开上传页面
2. 上传视频文件
3. 填写标题和描述
4. 添加标签
5. 保存草稿或发布

---

## ✅ 完成！

查看 AI 返回的截图，确认内容填写正确。

如果需要手动调整，可以在浏览器中继续操作。

---

## 🐛 遇到问题？

**问题**：CDP 连接失败  
**解决**：检查 Chrome 是否开启远程调试

**问题**：文件上传失败  
**解决**：确保视频路径正确，格式为 MP4

**问题**：描述填写无效  
**解决**：YouTube 必须用 execCommand，不能用 innerText

详细故障排除：见 `troubleshooting.md`

---

**祝你发布顺利！** 🍟
