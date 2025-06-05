"""GUI のスタイル定数を定義するモジュール"""

from .themes import *
from src.dahitter.config import ARROW_DOWN_PATH


# ============================================================
# --- タイルサイズ・角丸 ---
TILE_WIDTH = 62
TILE_HEIGHT = 100
TILE_RADIUS = 8

# ============================================================
# --- ウィンドウ全体のスタイル ---
WINDOW_STYLE = f"""
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_PRIMARY_COLOR};
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE_NORMAL}px;
"""

# ============================================================
# --- ヘッダー領域のスタイル ---
HEADER_STYLE = f"""
    background-color: {SURFACE_COLOR};
    border-bottom: 3px dashed {PRIMARY_COLOR};
"""

HEADER_TITLE_STYLE = f"""
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE_HEADER}px;
    font-weight: bold;
    color: {TEXT_PRIMARY_COLOR};
    border: 0;
"""

# ============================================================
# --- タイル領域 ---
TILE_AREA_STYLE = f"""
    border-radius: 8px;
    background-color: {SURFACE_COLOR};
"""

# ============================================================
# --- 手牌・待ち牌のボックススタイル ---
HAND_BOX_STYLE = f"""
    border: none;
    border-radius: 8px;
"""

# ============================================================
# --- カード状フレームのスタイル ---
CARD_STYLE = f"""
    border-radius: 8px;
    border: 2px solid {TEXT_SECONDARY_COLOR};
    background-color: {SURFACE_COLOR};
"""

# ============================================================
# --- ラベル表示スタイル ---
HAND_LABEL_STYLE = f"""
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE_NORMAL}px;
    font-weight: bold;
    border: 0;
    color: {TEXT_PRIMARY_COLOR};
    background-color: transparent;
    padding: 2px 0px 8px 2px;
"""

# ============================================================
# --- 状態ラベル ---
STATUS_LABEL_STYLE = f"""
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE_STATUS}px;
    font-weight: bold;
    color: {TEXT_PRIMARY_COLOR};
"""

ARROW_DOWN_SVG = ARROW_DOWN_PATH.replace("\\", "/")

COMBOBOX_STYLE = f"""
    QComboBox {{
        color: {TEXT_PRIMARY_COLOR};
        background-color: transparent;
        border: none;
        border-bottom: 2px solid {PRIMARY_COLOR};
        padding: 6px 32px 6px 8px;
        font-family: {FONT_FAMILY};
        font-size: {FONT_SIZE_NORMAL}px;
        min-width: 120px;
        border-radius: 0;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 24px;
        border: none;
        background: transparent;
    }}
    QComboBox::down-arrow {{
        image: url("{ARROW_DOWN_SVG}");
        width: 24px;
        height: 24px;
    }}
    QComboBox QAbstractItemView {{
        background: {MENU_BG_COLOR};
        color: {TEXT_PRIMARY_COLOR};
        selection-background-color: {PRIMARY_COLOR};
        selection-color: {WHITE_COLOR};
        border-radius: 4px;
        border: 2px solid {PRIMARY_COLOR};
        font-family: {FONT_FAMILY};
        font-size: {FONT_SIZE_POPUP}px;
        outline: none;
    }}
    QComboBox QAbstractItemView::item {{
        padding: 4px;
        outline: none;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: {PRIMARY_COLOR};
        color: {WHITE_COLOR};
        outline: none;
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: {PRIMARY_COLOR};
        color: {WHITE_COLOR};
        outline: none;
    }}
"""
