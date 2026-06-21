from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette


class ChatBubble(QFrame):
    def __init__(self, text, is_sender=False, speaker="", is_risk_tip=False, parent=None):
        super().__init__(parent)
        self.is_sender = is_sender
        self.is_risk_tip = is_risk_tip
        self.speaker = speaker
        self.text = text

        self.setObjectName("chatBubble")
        self._setup_ui()
        self._apply_style()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        if self.speaker and not self.is_risk_tip:
            speaker_label = QLabel(self.speaker)
            speaker_label.setObjectName("speakerLabel")
            speaker_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
            if self.is_sender:
                speaker_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(speaker_label)

        bubble_layout = QHBoxLayout()
        bubble_layout.setContentsMargins(0, 0, 0, 0)

        if self.is_sender:
            bubble_layout.addStretch()

        content_widget = QWidget()
        content_widget.setObjectName("bubbleContent")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(14, 10, 14, 10)
        content_layout.setSpacing(0)

        text_label = QLabel(self.text)
        text_label.setWordWrap(True)
        text_label.setObjectName("bubbleText")
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        content_layout.addWidget(text_label)

        content_widget.setMaximumWidth(480)
        bubble_layout.addWidget(content_widget)

        if not self.is_sender:
            bubble_layout.addStretch()

        layout.addLayout(bubble_layout)

    def _apply_style(self):
        if self.is_risk_tip:
            self.setStyleSheet("""
                #bubbleContent {
                    background-color: #fef3c7;
                    border: 2px solid #f59e0b;
                    border-radius: 10px;
                }
                #bubbleText {
                    color: #92400e;
                    font-size: 13px;
                    font-weight: 500;
                }
                QFrame#chatBubble {
                    background: transparent;
                }
            """)
        elif self.is_sender:
            self.setStyleSheet("""
                #bubbleContent {
                    background-color: #3498db;
                    border-radius: 10px;
                }
                #bubbleText {
                    color: white;
                    font-size: 14px;
                }
                QFrame#chatBubble {
                    background: transparent;
                }
            """)
        else:
            self.setStyleSheet("""
                #bubbleContent {
                    background-color: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 10px;
                }
                #bubbleText {
                    color: #333333;
                    font-size: 14px;
                }
                QFrame#chatBubble {
                    background: transparent;
                }
            """)

    def animate_appear(self):
        self.setWindowOpacity(0.0)
        animation = QPropertyAnimation(self, b"windowOpacity", self)
        animation.setDuration(300)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InCubic)
        animation.start()


class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bubbles = []
        self._setup_ui()

    def _setup_ui(self):
        from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(16, 16, 16, 16)
        self.chat_layout.setSpacing(12)
        self.chat_layout.addStretch()

        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area)

    def add_message(self, text, is_sender=False, speaker="", is_risk_tip=False):
        bubble = ChatBubble(text, is_sender, speaker, is_risk_tip)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self.bubbles.append(bubble)
        self._scroll_to_bottom()
        return bubble

    def _scroll_to_bottom(self):
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(50, self._do_scroll)

    def _do_scroll(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear(self):
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.bubbles.clear()
