"""テンプレートマッチングで牌を認識するモジュール"""

import os
import cv2
import numpy as np
from PIL import Image
from src.dahitter.config import AKA_DORA_RED_THRESHOLD, SCORE_THRESHOLD

TEMPLATE_CACHE: dict[str, dict[str, np.ndarray]] = {}


def _load_templates(template_dir: str) -> dict[str, np.ndarray]:
    """テンプレート画像を辞書形式で読み込む"""
    templates: dict[str, np.ndarray] = {}
    for fname in os.listdir(template_dir):
        if not fname.endswith(".png"):
            continue
        path = os.path.join(template_dir, fname)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            name = os.path.splitext(fname)[0]
            templates[name] = img
    return templates


def _get_templates(template_dir: str) -> dict[str, np.ndarray]:
    """テンプレート画像をキャッシュして取得する"""
    if template_dir not in TEMPLATE_CACHE:
        TEMPLATE_CACHE[template_dir] = _load_templates(template_dir)
    return TEMPLATE_CACHE[template_dir]

def is_aka(tile_img: Image.Image) -> bool:
    """牌画像が赤ドラかどうかを判定する"""
    tile_cv = np.array(tile_img)
    hsv = cv2.cvtColor(tile_cv, cv2.COLOR_RGB2HSV)
    mask1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
    mask2 = cv2.inRange(hsv, (160, 100, 100), (179, 255, 255))
    mask = cv2.bitwise_or(mask1, mask2)
    ratio = np.sum(mask > 0) / mask.size
    return ratio > AKA_DORA_RED_THRESHOLD

def recognize_tile(tile_img: Image.Image, template_dir: str) -> tuple[str | None, float | None]:
    """牌画像をテンプレートマッチングで認識する"""
    tile_cv = cv2.cvtColor(np.array(tile_img), cv2.COLOR_RGB2GRAY)
    aka = is_aka(tile_img)

    best_score = None
    best_name = None

    templates = _get_templates(template_dir)

    for name, temp in templates.items():
        if name == "unknown":
            continue

        # --- 赤ドラ選別 ---
        is_five = name.endswith("5") or name.endswith("5r")
        if is_five:
            if aka and name.endswith("5r"):
                pass
            elif not aka and name.endswith("5"):
                pass
            else:
                continue

        if temp.shape != tile_cv.shape:
            continue

        res = cv2.matchTemplate(tile_cv, temp, cv2.TM_CCOEFF_NORMED)
        score = res.max()
        if best_score is None or score > best_score:
            best_score = score
            best_name = name

    if best_score is None or best_score < SCORE_THRESHOLD:
        return None, best_score

    return best_name, best_score
