"""
Kingsway Video Uploader
Pure API-based upload (no browser automation).

Upload flow:
1. Pre-register video → sourceVideoId
2. Start heartbeat (every ≤10s, required)
3. Get presigned PUT URL
4. PUT video file to presigned URL
5. Notify upload success
6. Save SEO page (title, description)
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import requests

from utils.log import logger

KINGSWAY_CONFIG_DIR = Path(__file__).parent.parent.parent / "cookies" / "kingsway_config"
KINGSWAY_CONFIG_FILE = KINGSWAY_CONFIG_DIR / "local.json"

DEFAULT_BASE_URL = "https://api.kingswayvideo.com"


@dataclass
class KingswayConfig:
    api_key: str = ""
    base_url: str = DEFAULT_BASE_URL

    @classmethod
    def load(cls, account_name: str = "default") -> "KingswayConfig":
        config_file = KINGSWAY_CONFIG_DIR / f"{account_name}.json"
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(
                    api_key=data.get("apiKey", ""),
                    base_url=data.get("baseUrl", DEFAULT_BASE_URL),
                )
            except Exception as e:
                logger.warning(f"Failed to load Kingsway config {config_file}: {e}")

        # Fallback to shared local.json
        if KINGSWAY_CONFIG_FILE.exists():
            try:
                with open(KINGSWAY_CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(
                    api_key=data.get("apiKey", ""),
                    base_url=data.get("baseUrl", DEFAULT_BASE_URL),
                )
            except Exception as e:
                logger.warning(f"Failed to load Kingsway config {KINGSWAY_CONFIG_FILE}: {e}")

        return cls()

    def save(self, account_name: str = "default"):
        KINGSWAY_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config_file = KINGSWAY_CONFIG_DIR / f"{account_name}.json"
        data = {
            "apiKey": self.api_key,
            "baseUrl": self.base_url,
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @property
    def is_valid(self) -> bool:
        return bool(self.api_key) and self.api_key != "sk-在此填写你的 API Key"


def _make_headers(config: KingswayConfig) -> dict:
    return {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }


def pre_add_video(config: KingswayConfig, video_name: str, size: int) -> Optional[str]:
    """Step 1: Pre-register video, return sourceVideoId."""
    url = f"{config.base_url}/vod/video/pre-add-custom-video"
    body = {"videos": [{"videoName": video_name, "size": size}]}
    resp = requests.post(url, headers=_make_headers(config), json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"Pre-add response: {json.dumps(data, ensure_ascii=False)[:500]}")
    # Response structure may vary; try common patterns
    result = data.get("data", data)
    if isinstance(result, list):
        if result:
            item = result[0]
            return item if isinstance(item, str) else item.get("sourceVideoId")
    elif isinstance(result, dict):
        videos = result.get("videos", [])
        if videos:
            item = videos[0]
            return item if isinstance(item, str) else item.get("sourceVideoId")
    logger.error(f"Pre-add video response unexpected: {data}")
    return None


def start_heartbeat(config: KingswayConfig, source_video_id: str, stop_event=None):
    """Step 2: Heartbeat every ≤10s to keep upload alive."""
    url = f"{config.base_url}/vod/video/add-custom-video-heartbeat"
    while stop_event is None or not stop_event.is_set():
        try:
            body = {"videos": [{"sourceVideoId": source_video_id, "uploadPercent": 0.1}]}
            requests.post(url, headers=_make_headers(config), json=body, timeout=10)
        except Exception as e:
            logger.warning(f"Heartbeat failed: {e}")
        if stop_event:
            stop_event.wait(8)
        else:
            time.sleep(8)


def get_presigned_url(config: KingswayConfig, source_video_id: str) -> Optional[dict]:
    """Step 3: Get presigned PUT URL and videoUrl."""
    url = f"{config.base_url}/vod/video/presigned-put-upload-url"
    body = {"sourceVideoId": source_video_id, "expiresInSeconds": 3600}
    resp = requests.post(url, headers=_make_headers(config), json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"Presigned URL response: {json.dumps(data, ensure_ascii=False)[:500]}")
    result = data.get("data", data)
    if isinstance(result, dict):
        presigned_url = result.get("presignedPutUrl")
        video_url = result.get("videoUrl", "")
        if presigned_url:
            return {"presignedPutUrl": presigned_url, "videoUrl": video_url}
    # Try nested data
    if isinstance(data, dict) and "data" in data:
        inner = data["data"]
        if isinstance(inner, dict) and inner.get("presignedPutUrl"):
            return {"presignedPutUrl": inner["presignedPutUrl"], "videoUrl": inner.get("videoUrl", "")}
    logger.error(f"Presigned URL response unexpected: {data}")
    return None


def upload_video_file(presigned_url: str, file_path: str) -> bool:
    """Step 4: PUT video file to presigned URL."""
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            resp = requests.put(
                presigned_url,
                data=f,
                headers={"Content-Length": str(file_size)},
                timeout=3600,
            )
        if resp.status_code == 200:
            return True
        logger.error(f"Upload PUT failed: status={resp.status_code}, body={resp.text[:500]}")
        return False
    except Exception as e:
        logger.error(f"Upload PUT exception: {e}")
        return False


def notify_success(config: KingswayConfig, source_video_id: str, video_url: str) -> bool:
    """Step 5: Notify upload success."""
    url = f"{config.base_url}/vod/video/add-custom-video-success"
    body = {"sourceVideoId": source_video_id, "videoUrl": video_url}
    resp = requests.post(url, headers=_make_headers(config), json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"Upload success notification: {data}")
    return True


def notify_fail(config: KingswayConfig, source_video_id: str, fail_reason: str = ""):
    """Notify upload failure."""
    url = f"{config.base_url}/vod/video/add-custom-video-fail"
    body = {"sourceVideoId": source_video_id, "failReason": fail_reason}
    try:
        requests.post(url, headers=_make_headers(config), json=body, timeout=10)
    except Exception:
        pass


def save_seo_page(config: KingswayConfig, video_id: str, title: str, description: str, lang: str = "en") -> bool:
    """Step 6: Save SEO page (title, description)."""
    url = f"{config.base_url}/vod/player/save-video-seo-page"
    body = {
        "videoId": video_id,
        "seoPage": [
            {
                "lang": lang,
                "title": title,
                "description": description,
            }
        ],
    }
    resp = requests.post(url, headers=_make_headers(config), json=body, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"SEO page saved: {data}")
    return True


@dataclass
class KingswayVideoUploadRequest:
    account_name: str
    video_file: str
    title: str
    description: str
    tags: list[str] = field(default_factory=list)
    lang: str = "en"


async def upload_kingsway_video(request: KingswayVideoUploadRequest) -> dict:
    """Main upload flow for Kingsway."""
    import threading

    config = KingswayConfig.load(request.account_name)
    if not config.is_valid:
        raise RuntimeError(
            f"Kingsway API key is not configured for account '{request.account_name}'. "
            f"Please save your API key to: {KINGSWAY_CONFIG_DIR / f'{request.account_name}.json'}\n"
            f"Format: {{\"apiKey\": \"sk-xxx\", \"baseUrl\": \"https://api.kingswayvideo.com\"}}"
        )

    video_path = Path(request.video_file)
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    file_size = video_path.stat().st_size
    video_name = video_path.name

    # Step 1: Pre-register
    logger.info(f"[Kingsway] Step 1: Pre-registering video: {video_name}")
    source_video_id = pre_add_video(config, video_name, file_size)
    if not source_video_id:
        raise RuntimeError("Failed to pre-register video")
    logger.info(f"[Kingsway] sourceVideoId: {source_video_id}")

    # Step 2: Start heartbeat in background
    stop_event = threading.Event()
    heartbeat_thread = threading.Thread(
        target=start_heartbeat, args=(config, source_video_id, stop_event), daemon=True
    )
    heartbeat_thread.start()
    logger.info("[Kingsway] Step 2: Heartbeat started")

    try:
        # Step 3: Get presigned URL
        logger.info("[Kingsway] Step 3: Getting presigned URL")
        url_info = get_presigned_url(config, source_video_id)
        if not url_info:
            raise RuntimeError("Failed to get presigned URL")
        presigned_url = url_info["presignedPutUrl"]
        video_url = url_info["videoUrl"]

        # Step 4: Upload video file
        logger.info(f"[Kingsway] Step 4: Uploading video ({file_size} bytes)")
        success = upload_video_file(presigned_url, str(video_path))
        if not success:
            notify_fail(config, source_video_id, "Upload PUT failed")
            raise RuntimeError("Failed to upload video file")

        # Step 5: Notify success
        logger.info("[Kingsway] Step 5: Notifying upload success")
        notify_success(config, source_video_id, video_url)

        # Step 6: Save SEO page
        if request.title or request.description:
            logger.info("[Kingsway] Step 6: Saving SEO page")
            save_seo_page(
                config,
                video_id=source_video_id,
                title=request.title,
                description=request.description,
                lang=request.lang,
            )

        logger.info(f"[Kingsway] Upload complete! videoId: {source_video_id}")
        return {
            "success": True,
            "sourceVideoId": source_video_id,
            "videoUrl": video_url,
        }

    finally:
        stop_event.set()
        heartbeat_thread.join(timeout=5)


def check_kingsway_config(account_name: str) -> bool:
    """Check if Kingsway API key is configured and valid."""
    config = KingswayConfig.load(account_name)
    return config.is_valid


def setup_kingsway_config(account_name: str, api_key: str, base_url: str = DEFAULT_BASE_URL):
    """Save Kingsway API config."""
    config = KingswayConfig(api_key=api_key, base_url=base_url)
    config.save(account_name)
    return config
