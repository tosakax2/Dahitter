"""ゲーム画面から牌画像を切り出す処理"""

from PIL import Image
from src.dahitter.gui.styles import TILE_WIDTH, TILE_HEIGHT
from src.dahitter.config import HAND_CROP_RATIOS


def crop_my_hand_and_tsumo(game_img: Image.Image, game: str = "mahjong_soul") -> tuple[list[Image.Image], Image.Image]:
    """自分の手牌13枚とツモ牌を切り出す"""

    width, height = game_img.size

    if game not in HAND_CROP_RATIOS:
        raise ValueError("未対応のゲーム指定")

    # ============================================================
    # --- 切り出し位置計算 ---
    ratio = HAND_CROP_RATIOS[game]
    my_hand_left = int(width * ratio["my_hand_left"])
    my_hand_right = int(width * ratio["my_hand_right"])
    my_hand_top = int(height * ratio["my_hand_top"])
    my_hand_bottom = int(height * ratio["my_hand_bottom"])
    tsumo_left = int(width * ratio["tsumo_left"])

    # ============================================================
    # --- 手牌切り出し ---
    my_hand_img = game_img.crop((my_hand_left, my_hand_top, my_hand_right, my_hand_bottom))
    hand_width = my_hand_right - my_hand_left
    # --- 1枚あたりの幅計算 ---
    one_tile_width = hand_width // 13

    hand_imgs = []
    for i in range(13):
        left = int(hand_width * i / 13)
        right = int(hand_width * (i + 1) / 13)
        tile_img = my_hand_img.crop((left, 0, right, my_hand_img.size[1]))
        tile_img = tile_img.resize((TILE_WIDTH, TILE_HEIGHT), Image.LANCZOS)
        hand_imgs.append(tile_img)

    # ============================================================
    # --- ツモ牌切り出し ---
    tsumo_right = tsumo_left + one_tile_width
    tsumo_img = game_img.crop((tsumo_left, my_hand_top, tsumo_right, my_hand_bottom))
    tsumo_img = tsumo_img.resize((TILE_WIDTH, TILE_HEIGHT), Image.LANCZOS)

    return hand_imgs, tsumo_img
