# Kingsway 上传 Skill - 故障排查

## 常见问题

### "Kingsway API key is not configured"

**原因**：API Key 未配置或配置文件损坏

**解决**：
```powershell
sau kingsway setup --account kingsway --api-key "sk-xxx"
```

### Pre-add video 响应异常

**原因**：API 响应结构与预期不符

**解决**：检查 `pre_add_video` 函数中的响应解析逻辑，可能需要根据实际 API 响应调整字段路径。

### 心跳超时

**原因**：上传时间过长，心跳未能及时保活

**解决**：检查网络连接，确保心跳线程正常运行。日志中会有 `[Kingsway] Heartbeat started` 标记。

### PUT 上传 403

**原因**：预签名 URL 过期或签名无效

**解决**：重新调用预签名 URL 接口获取新的 URL。

### SEO page not found for language

**原因**：该视频下尚未有对应语言的字幕/SEO 页数据

**解决**：确认 Kingsway 后台该视频已生成对应语言的字幕。尝试使用 `en`（默认语言）。
