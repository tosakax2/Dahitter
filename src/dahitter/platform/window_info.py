"""Windows 上でゲームウィンドウを取得するヘルパモジュール"""

import win32gui
import win32process
import psutil


# ============================================================
GAME_PROCESS_NAMES = {
    "mahjong_soul": "Jantama_MahjongSoul.exe",
    "riichi_city": "Mahjong-JP.exe",
}

def find_game_window(game: str = "mahjong_soul") -> int:
    """指定ゲームのウィンドウハンドルを返す"""
    target_name = GAME_PROCESS_NAMES.get(game)
    if not target_name:
        raise ValueError(f"未対応のゲーム指定: {game}")

    windows = []

    def enum_windows_callback(hwnd, windows):
        if not win32gui.IsWindowVisible(hwnd):
            return
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            proc = psutil.Process(pid)
            if proc.name() == target_name:
                windows.append(hwnd)
        except psutil.NoSuchProcess:
            pass

    # ============================================================
    # --- ウィンドウ列挙 ---
    win32gui.EnumWindows(enum_windows_callback, windows)

    if not windows:
        raise RuntimeError(f"{target_name} のウィンドウが見つかりません")

    # --- 最初に見つかったウィンドウを返す ---
    return windows[0]

def get_client_rect(hwnd: int) -> tuple[int, int, int, int]:
    """クライアント矩形をスクリーン座標で取得する"""

    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    # --- クライアント座標をスクリーン座標へ変換 ---
    point = win32gui.ClientToScreen(hwnd, (left, top))
    width = right - left
    height = bottom - top
    return (point[0], point[1], point[0] + width, point[1] + height)
