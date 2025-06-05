"""テンプレート画像を生成するツール"""

import os
from src.dahitter.platform.window_info import find_game_window, get_client_rect
from src.dahitter.vision.capture import capture_window
from src.dahitter.vision.cropper import crop_my_hand_and_tsumo


def main():
    """ゲーム画面をキャプチャしてテンプレートを保存する"""

    APPS = {
        "1": ("雀魂", "mahjong_soul"),
        "2": ("麻雀一番街", "riichi_city"),
    }

    # ============================================================
    # --- アプリ選択 ---
    print("どちらのアプリの牌画像を分割しますか？")
    for k, (label, _) in APPS.items():
        print(f"{k}: {label}")

    sel = input("番号を入力してください: ").strip()
    if sel not in APPS:
        print("不正な選択です。終了します。")
        return

    app_label, game = APPS[sel]
    print(f"{app_label} ({game}) のウィンドウをキャプチャします...")

    # ============================================================
    # --- キャプチャ処理 ---
    try:
        hwnd = find_game_window(game)
        rect = get_client_rect(hwnd)
        img = capture_window(rect)

        hand_imgs, tsumo_img = crop_my_hand_and_tsumo(img, game)

        out_dir = os.path.join(os.getcwd(), "captured_tiles")
        os.makedirs(out_dir, exist_ok=True)

        for i, tile_img in enumerate(hand_imgs):
            tile_img.save(os.path.join(out_dir, f"hand_{i + 1:02d}.png"))
        tsumo_img.save(os.path.join(out_dir, "tsumo.png"))

        print(f"\n保存完了: {out_dir}/hand_01.png ～ hand_13.png, tsumo.png")

    except Exception as e:
        # --- 例外処理 ---
        print(f"エラー: {e}")

if __name__ == "__main__":
    main()
