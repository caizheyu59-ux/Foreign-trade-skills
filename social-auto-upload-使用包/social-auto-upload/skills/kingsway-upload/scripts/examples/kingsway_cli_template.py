"""
Kingsway 视频上传 CLI 模板（Python）

通过 subprocess 调用 sau CLI，或使用 Python 直接调用 Kingsway API。
"""

import subprocess
import sys
from pathlib import Path

SAU_DIR = Path(__file__).parent.parent.parent.parent


def upload_video_sau_cli(video_path: str, title: str, desc: str, account: str = "kingsway", lang: str = "en"):
    """通过 sau CLI 上传视频到 Kingsway"""
    cmd = [
        sys.executable, "-m", "sau_cli",
        "kingsway", "upload-video",
        "--account", account,
        "--file", video_path,
        "--title", title,
        "--desc", desc,
        "--lang", lang,
    ]
    result = subprocess.run(cmd, cwd=SAU_DIR, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 上传成功: {result.stdout}")
    else:
        print(f"❌ 上传失败: {result.stderr}")
    return result.returncode == 0


def upload_video_direct(video_path: str, title: str, desc: str, account: str = "kingsway", lang: str = "en"):
    """直接调用 Kingsway API（不经过 CLI）"""
    sys.path.insert(0, str(SAU_DIR))
    from uploader.kingsway_uploader.main import upload_kingsway_video, KingswayVideoUploadRequest
    import asyncio

    req = KingswayVideoUploadRequest(
        account_name=account,
        video_file=video_path,
        title=title,
        description=desc,
        lang=lang,
    )
    result = asyncio.run(upload_kingsway_video(req))
    if result.get("success"):
        print(f"✅ 上传成功: videoId={result.get('sourceVideoId')}")
    else:
        print(f"❌ 上传失败: {result}")
    return result.get("success")


if __name__ == "__main__":
    # 示例：上传视频
    VIDEO = "C:/Users/caizheyu/Desktop/test.mp4"
    TITLE = "一分钟教你学会在独立站做出悬浮视频"
    DESC = "第一步：创建组件 登录 KingswayVideo 后台，点击新建小部件。第二步：填充内容。第三步：一键部署。搞定！"

    upload_video_direct(VIDEO, TITLE, DESC, account="kingsway", lang="en")
