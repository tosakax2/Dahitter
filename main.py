"""Dahitter アプリケーションを起動するモジュール"""

import sys
import traceback
import ctypes
from src.dahitter.gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication


def main():
    """Qt アプリケーションを初期化してメインウィンドウを表示する"""

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        app = QApplication(sys.argv)
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
    except Exception:
        with open("error.log", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)


if __name__ == "__main__":
    # --- エントリーポイント ---
    main()
