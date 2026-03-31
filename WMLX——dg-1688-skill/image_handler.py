#!/usr/bin/env python3
"""
图片处理模块
负责图片下载、格式转换、等比缩放
"""

import os
import hashlib
import requests
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
from io import BytesIO


def _is_valid_image_file(path: str) -> bool:
    """判断本地文件是否为可识别图片"""
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def _crop_top_pixels(image_path: str, crop_top_px: int = 100) -> Optional[str]:
    """裁剪图片顶部固定像素，返回裁剪后的新路径。"""
    if not os.path.exists(image_path):
        return None
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            # 图片太矮时不裁，避免裁空
            if h <= crop_top_px + 10:
                return image_path
            cropped = img.crop((0, crop_top_px, w, h))
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            out_path = os.path.join(os.path.dirname(image_path), f"{base_name}_crop.png")
            if cropped.mode not in ("RGB", "RGBA"):
                cropped = cropped.convert("RGB")
            cropped.save(out_path, "PNG")
            return out_path
    except Exception as e:
        print(f"Warning: Failed to crop image top {crop_top_px}px: {e}")
        return None


def download_image(url: str, temp_dir: str = "./tmp/images") -> Optional[str]:
    """
    下载网络图片到本地临时目录

    Args:
        url: 图片 URL
        temp_dir: 临时存储目录

    Returns:
        下载后的本地文件路径，失败返回 None
    """
    if not url or not url.startswith(('http://', 'https://')):
        return None

    try:
        # 创建临时目录
        os.makedirs(temp_dir, exist_ok=True)

        # 生成唯一文件名
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        ext = _get_extension_from_url(url)
        local_path = os.path.join(temp_dir, f"{url_hash}{ext}")

        # 如果文件已存在且可用，直接返回；坏缓存则删除后重下
        if os.path.exists(local_path):
            if _is_valid_image_file(local_path):
                return local_path
            try:
                os.remove(local_path)
            except OSError:
                pass

        # 下载图片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # 避免使用系统代理（当前环境代理会对 alicdn 返回 403）
        session = requests.Session()
        session.trust_env = False
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        content_type = (response.headers.get("content-type") or "").lower()
        if "image" not in content_type:
            print(f"Warning: Non-image response for {url}: content-type={content_type}")
            return None

        with open(local_path, 'wb') as f:
            f.write(response.content)

        # 防止服务端返回了伪装图片的文本/错误页
        if not _is_valid_image_file(local_path):
            try:
                os.remove(local_path)
            except OSError:
                pass
            print(f"Warning: Downloaded file is not a valid image: {url}")
            return None

        return local_path

    except Exception as e:
        print(f"Warning: Failed to download image from {url}: {e}")
        return None


def convert_to_png(image_path: str, temp_dir: str = "./tmp/images") -> Optional[str]:
    """
    将图片转换为 PNG 格式（支持 WebP、AVIF 等非常规格式）

    Args:
        image_path: 原始图片路径
        temp_dir: 输出目录

    Returns:
        转换后的 PNG 文件路径，失败返回 None
    """
    if not os.path.exists(image_path):
        return None

    try:
        # 如果已经是 PNG，直接返回
        if image_path.lower().endswith('.png'):
            return image_path

        # 打开图片并转换为 PNG
        with Image.open(image_path) as img:
            # 转换为 RGB（处理透明通道）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                else:
                    img = img.convert('RGB')
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # 生成 PNG 路径
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            png_path = os.path.join(temp_dir, f"{base_name}.png")

            img.save(png_path, 'PNG')
            return png_path

    except Exception as e:
        print(f"Warning: Failed to convert image to PNG: {e}")
        return None


