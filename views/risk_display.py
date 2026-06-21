from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPalette
from config import RISK_LEVELS


class RiskDisplayWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("riskPanel")
        self._setup_ui()
        self._current_score = 0

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        title_label = QLabel("风险评估")
        title_label.setObjectName("riskTitleLabel")
        title_label.setStyleSheet("font-size: 14px; color: #7f8c8d; font-weight: bold;")
        layout.addWidget(title_label)

        score_layout = QHBoxLayout()
        score_layout.setSpacing(8)

        self.score_label = QLabel("0")
        self.score_label.setObjectName("riskScoreLabel")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        score_layout.addWidget(self.score_label)

        self.level_label = QLabel("安全")
        self.level_label.setObjectName("riskLevelLabel")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        score_layout.addWidget(self.level_label)
        score_layout.addStretch()

        layout.addLayout(score_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        layout.addWidget(self.progress_bar)

        tip_label = QLabel("分数越高，受骗风险越大")
        tip_label.setStyleSheet("font-size: 11px; color: #95a5a6;")
        layout.addWidget(tip_label)

        self._update_appearance(0)

    def update_risk(self, score: int):
        old_score = self._current_score
        self._current_score = score

        self.score_label.setText(str(score))
        self.progress_bar.setValue(score)
        self._animate_score_change(old_score, score)
        self._update_appearance(score)

    def _animate_score_change(self, old_score: int, new_score: int):
        pass

    def _update_appearance(self, score: int):
        level_info = self._get_level_info(score)
        color = level_info["color"]
        label = level_info["label"]

        self.level_label.setText(label)
        self.score_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
        self.level_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color};")

        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 5px;
                background-color: #e8e8e8;
            }}
            QProgressBar::chunk {{
                border-radius: 5px;
                background-color: {color};
            }}
        """)

    def _get_level_info(self, score: int) -> dict:
        for key, level in RISK_LEVELS.items():
            if level["min"] <= score <= level["max"]:
                return level
        return RISK_LEVELS["danger"]

    def reset(self):
        self.update_risk(0)
