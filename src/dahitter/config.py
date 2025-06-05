"""アプリケーション設定を管理するモジュール"""

import os
import sys


def resource_path(relative_path: str) -> str:
    """ビルド環境に応じてリソースへのパスを返す"""
    base = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base, relative_path)

# ============================================================
# --- リソースパス定義 ---
ICON_PATH = resource_path("src/dahitter/icons/icon.ico")
ARROW_DOWN_PATH = resource_path("src/dahitter/icons/arrow_drop_down.svg")

BASE_TEMPLATE_DIR = resource_path("templates")
TEMPLATE_DIRS = {
    "mahjong_soul": os.path.join(BASE_TEMPLATE_DIR, "mahjong_soul"),
    "riichi_city": os.path.join(BASE_TEMPLATE_DIR, "riichi_city"),
}

# ============================================================
# --- 認識パラメータ ---
SCORE_THRESHOLD = 0.50

# --- 赤ドラ判定のHSVマスク閾値 ---
AKA_DORA_RED_THRESHOLD = 0.10

# ============================================================
# --- 牌関連の定数 ---
TILE_KIND_COUNT = 34
MAX_TILE_DUPLICATE = 4

# ============================================================
# --- 画面キャプチャ位置設定 ---
HAND_CROP_RATIOS = {
    "mahjong_soul": {
        "my_hand_left": 221 / 1920,
        "my_hand_right": 1456 / 1920,
        "my_hand_top": 921 / 1080,
        "my_hand_bottom": 1072 / 1080,
        "tsumo_left": 1486 / 1920,
    },
    "riichi_city": {
        "my_hand_left": 241 / 1920,
        "my_hand_right": 1606 / 1920,
        "my_hand_top": 903 / 1080,
        "my_hand_bottom": 1060 / 1080,
        "tsumo_left": 1653 / 1920,
    },
}
