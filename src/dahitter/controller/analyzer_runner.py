"""ゲーム画面を解析して牌情報を取得するモジュール"""

from src.dahitter.platform.window_info import find_game_window, get_client_rect
from src.dahitter.vision.capture import capture_window
from src.dahitter.vision.cropper import crop_my_hand_and_tsumo
from src.dahitter.vision.matcher import recognize_tile
from src.dahitter.logic.analyzer import (
    analyze_hand_with_ukeire,
    convert_hand_to_34,
    calc_ukeire34,
)
from mahjong.shanten import Shanten
from src.dahitter.config import TEMPLATE_DIRS

def analyze_current_state(game_code: str) -> dict:
    """現在のゲーム画面から手牌状況を解析して返す"""

    # ============================================================
    # --- 画面キャプチャ ---
    hwnd = find_game_window(game_code)
    rect = get_client_rect(hwnd)
    img = capture_window(rect)
    hand_imgs, tsumo_img = crop_my_hand_and_tsumo(img, game_code)

    # ============================================================
    # --- 画像認識 ---
    template_dir = TEMPLATE_DIRS[game_code]
    hand_names = []
    for tile in hand_imgs:
        name, score = recognize_tile(tile, template_dir)
        hand_names.append(name if name else "?")

    tsumo_name, _ = recognize_tile(tsumo_img, template_dir)
    tsumo_name = tsumo_name or "?"

    # ============================================================
    # --- 向聴計算 ---
    hand34 = convert_hand_to_34(hand_names)
    base_shanten = Shanten().calculate_shanten(hand34)
    ukeire_tile_indices, _ = calc_ukeire34(hand34, base_shanten)
    from src.dahitter.logic.analyzer import tile34_to_name
    ukeire_names = [tile34_to_name(i) for i in ukeire_tile_indices]

    # --- 打牌候補ごとの向聴数計算 (ツモ牌を含める) ---
    all_tiles = hand_names + [tsumo_name]
    _, raw_candidates = analyze_hand_with_ukeire(all_tiles)

    # 向聴前後の情報を candidate に付加する
    candidates = []
    for c in raw_candidates:
        c["shanten_before"] = base_shanten
        c["shanten_after"] = c.get("shanten", base_shanten)  # fallback safety
        candidates.append(c)

    # --- 和了判定 ---
    is_agari = False
    if tsumo_name != "?" and base_shanten == 0:
        is_agari = tsumo_name in ukeire_names

    # ============================================================
    # --- 結果生成 ---
    return {
        "hand_images": hand_imgs,
        "tsumo_image": tsumo_img,
        "hand_names": hand_names,
        "tsumo_name": tsumo_name,
        "shanten": base_shanten,
        "candidates": candidates,
        "ukeire_names": ukeire_names,
        "is_agari": is_agari,
    }
