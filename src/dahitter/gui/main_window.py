"""Dahitter のメインウィンドウを実装するモジュール"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QComboBox, QSizePolicy
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
from PySide6.QtCore import QTimer, Qt
from src.dahitter.gui.styles.themes import (
    ERROR_COLOR,
    DISABLED_COLOR,
    WARNING_COLOR,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    TEXT_PRIMARY_COLOR,
    FONT_FAMILY,
    FONT_SIZE_STATUS,
    FONT_SIZE_NORMAL,
)
from src.dahitter.gui.widgets.toggle_switch import ToggleSwitch
from src.dahitter.controller.analyzer_runner import analyze_current_state
from src.dahitter.config import TEMPLATE_DIRS
from src.dahitter.gui.styles import (
    WINDOW_STYLE, HEADER_STYLE, HEADER_TITLE_STYLE,
    COMBOBOX_STYLE,
    HAND_BOX_STYLE, CARD_STYLE, HAND_LABEL_STYLE, STATUS_LABEL_STYLE,
    TILE_WIDTH, TILE_HEIGHT, TILE_RADIUS,
)
from PIL.ImageQt import ImageQt
from PIL import Image
import os
from src.dahitter.config import ICON_PATH


class MainWindow(QWidget):
    """牌解析結果を表示するウィンドウクラス"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dahitter - 麻雀アシストツール")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setStyleSheet(WINDOW_STYLE)
        self.game_code = "mahjong_soul"

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_widget.setStyleSheet(HEADER_STYLE)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(24, 12, 24, 12)

        header_title = QLabel("Dahitter - 麻雀アシストツール")
        header_title.setStyleSheet(HEADER_TITLE_STYLE)
        header_layout.addWidget(header_title)

        self.combo = QComboBox()
        self.combo.addItems(["雀魂", "麻雀一番街"])
        self.combo.setStyleSheet(COMBOBOX_STYLE)
        self.combo.setFixedWidth(160)
        self.combo.currentIndexChanged.connect(self.on_game_changed)
        header_layout.addWidget(self.combo)

        self.toggle = ToggleSwitch()
        self.toggle.toggled.connect(self.on_toggle)
        header_layout.addWidget(self.toggle)

        self.main_layout.addWidget(header_widget)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # ============================================================
        # --- 手牌フレーム ---
        self.hand_frame = QFrame(self)
        self.hand_frame.setStyleSheet(CARD_STYLE)
        hand_frame_layout = QVBoxLayout()
        hand_frame_layout.setContentsMargins(8, 8, 8, 8)
        self.hand_frame.setLayout(hand_frame_layout)

        self.hand_label = QLabel("あなたの手牌")
        self.hand_label.setStyleSheet(HAND_LABEL_STYLE)
        hand_frame_layout.addWidget(self.hand_label, alignment=Qt.AlignLeft)

        self.hand_box = QFrame()
        self.hand_box.setStyleSheet(HAND_BOX_STYLE)
        hand_layout = QHBoxLayout()
        self.hand_box.setLayout(hand_layout)
        hand_frame_layout.addWidget(self.hand_box)

        # ============================================================
        # --- 待ち牌フレーム ---
        self.wait_frame = QFrame(self)
        self.wait_frame.setStyleSheet(CARD_STYLE)
        wait_frame_layout = QVBoxLayout()
        wait_frame_layout.setContentsMargins(8, 8, 8, 8)
        self.wait_frame.setLayout(wait_frame_layout)

        self.wait_label = QLabel("待ち牌")
        self.wait_label.setStyleSheet(HAND_LABEL_STYLE)
        wait_frame_layout.addWidget(self.wait_label, alignment=Qt.AlignLeft)

        wait_content_layout = QHBoxLayout()
        wait_content_layout.setSpacing(16)
        wait_frame_layout.addLayout(wait_content_layout)

        self.wait_box = QFrame()
        self.wait_box.setStyleSheet(HAND_BOX_STYLE)
        wait_layout = QHBoxLayout()
        wait_layout.setAlignment(Qt.AlignLeft)
        self.wait_box.setLayout(wait_layout)
        wait_content_layout.addWidget(self.wait_box)

        # ============================================================
        # --- ステータスフレーム ---
        self.status_frame = QFrame(self)
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(16, 16, 16, 16)
        self.status_frame.setLayout(status_layout)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)

        # ============================================================
        # --- 待ち牌フレームとステータスフレーム ---
        wait_status_widget = QWidget()
        wait_status_layout = QHBoxLayout(wait_status_widget)
        wait_status_layout.setContentsMargins(16, 16, 16, 16)
        wait_status_layout.setSpacing(16)
        wait_status_layout.addWidget(self.wait_frame)
        wait_status_layout.addWidget(self.status_frame)

        # --- 手牌フレームをラップ ---
        hand_wrapper = QWidget()
        hand_wrapper_layout = QVBoxLayout(hand_wrapper)
        hand_wrapper_layout.setContentsMargins(16, 16, 16, 16)
        hand_wrapper_layout.addWidget(self.hand_frame)

        # --- 作成したフレームを配置 ---
        content_layout.addWidget(hand_wrapper)
        content_layout.addWidget(wait_status_widget)

        self.main_layout.addWidget(content_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_analysis)

        self.adjustSize()
        self.setFixedSize(self.sizeHint())

        self.show_unknown_tiles()

    def on_game_changed(self, index):
        """ゲーム選択が変更されたときに実行する"""
        label = self.combo.currentText()
        self.game_code = "mahjong_soul" if label == "雀魂" else "riichi_city"
        self.show_unknown_tiles()

    def on_toggle(self, checked):
        """解析の開始と停止を切り替える"""
        if checked:
            self.timer.start(500)
        else:
            self.timer.stop()

    def start_analysis(self):
        """画面を解析して表示を更新する"""
        # ============================================================
        # --- 解析処理 ---
        self.result = analyze_current_state(self.game_code)
        if not self.result:
            self.update_status("解析失敗", ERROR_COLOR)
            return

        shanten = self.result.get("shanten", -1)
        is_agari = self.result.get("is_agari", False)
        candidates = self.result.get("candidates", [])
        wait_tiles = []

        if is_agari:
            status = "和了！"
            color = SECONDARY_COLOR
            wait_tiles = self.result.get("ukeire_names", [])
            show_candidates = []
        elif shanten == 0:
            status = "聴牌"
            color = PRIMARY_COLOR
            wait_tiles = self.result.get("ukeire_names", [])
            show_candidates = candidates
        else:
            status = f"{shanten}向聴" if shanten > 0 else "?"
            color = TEXT_PRIMARY_COLOR if shanten == 1 else DISABLED_COLOR
            wait_tiles = []
            show_candidates = candidates

        self.update_status(status, color)

        self.show_tiles(
            self.result["hand_names"],
            self.result["tsumo_name"],
            wait_tiles,
            show_candidates,
            shanten,
        )

    def update_status(self, text, color=DISABLED_COLOR):
        """ステータスバーの文言と色を更新する"""
        self.status_label.setText(text)
        self.status_label.setStyleSheet(
            f"font-size: {FONT_SIZE_STATUS}px; font-weight: bold; "
            f"font-family: {FONT_FAMILY}; color: {color};"
        )

    def get_unknown_tile_path(self):
        """不明牌画像のパスを返す"""
        return os.path.join(TEMPLATE_DIRS[self.game_code], "unknown.png")

    def show_unknown_tiles(self):
        """空の手牌表示を初期化する"""
        # ============================================================
        # --- 未解析表示 ---
        hand_layout = self.hand_box.layout()
        while hand_layout.count():
            item = hand_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        wait_layout = self.wait_box.layout()
        while wait_layout.count():
            item = wait_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        unknown_img = self.tile_to_pixmap("?")

        for _ in range(13):
            wrapper = QWidget()
            wrapper.setStyleSheet("border: none; background-color: transparent;")
            v = QVBoxLayout(wrapper)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(4)

            label = QLabel()
            label.setPixmap(unknown_img)
            label.setStyleSheet("border: none; background-color: transparent;")
            num_label = QLabel("")
            num_label.setAlignment(Qt.AlignHCenter)
            num_label.setStyleSheet(
                f"font-family: {FONT_FAMILY}; font-size: {FONT_SIZE_NORMAL}px; color: {TEXT_PRIMARY_COLOR};"
            )
            v.addWidget(label, alignment=Qt.AlignHCenter)
            v.addWidget(num_label)
            hand_layout.addWidget(wrapper)

        hand_layout.addSpacing(32)

        tsumo_wrapper = QWidget()
        tsumo_wrapper.setStyleSheet("border: none; background-color: transparent;")
        v = QVBoxLayout(tsumo_wrapper)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(4)

        tsumo_label = QLabel()
        tsumo_label.setPixmap(unknown_img)
        tsumo_label.setStyleSheet("border: none; background-color: transparent;")
        tsumo_num = QLabel("")
        tsumo_num.setAlignment(Qt.AlignHCenter)
        tsumo_num.setStyleSheet(
            f"font-family: {FONT_FAMILY}; font-size: {FONT_SIZE_NORMAL}px; color: {TEXT_PRIMARY_COLOR};"
        )
        v.addWidget(tsumo_label, alignment=Qt.AlignHCenter)
        v.addWidget(tsumo_num)
        hand_layout.addWidget(tsumo_wrapper)

        for _ in range(13):
            wrapper = QWidget()
            wrapper.setStyleSheet("border: none; background-color: transparent;")
            v = QVBoxLayout(wrapper)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(4)

            spacer = QLabel()
            spacer.setFixedSize(TILE_WIDTH // 2, TILE_HEIGHT // 2)
            spacer.setStyleSheet("border: none; background-color: transparent;")

            v.addWidget(spacer, alignment=Qt.AlignHCenter)
            wait_layout.addWidget(wrapper)

        self.update_status("未解析")

    def show_tiles(self, hand_tiles, tsumo_tile, wait_tiles=None, candidates=None, current_shanten=None):
        """解析結果に基づき牌画像をウィジェットへ配置する"""
        # ============================================================
        # --- 表示更新 ---
        hand_layout = self.hand_box.layout()
        while hand_layout.count():
            item = hand_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        wait_layout = self.wait_box.layout()
        while wait_layout.count():
            item = wait_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        all_tiles = hand_tiles + [tsumo_tile]

        # --- 候補マップ構築 + 最大最小スコア判定 ---
        cand_map = {c["index"]: c for c in candidates} if candidates else {}
        max_score_indices = set()
        min_score_indices = set()
        if candidates:
            scores = [c["score"] for c in candidates]
            max_score = max(scores)
            min_score = min(scores)
            max_score_indices = {c["index"] for c in candidates if c["score"] == max_score}
            min_score_indices = {c["index"] for c in candidates if c["score"] == min_score}

        # --- 手牌＋ツモ牌の表示 ---
        for i, tile in enumerate(all_tiles):
            wrapper = QWidget()
            wrapper.setStyleSheet("border: none; background-color: transparent;")
            v = QVBoxLayout(wrapper)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(4)

            label = QLabel()
            label.setPixmap(self.tile_to_pixmap(tile))
            label.setStyleSheet("border: none; background-color: transparent;")

            num_label = QLabel("")
            num_label.setAlignment(Qt.AlignHCenter)

            rank_text = ""
            color = TEXT_PRIMARY_COLOR
            weight = ""
            if i in max_score_indices:
                rank_text = "+"
                before = cand_map[i].get("shanten_before", current_shanten)
                after = cand_map[i].get("shanten_after", current_shanten)
                color = WARNING_COLOR if before > after else TEXT_PRIMARY_COLOR
                weight = "font-weight: bold;"
            elif i in min_score_indices:
                rank_text = "-"
                color = TEXT_PRIMARY_COLOR
                weight = "font-weight: bold;"

            num_label.setText(rank_text)
            num_label.setStyleSheet(
                f"font-family: {FONT_FAMILY}; font-size: {FONT_SIZE_NORMAL}px; color: {color}; {weight}"
            )

            v.addWidget(label, alignment=Qt.AlignHCenter)
            v.addWidget(num_label)
            hand_layout.addWidget(wrapper)

            if i == len(hand_tiles) - 1:
                hand_layout.addSpacing(32)  # ツモとの間隔

        # --- 待ち牌の表示 ---
        if wait_tiles:
            unique_wait = list(dict.fromkeys(wait_tiles))
            for tile in unique_wait:
                wrapper = QWidget()
                wrapper.setStyleSheet("border: none; background-color: transparent;")
                v = QVBoxLayout(wrapper)
                v.setContentsMargins(0, 0, 0, 0)
                v.setSpacing(4)

                label = QLabel()
                label.setPixmap(self.tile_to_pixmap(tile, (TILE_WIDTH // 2, TILE_HEIGHT // 2)))
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(TILE_WIDTH // 2, TILE_HEIGHT // 2)
                label.setStyleSheet("border: none; background-color: transparent;")
                v.addWidget(label, alignment=Qt.AlignHCenter)
                wait_layout.addWidget(wrapper)
            remaining = 13 - len(unique_wait)
        else:
            remaining = 13

        for _ in range(max(remaining, 0)):
            wrapper = QWidget()
            wrapper.setStyleSheet("border: none; background-color: transparent;")
            v = QVBoxLayout(wrapper)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(4)

            label = QLabel("")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(TILE_WIDTH // 2, TILE_HEIGHT // 2)
            label.setStyleSheet("border: none; background-color: transparent;")
            v.addWidget(label, alignment=Qt.AlignHCenter)
            wait_layout.addWidget(wrapper)

    def tile_to_pixmap(self, tile_name, size=(TILE_WIDTH, TILE_HEIGHT)):
        """牌名や画像から角丸付き ``QPixmap`` を生成する"""
        if isinstance(tile_name, Image.Image):
            pixmap = QPixmap.fromImage(ImageQt(tile_name.convert("RGBA")))
        else:
            if tile_name in ("", "?", None):
                tile_path = self.get_unknown_tile_path()
            else:
                tile_path = os.path.join(TEMPLATE_DIRS[self.game_code], tile_name + ".png")
                if not os.path.exists(tile_path):
                    tile_path = self.get_unknown_tile_path()

            pixmap = QPixmap(tile_path)

        if pixmap.width() != size[0] or pixmap.height() != size[1]:
            pixmap = pixmap.scaled(size[0], size[1], Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        rounded = QPixmap(size[0], size[1])
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        path = QPainterPath()
        scale_ratio = size[0] / TILE_WIDTH
        radius = TILE_RADIUS * scale_ratio
        path.addRoundedRect(0, 0, size[0], size[1], radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rounded
