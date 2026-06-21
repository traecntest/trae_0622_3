from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from config import RISK_LEVELS


class ResultPageWidget(QWidget):
    back_to_home = pyqtSignal()
    export_pdf = pyqtSignal()
    retry_exercise = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        title_label = QLabel("演练结果")
        title_label.setObjectName("titleLabel")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        content_layout.addWidget(title_label)

        self.script_name_label = QLabel("")
        self.script_name_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        content_layout.addWidget(self.script_name_label)

        score_panel = QFrame()
        score_panel.setObjectName("scorePanel")
        score_panel.setStyleSheet("""
            QFrame#scorePanel {
                background-color: white;
                border-radius: 12px;
            }
        """)

        score_layout = QVBoxLayout(score_panel)
        score_layout.setContentsMargins(30, 25, 30, 25)
        score_layout.setSpacing(10)

        score_title = QLabel("最终风险得分")
        score_title.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        score_layout.addWidget(score_title)

        score_row = QHBoxLayout()
        self.score_label = QLabel("0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        score_row.addWidget(self.score_label)

        self.level_label = QLabel("安全")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        score_row.addWidget(self.level_label)
        score_row.addStretch()
        score_layout.addLayout(score_row)

        content_layout.addWidget(score_panel)

        stats_panel = QFrame()
        stats_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        stats_layout = QVBoxLayout(stats_panel)
        stats_layout.setContentsMargins(20, 18, 20, 18)
        stats_layout.setSpacing(12)

        stats_title = QLabel("统计数据")
        stats_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #2c3e50;")
        stats_layout.addWidget(stats_title)

        self.stats_content = QLabel("")
        self.stats_content.setWordWrap(True)
        self.stats_content.setStyleSheet("font-size: 14px; color: #333; line-height: 1.8;")
        stats_layout.addWidget(self.stats_content)

        content_layout.addWidget(stats_panel)

        summary_panel = QFrame()
        summary_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        summary_layout = QVBoxLayout(summary_panel)
        summary_layout.setContentsMargins(20, 18, 20, 18)
        summary_layout.setSpacing(12)

        summary_title = QLabel("防骗要点")
        summary_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #2c3e50;")
        summary_layout.addWidget(summary_title)

        self.summary_content = QLabel("")
        self.summary_content.setWordWrap(True)
        self.summary_content.setStyleSheet("font-size: 14px; color: #333; line-height: 2;")
        summary_layout.addWidget(self.summary_content)

        content_layout.addWidget(summary_panel)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.back_button = QPushButton("返回首页")
        self.back_button.setObjectName("secondaryButton")
        self.back_button.setFixedHeight(48)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(self.back_to_home.emit)
        btn_layout.addWidget(self.back_button)

        self.retry_button = QPushButton("再练一次")
        self.retry_button.setObjectName("secondaryButton")
        self.retry_button.setFixedHeight(48)
        self.retry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.retry_button.clicked.connect(self.retry_exercise.emit)
        btn_layout.addWidget(self.retry_button)

        self.export_button = QPushButton("生成家庭防骗卡")
        self.export_button.setObjectName("primaryButton")
        self.export_button.setFixedHeight(48)
        self.export_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_button.clicked.connect(self.export_pdf.emit)
        btn_layout.addWidget(self.export_button)

        content_layout.addLayout(btn_layout)
        content_layout.addStretch()

        self.scroll_area.setWidget(content)
        layout.addWidget(self.scroll_area)

    def set_result(self, script_name: str, summary: dict, tips: list = None):
        self.script_name_label.setText(f"场景：{script_name}")

        score = summary.get("final_score", 0)
        level_key = summary.get("final_level", "safe")
        level_label = summary.get("final_level_label", "安全")
        level_info = RISK_LEVELS.get(level_key, RISK_LEVELS["safe"])
        color = level_info["color"]

        self.score_label.setText(str(score))
        self.score_label.setStyleSheet(f"font-size: 48px; font-weight: bold; color: {color};")
        self.level_label.setText(level_label)
        self.level_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color}; padding-bottom: 8px;")

        total_choices = summary.get("total_choices", 0)
        safe_choices = summary.get("safe_choices", 0)
        safety_rate = int(summary.get("safety_rate", 0) * 100)

        stats_text = (
            f"• 总选择次数：{total_choices} 次<br>"
            f"• 安全选择：{safe_choices} 次<br>"
            f"• 安全选择率：{safety_rate}%<br>"
            f"• 风险趋势：{self._trend_text(summary.get('risk_trend', 'stable'))}"
        )
        self.stats_content.setText(stats_text)

        if tips:
            tip_html = "<br>".join([f"• {tip}" for tip in tips])
        else:
            tip_html = self._default_tips(level_key)
        self.summary_content.setText(tip_html)

    def _trend_text(self, trend):
        trends = {
            "rising": "上升趋势 ⚠️",
            "falling": "下降趋势 ✓",
            "stable": "平稳 →"
        }
        return trends.get(trend, "平稳 →")

    def _default_tips(self, level_key):
        tips = {
            "safe": [
                "不轻信陌生来电和短信",
                "不透露银行卡密码和验证码",
                "不向陌生人转账汇款",
                "遇到疑问先和家人商量",
                "可疑情况拨打110核实"
            ],
            "caution": [
                "提高警惕，不要有侥幸心理",
                "公检法机关不会电话办案",
                "刷单本身就是违法行为",
                "天上不会掉馅饼",
                "多和家人沟通交流"
            ],
            "warning": [
                "⚠️ 您的防骗意识有待提高",
                "请牢记：三不一多原则",
                "未知链接不点击",
                "陌生来电不轻信",
                "个人信息不透露",
                "转账汇款多核实"
            ],
            "danger": [
                "🚨 您处于高风险状态！",
                "请立即学习防骗知识",
                "凡是要求转账的都是诈骗",
                "凡是要求提供密码的都是诈骗",
                "凡是自称公检法要求汇款的都是诈骗",
                "请牢记全国反诈热线：96110"
            ]
        }
        tip_list = tips.get(level_key, tips["safe"])
        return "<br>".join([f"• {tip}" for tip in tip_list])
