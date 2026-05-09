# 故障排查

## 找不到 `sau` 命令

可以尝试以下方式：

```powershell
.\.venv\Scripts\Activate.ps1
sau douyin --help
```

```powershell
.\.venv\Scripts\sau.exe douyin --help
```

```bash
uv run sau douyin --help
```

如果当前环境还没有安装项目：

```bash
uv pip install -e .
```

## cookie 无效或已过期

先检查 cookie 状态：

```bash
sau douyin check --account <account>
```

如果无效，就重新登录：

```bash
sau douyin login --account <account>
```

## 无头登录二维码处理

如果用户无法使用终端二维码输出：

- 查找 CLI 打印出来的临时二维码图片
- agent 不要只把图片路径回给用户
- agent 应优先直接把本地二维码图片展示/发送给用户扫码

如果终端二维码显示不正常，优先使用保存下来的图片路径，而不是反复尝试随机的终端设置。

## 上传参数缺失

### 视频上传

最少需要：

- `--account`
- `--file`
- `--title`

### 图文上传

最少需要：

- `--account`
- `--images`
- `--title`

`--note` 当前是可选图文正文。

## 图片限制

对 `upload-note` 来说：

- 不支持 GIF
- 最多 35 张图片

如果超出这些限制，先减少图片数量或替换文件格式，再重试。

## 定时发布

时间格式使用：

```text
YYYY-MM-DD HH:MM
```

如果不需要定时发布，去掉 `--schedule` 即可改为立即发布。

## 描述/正文中的引号导致命令崩溃

当 `--desc` 或 `--note` 的内容中包含双引号（如 `"新建小部件"`）时，PowerShell 会把参数拆成多段，导致命令报错。

**解决方式**：使用 `--desc-file` / `--note-file` 从文件读取内容：

```bash
# 把描述保存到文件
echo '点击"新建小部件"，选择悬浮模式' > desc.txt

# 用 --desc-file 代替 --desc
sau douyin upload-video --account kingsway --file video.mp4 --title "标题" --desc-file desc.txt
sau xiaohongshu upload-note --account kingsway --images img1.png --title "标题" --note-file note.txt
```

文件内容按 UTF-8 完整读取，不受 shell 引号解析影响。
