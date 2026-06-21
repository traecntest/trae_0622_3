from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ScriptCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, script_data, parent=None):
        super().__init__(parent)
        self.script_id = script_data.get("id", "")
        self.script_name = script_data.get("name", "")
        self.description = script_data.get("description", "")
        self.difficulty = script_data.get("difficulty", "medium")
        self.estimated_time = script_data.get("estimated_time", 0)
        self.scam_type = script_data.get("scam_type", "")

        self.setObjectName("scriptCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_ui()
        self._apply_style()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        header_layout = QHBoxLayout()

        title_label = QLabel(self.script_name)
        title_label.setObjectName("scriptTitle")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title_label)

        difficulty_label = QLabel(self._get_difficulty_label())
        difficulty_label.setObjectName("difficultyTag")
        difficulty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        difficulty_label.setFixedHeight(24)
        difficulty_label.setStyleSheet(self._get_difficulty_style())
        header_layout.addWidget(difficulty_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        type_label = QLabel(f"类型：{self.scam_type}")
        type_label.setStyleSheet("font-size: 12px; color: #3498db; font-weight: bold;")
        layout.addWidget(type_label)

        desc_label = QLabel(self.description)
        desc_label.setObjectName("scriptDesc")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 13px; color: #7f8c8d;")
        layout.addWidget(desc_label)

        if self.estimated_time > 0:
            time_label = QLabel(f"预计时长：{self.estimated_time}分钟")
            time_label.setStyleSheet("font-size: 12px; color: #95a5a6;")
            layout.addWidget(time_label)

    def _get_difficulty_label(self):
        labels = {"easy": "简单", "medium": "中等", "hard": "困难"}
        return labels.get(self.difficulty, "中等")

    def _get_difficulty_style(self):
        colors = {
            "easy": "background-color: #d1fae5; color: #065f46;",
            "medium": "background-color: #fef3c7; color: #92400e;",
            "hard": "background-color: #fee2e2; color: #991b1b;"
        }
        base = "padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold;"
        return base + colors.get(self.difficulty, colors["medium"])

    def _apply_style(self):
        self.setStyleSheet("""
            QFrame#scriptCard {
                background-color: white;
                border: 2px solid #e8e8e8;
                border-radius: 10px;
            }
            QFrame#scriptCard:hover {
                border-color: #3498db;
                background-color: #f8fafc;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.script_id)
        super().mousePressEvent(event)


class ScriptSelectorWidget(QWidget):
    script_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title_label = QLabel("选择演练场景")
        title_label.setObjectName("titleLabel")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title_label)

        subtitle = QLabel("点击下方卡片，开始反诈演练")
        subtitle.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        layout.addWidget(subtitle)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(12)

        self.scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.scroll_area, 1)

    def load_scripts(self, scripts_data):
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()
        self.cards.clear()

        for script_data in scripts_data:
            card = ScriptCard(script_data)
            card.clicked.connect(self._on_card_clicked)
            self.cards_layout.addWidget(card)
            self.cards.append(card)

        self.cards_layout.addStretch()

    def _on_card_clicked(self, script_id):
        self.script_selected.emit(script_id)
