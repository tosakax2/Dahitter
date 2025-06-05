"""Dahitter アプリケーションを起動するモジュール"""

import sys
from src.dahitter.gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication


def main():
    """Qt アプリケーションを初期化してメインウィンドウを表示する"""

    app = QApplication(sys.argv)

    win = MainWindow()
    win.adjustSize()

    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # --- エントリーポイント ---
    main()
