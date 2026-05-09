# Kingsway 上传 Skill - 运行前提

## 必需条件

- ✅ `sau` CLI 已安装（来自 `social-auto-upload`）
- ✅ `requests` Python 库已安装（`pip install requests`）
- ✅ Python 3.12+ 已安装

## 配置

- API Key 通过 `sau kingsway setup --account <name> --api-key <key>` 配置
- 配置文件存储位置：`cookies/kingsway_config/<account_name>.json`
- 该目录已 `.gitignore`，不会提交到 Git

## API Base URL

默认：`https://api.kingswayvideo.com`

如需使用其他环境，通过 `--base-url` 参数指定：
```powershell
sau kingsway setup --account kingsway --api-key sk-xxx --base-url "https://test-api.kingswayvideo.com"
```
