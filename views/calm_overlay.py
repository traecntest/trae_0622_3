from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
from config import CALM_COUNTDOWN_SECONDS


class CalmOverlay(QWidget):
    calm_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.countdown = CALM_COUNTDOWN_SECONDS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_tick)
        self._setup_ui()
        self.hide()

    def _setup_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("calmBg")
        self.bg_frame.setStyleSheet("""
            #calmBg {
                background-color: rgba(20, 50, 80, 235);
                border-radius: 20px;
            }
        """)

        bg_layout = QVBoxLayout(self.bg_frame)
        bg_layout.setContentsMargins(60, 50, 60, 50)
        bg_layout.setSpacing(20)

        title_label = QLabel("深呼吸，冷静一下")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            color: white;
            font-size: 36px;
            font-weight: bold;
        """)
        bg_layout.addWidget(title_label)

        self.countdown_label = QLabel(str(self.countdown))
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("""
            color: #4ade80;
            font-size: 72px;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 30);
            border-radius: 60px;
            min-width: 120px;
            min-height: 120px;
            padding: 20px;
        """)

        count_layout = QHBoxLayout()
        count_layout.addStretch()
        count_layout.addWidget(self.countdown_label)
        count_layout.addStretch()
        bg_layout.addLayout(count_layout)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("""
            color: #e0e0e0;
            font-size: 16px;
            line-height: 1.8;
        """)
        bg_layout.addWidget(self.message_label)

        instruction_label = QLabel("请利用这段时间仔细思考，不要被催促冲昏头脑")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("""
            color: #a0aec0;
            font-size: 13px;
        """)
        bg_layout.addWidget(instruction_label)

        self.skip_button = QPushButton("我已冷静，继续")
        self.skip_button.setObjectName("calmSkipButton")
        self.skip_button.setEnabled(False)
        self.skip_button.setFixedHeight(50)
        self.skip_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.skip_button.clicked.connect(self._on_skip)
        self.skip_button.setStyleSheet("""
            QPushButton#calmSkipButton {
                background-color: #4ade80;
                color: #0f172a;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 30px;
            }
            QPushButton#calmSkipButton:hover {
                background-color: #22c55e;
            }
            QPushButton#calmSkipButton:disabled {
                background-color: #475569;
                color: #94a3b8;
            }
        """)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.skip_button)
        btn_layout.addStretch()
        bg_layout.addLayout(btn_layout)

        main_layout.addWidget(self.bg_frame)

    def show_calm(self, message: str = ""):
        self.countdown = CALM_COUNTDOWN_SECONDS
        self.countdown_label.setText(str(self.countdown))
        self.message_label.setText(message)
        self.skip_button.setEnabled(False)
        self.skip_button.setText(f"等待 {self.countdown} 秒...")

        parent = self.parent()
        if parent:
            self.setGeometry(parent.rect())

        self.show()
        self._animate_in()
        self.timer.start(1000)

    def _animate_in(self):
        self.bg_frame.setWindowOpacity(0.0)
        anim = QPropertyAnimation(self.bg_frame, b"windowOpacity", self)
        anim.setDuration(300)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

    def _on_tick(self):
        self.countdown -= 1
        self.countdown_label.setText(str(self.countdown))

        if self.countdown <= 3:
            self.skip_button.setEnabled(True)
            self.skip_button.setText("我已冷静，继续")
        else:
            self.skip_button.setText(f"等待 {self.countdown} 秒...")

        if self.countdown <= 0:
            self.timer.stop()
            self._finish_calm()

    def _on_skip(self):
        if self.countdown <= 3:
            self.timer.stop()
            self._finish_calm()

    def _finish_calm(self):
        self.hide()
        self.calm_finished.emit()

    def closeEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
        super().closeEvent(event)
