#!/bin/bash
# Kingsway 上传命令模板（Shell）

# 检查 API Key 配置
sau kingsway check --account kingsway

# 配置 API Key
sau kingsway setup --account kingsway --api-key "sk-xxx" --base-url "https://api.kingswayvideo.com"

# 上传视频（精准填写标题和描述）
sau kingsway upload-video \
  --account kingsway \
  --file /path/to/video.mp4 \
  --title "你的视频标题" \
  --desc "你的视频描述" \
  --lang en

# 上传视频（带标签）
sau kingsway upload-video \
  --account kingsway \
  --file /path/to/video.mp4 \
  --title "你的视频标题" \
  --desc "你的视频描述" \
  --tags "KingswayVideo,独立站,悬浮视频" \
  --lang en
