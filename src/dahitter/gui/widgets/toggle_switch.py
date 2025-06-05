"""シンプルなトグルスイッチウィジェット"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, Signal, Property
from PySide6.QtGui import QPainter, QColor, QBrush
from src.dahitter.gui.styles.themes import PRIMARY_COLOR, INACTIVE_COLOR, WHITE_COLOR


class ToggleSwitch(QWidget):
    """ON/OFF を表すカスタムスイッチ"""

    toggled = Signal(bool)

    def __init__(self, parent=None):
        """ウィジェットを初期化する"""
        super().__init__(parent)
        self.setFixedSize(QSize(50, 28))
        self._checked = False
        self.__knob_x = 2
        self.setCursor(Qt.PointingHandCursor)

        self._anim = QPropertyAnimation(self, b"_knob_x", self)
        self._anim.setDuration(150)

    def mousePressEvent(self, event):
        """クリック時に状態を切り替える"""
        # ============================================================
        # --- 状態反転 ---
        self._checked = not self._checked
        start = self.__knob_x
        end = self.width() - 26 if self._checked else 2

        # --- アニメーション開始 ---
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

        self.toggled.emit(self._checked)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        """スイッチを描画する"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # ============================================================
        # --- 背景描画 ---
        bg_color = QColor(PRIMARY_COLOR) if self._checked else QColor(INACTIVE_COLOR)
        p.setBrush(QBrush(bg_color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 14, 14)

        # --- ノブ描画 ---
        knob_rect = QRect(int(self.__knob_x), 2, 24, 24)
        p.setBrush(QBrush(QColor(WHITE_COLOR)))
        p.drawEllipse(knob_rect)

    def sizeHint(self):
        """推奨サイズを返す"""
        return QSize(50, 28)

    def isChecked(self):
        """チェック状態を返す"""
        return self._checked

    def setChecked(self, checked: bool):
        """チェック状態を設定する"""
        if self._checked != checked:
            self._checked = checked
            self.__knob_x = self.width() - 26 if checked else 2
            self.update()

    def _set_knob_x(self, value):
        """アニメーション用の内部値を設定する"""
        self.__knob_x = value
        self.update()

    def _get_knob_x(self):
        """アニメーション用の内部値を取得する"""
        return self.__knob_x

    _knob_x = Property(float, _get_knob_x, _set_knob_x)