def resize_for_excel(image_path: str, max_size: int = 90) -> Tuple[Optional[str], int, int]:
    """
    等比缩放图片以适应 Excel 单元格

    Args:
        image_path: 图片路径
        max_size: 最大尺寸（像素）

    Returns:
        (缩放后的图片路径, 实际宽度, 实际高度)
        失败返回 (None, 0, 0)
    """
    if not os.path.exists(image_path):
        return None, 0, 0

    try:
        with Image.open(image_path) as img:
            width, height = img.size

            # 计算缩放比例
            scale = min(max_size / width, max_size / height)

            if scale < 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)

                # 缩放图片
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # 保存到临时目录
                temp_dir = os.path.dirname(image_path)
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                resized_path = os.path.join(temp_dir, f"{base_name}_resized.png")

                # 确保 RGB 模式
                if img_resized.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img_resized.size, (255, 255, 255))
                    if img_resized.mode == 'P':
                        img_resized = img_resized.convert('RGBA')
                    if img_resized.mode in ('RGBA', 'LA'):
                        background.paste(img_resized, mask=img_resized.split()[-1])
                        img_resized = background
                    else:
                        img_resized = img_resized.convert('RGB')
                elif img_resized.mode != 'RGB':
                    img_resized = img_resized.convert('RGB')

                img_resized.save(resized_path, 'PNG')
                return resized_path, new_width, new_height
            else:
                # 不需要缩放，但确保是 PNG 格式
                if not image_path.lower().endswith('.png'):
                    return convert_to_png(image_path), width, height
                return image_path, width, height

    except Exception as e:
        print(f"Warning: Failed to resize image: {e}")
        return None, 0, 0


def process_image_for_excel(image_url: str, temp_dir: str = "./tmp/images") -> Tuple[Optional[str], int, int]:
    """
    全流程处理图片：下载 → 转换 → 缩放

    Args:
        image_url: 图片 URL 或本地路径
        temp_dir: 临时目录

    Returns:
        (最终图片路径, 宽度, 高度)，失败返回 (None, 0, 0)
    """
    # 如果是本地路径
    if os.path.exists(image_url):
        local_path = image_url
    else:
        # 下载网络图片
        local_path = download_image(image_url, temp_dir)

    if not local_path:
        return None, 0, 0

    # 转换为 PNG（仅在格式不兼容时转换，不做尺寸压缩）
    final_path = local_path
    if not local_path.lower().endswith((".png", ".jpg", ".jpeg")):
        png_path = convert_to_png(local_path, temp_dir)
        if not png_path:
            return None, 0, 0
        final_path = png_path

    # 按规则裁掉顶部 100px 编码区，再写入 Excel（不改变宽高比）
    cropped_path = _crop_top_pixels(final_path, crop_top_px=100)
    if cropped_path:
        final_path = cropped_path

    # 读取最终图尺寸，交给 Excel 显示层做等比缩放，不改图片文件像素
    try:
        with Image.open(final_path) as img:
            width, height = img.size
    except Exception as e:
        print(f"Warning: Failed to read image size: {e}")
        return None, 0, 0

    return final_path, width, height


def _get_extension_from_url(url: str) -> str:
    """从 URL 提取文件扩展名"""
    # 移除查询参数
    clean_url = url.split('?')[0].split('#')[0]

    # 提取扩展名
    ext = os.path.splitext(clean_url)[1].lower()

    # 默认扩展名
    if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.bmp']:
        ext = '.jpg'

    return ext


if __name__ == "__main__":
    # 简单测试
    print("Testing image handler...")

    # 测试本地路径处理
    print("\nTest 1: Process local path")
    # 创建一个测试图片
    test_img = Image.new('RGB', (200, 150), color='red')
    test_path = "./tmp/images/test_original.jpg"
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    test_img.save(test_path, 'JPEG')

    result, w, h = process_image_for_excel(test_path)
    print(f"  Result: {result}")
    print(f"  Dimensions: {w}x{h}")

    # 清理
    if result and os.path.exists(result):
        os.remove(result)
    if os.path.exists(test_path):
        os.remove(test_path)

    print("\nImage handler tests completed!")
