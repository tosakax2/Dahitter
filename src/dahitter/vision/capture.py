"""画面キャプチャを行うユーティリティ"""

from typing import Tuple
import mss
from PIL import Image


def capture_window(rect: Tuple[int, int, int, int]) -> Image.Image:
    """指定領域をキャプチャして ``PIL.Image`` を返す"""
    # ============================================================
    # --- 矩形情報展開 ---
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top

    # --- mss でキャプチャ ---
    with mss.mss() as sct:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
