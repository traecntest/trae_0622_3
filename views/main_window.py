from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QStackedWidget, QFrame, QButtonGroup,
                             QMessageBox, QFileDialog, QLineEdit, QSpinBox, QDialog,
                             QDialogButtonBox, QScrollArea)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QIcon

from views.style_sheet import get_style_sheet
from views.chat_widget import ChatWidget
from views.risk_display import RiskDisplayWidget
from views.calm_overlay import CalmOverlay
from views.script_selector import ScriptSelectorWidget
from views.result_page import ResultPageWidget

from controllers import MainController, ExerciseController
from engines import ScriptEngine
from risk_assessment import RiskAssessor
from utils import PDFGenerator, ElderlyModeManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_controller = MainController()
        self.exercise_controller = None
        self.pdf_generator = PDFGenerator()
        self.elderly_manager = ElderlyModeManager()
        self.current_script_id = ""

        self.setWindowTitle("银盾反诈彩排室")
        self.setMinimumSize(QSize(960, 680))
        self.resize(QSize(1080, 720))

        self._setup_ui()
        self._load_scripts()
        self._apply_style()

        self.elderly_manager.mode_changed.connect(self._on_elderly_mode_changed)
        self._init_default_user()
        self._update_user_display()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebarWidget")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        app_title = QLabel("银盾反诈")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_title.setStyleSheet("font-size: 22px; font-weight: bold; color: white; padding: 25px 0 8px 0;")
        sidebar_layout.addWidget(app_title)

        app_subtitle = QLabel("彩排室")
        app_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_subtitle.setStyleSheet("font-size: 14px; color: #94a3b8; padding-bottom: 15px;")
        sidebar_layout.addWidget(app_subtitle)

        user_frame = QFrame()
        user_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,0.08);
                border-radius: 8px;
                margin: 0 12px 12px 12px;
            }
        """)
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(10, 10, 10, 10)
        user_layout.setSpacing(4)

        self.user_name_label = QLabel("当前用户")
        self.user_name_label.setStyleSheet("color: white; font-size: 13px; font-weight: bold;")
        user_layout.addWidget(self.user_name_label)

        self.user_info_label = QLabel("未登录")
        self.user_info_label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        user_layout.addWidget(self.user_info_label)

        user_btn_layout = QHBoxLayout()
        user_btn_layout.setSpacing(6)

        self.switch_user_btn = QPushButton("切换用户")
        self.switch_user_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.switch_user_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(52,152,219,0.3);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(52,152,219,0.5);
            }
        """)
        self.switch_user_btn.clicked.connect(self._show_user_manager)
        user_btn_layout.addWidget(self.switch_user_btn)

        self.add_user_btn = QPushButton("+新用户")
        self.add_user_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_user_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(34,197,94,0.3);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(34,197,94,0.5);
            }
        """)
        self.add_user_btn.clicked.connect(self._show_create_user_dialog)
        user_btn_layout.addWidget(self.add_user_btn)

        user_layout.addLayout(user_btn_layout)
        sidebar_layout.addWidget(user_frame)

        self.nav_buttons = []
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        nav_items = [
            ("首页", "home"),
            ("演练记录", "records"),
            ("设置", "settings"),
        ]

        for i, (text, page_name) in enumerate(nav_items):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, p=page_name: self._navigate_to(p))
            self.button_group.addButton(btn, i)
            self.nav_buttons.append((btn, page_name))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        self.elderly_btn = QPushButton("老人模式")
        self.elderly_btn.setCheckable(True)
        self.elderly_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.elderly_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
        """)
        self.elderly_btn.clicked.connect(self._toggle_elderly_mode)
        sidebar_layout.addWidget(self.elderly_btn)

        main_layout.addWidget(sidebar)

        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)

        self._create_home_page()
        self._create_exercise_page()
        self._create_records_page()
        self._create_settings_page()
        self._create_result_page()

        self.calm_overlay = CalmOverlay(self)

        self._navigate_to("home")
        if self.nav_buttons:
            self.nav_buttons[0][0].setChecked(True)

    def _create_home_page(self):
        self.home_page = QWidget()
        layout = QVBoxLayout(self.home_page)
        layout.setContentsMargins(0, 0, 0, 0)

        self.script_selector = ScriptSelectorWidget()
        self.script_selector.script_selected.connect(self._on_script_selected)
        layout.addWidget(self.script_selector)

        self.content_stack.addWidget(self.home_page)

    def _create_exercise_page(self):
        self.exercise_page = QWidget()
        layout = QHBoxLayout(self.exercise_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setObjectName("exerciseHeader")
        header.setStyleSheet("""
            QFrame#exerciseHeader {
                background-color: white;
                border-bottom: 1px solid #e5e7eb;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 12, 16, 12)

        self.back_btn = QPushButton("← 返回")
        self.back_btn.setObjectName("secondaryButton")
        self.back_btn.setFixedHeight(36)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self._back_to_home)
        header_layout.addWidget(self.back_btn)

        self.exercise_title = QLabel("反诈演练")
        self.exercise_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(self.exercise_title)
        header_layout.addStretch()

        chat_layout.addWidget(header)

        self.chat_widget = ChatWidget()
        chat_layout.addWidget(self.chat_widget, 1)

        self.options_container = QFrame()
        self.options_container.setObjectName("optionsPanel")
        self.options_container.setStyleSheet("""
            QFrame#optionsPanel {
                background-color: white;
                border-top: 1px solid #e5e7eb;
            }
        """)
        self.options_layout = QVBoxLayout(self.options_container)
        self.options_layout.setContentsMargins(16, 12, 16, 16)
        self.options_layout.setSpacing(8)

        self.option_buttons = []
        chat_layout.addWidget(self.options_container)

        layout.addWidget(chat_container, 1)

        side_panel = QFrame()
        side_panel.setObjectName("sidePanel")
        side_panel.setFixedWidth(260)
        side_panel.setStyleSheet("""
            QFrame#sidePanel {
                background-color: #f8fafc;
                border-left: 1px solid #e5e7eb;
            }
        """)
        side_layout = QVBoxLayout(side_panel)
        side_layout.setContentsMargins(16, 16, 16, 16)
        side_layout.setSpacing(12)

        self.risk_display = RiskDisplayWidget()
        side_layout.addWidget(self.risk_display)

        self.tip_panel = QFrame()
        self.tip_panel.setObjectName("tipPanel")
        self.tip_panel.setStyleSheet("""
            QFrame#tipPanel {
                background-color: white;
                border-radius: 10px;
            }
        """)
        tip_layout = QVBoxLayout(self.tip_panel)
        tip_layout.setContentsMargins(14, 12, 14, 12)

        tip_title = QLabel("防骗贴士")
        tip_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #f59e0b;")
        tip_layout.addWidget(tip_title)

        self.tip_content = QLabel("")
        self.tip_content.setWordWrap(True)
        self.tip_content.setStyleSheet("font-size: 13px; color: #666; line-height: 1.6;")
        tip_layout.addWidget(self.tip_content)

        side_layout.addWidget(self.tip_panel)
        side_layout.addStretch()

        layout.addWidget(side_panel)

        self.content_stack.addWidget(self.exercise_page)

    def _create_records_page(self):
        from PyQt6.QtWidgets import QScrollArea, QFrame

        self.records_page = QWidget()
        layout = QVBoxLayout(self.records_page)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("演练记录")
        title_label.setObjectName("titleLabel")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title_label)

        self.records_scroll = QScrollArea()
        self.records_scroll.setWidgetResizable(True)
        self.records_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.records_content = QWidget()
        self.records_layout = QVBoxLayout(self.records_content)
        self.records_layout.setContentsMargins(0, 0, 0, 0)
        self.records_layout.setSpacing(10)

        self.records_scroll.setWidget(self.records_content)
        layout.addWidget(self.records_scroll, 1)

        self.content_stack.addWidget(self.records_page)

    def _create_settings_page(self):
        self.settings_page = QWidget()
        layout = QVBoxLayout(self.settings_page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title_label = QLabel("设置")
        title_label.setObjectName("titleLabel")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title_label)

        user_card = QFrame()
        user_card.setStyleSheet("background-color: white; border-radius: 10px;")
        user_card_layout = QVBoxLayout(user_card)
        user_card_layout.setContentsMargins(20, 18, 20, 18)
        user_card_layout.setSpacing(14)

        user_title = QHBoxLayout()
        user_title_label = QLabel("用户管理")
        user_title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        user_title.addWidget(user_title_label)
        user_title.addStretch()
        create_user_btn = QPushButton("+ 创建新用户")
        create_user_btn.setObjectName("primaryButton")
        create_user_btn.setFixedHeight(36)
        create_user_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_user_btn.clicked.connect(self._show_create_user_dialog)
        user_title.addWidget(create_user_btn)
        user_card_layout.addLayout(user_title)

        self.users_scroll = QScrollArea()
        self.users_scroll.setWidgetResizable(True)
        self.users_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.users_scroll.setMaximumHeight(300)

        self.users_container = QWidget()
        self.users_list_layout = QVBoxLayout(self.users_container)
        self.users_list_layout.setContentsMargins(0, 0, 0, 0)
        self.users_list_layout.setSpacing(8)

        self.users_scroll.setWidget(self.users_container)
        user_card_layout.addWidget(self.users_scroll)

        layout.addWidget(user_card)

        settings_card = QFrame()
        settings_card.setStyleSheet("background-color: white; border-radius: 10px;")
        card_layout = QVBoxLayout(settings_card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(16)

        elderly_row = QHBoxLayout()
        elderly_label = QLabel("老人模式")
        elderly_label.setStyleSheet("font-size: 15px; color: #333;")
        elderly_row.addWidget(elderly_label)
        elderly_row.addStretch()

        self.elderly_toggle = QPushButton("开启")
        self.elderly_toggle.setCheckable(True)
        self.elderly_toggle.setFixedSize(80, 36)
        self.elderly_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.elderly_toggle.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                border: none;
                border-radius: 18px;
                color: #666;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #22c55e;
                color: white;
            }
        """)
        self.elderly_toggle.clicked.connect(self._toggle_elderly_mode)
        elderly_row.addWidget(self.elderly_toggle)
        card_layout.addLayout(elderly_row)

        desc = QLabel("老人模式：使用大字体、高对比度配色、大按钮设计，方便老年人操作。")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #7f8c8d;")
        card_layout.addWidget(desc)

        layout.addWidget(settings_card)
        layout.addStretch()

        self.content_stack.addWidget(self.settings_page)

    def _create_result_page(self):
        self.result_page = ResultPageWidget()
        self.result_page.back_to_home.connect(self._back_to_home)
        self.result_page.retry_exercise.connect(self._retry_exercise)
        self.result_page.export_pdf.connect(self._export_result_pdf)
        self.content_stack.addWidget(self.result_page)

    def _load_scripts(self):
        scripts = self.main_controller.get_all_scripts()
        self.script_selector.load_scripts(scripts)

    def _apply_style(self):
        style = get_style_sheet(self.elderly_manager.is_elderly_mode())
        self.setStyleSheet(style)

    def _navigate_to(self, page_name):
        page_map = {
            "home": self.home_page,
            "exercise": self.exercise_page,
            "records": self.records_page,
            "settings": self.settings_page,
            "result": self.result_page,
        }
        page = page_map.get(page_name)
        if page:
            self.content_stack.setCurrentWidget(page)
            if page_name == "records":
                self._refresh_records()
            elif page_name == "settings":
                self._refresh_users_list()

    def _on_script_selected(self, script_id):
        self.current_script_id = script_id
        self._start_exercise(script_id)

    def _start_exercise(self, script_id):
        if not self.main_controller.get_current_user():
            user = self.main_controller.create_user("default_user", "演练用户")
            self.main_controller.set_current_user(user)

        result = self.main_controller.start_exercise(script_id)
        record = result["record"]
        start_node = result["start_node"]
        metadata = result["script_metadata"]

        self.exercise_controller = ExerciseController(
            script_engine=self.main_controller.script_engine,
            record=record
        )
        self.exercise_controller.start()

        self.exercise_title.setText(metadata.get("name", "反诈演练"))
        self.chat_widget.clear()
        self.risk_display.reset()
        self.tip_content.setText("")

        self._display_node(start_node)

        self._navigate_to("exercise")

    def _display_node(self, node):
        self.chat_widget.add_message(
            text=node.text,
            is_sender=False,
            speaker=node.speaker
        )

        if node.risk_tip:
            self.tip_content.setText(node.risk_tip)
            self.chat_widget.add_message(
                text="💡 " + node.risk_tip,
                is_sender=False,
                is_risk_tip=True
            )

        self._render_options(node.options)

        if node.is_end:
            QTimer.singleShot(500, self._show_result)

    def _render_options(self, options):
        for btn in self.option_buttons:
            btn.deleteLater()
        self.option_buttons.clear()

        for option in options:
            btn = QPushButton(option.text)
            btn.setObjectName("optionButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(44)
            btn.clicked.connect(lambda checked, opt=option: self._on_option_clicked(opt))
            self.options_layout.addWidget(btn)
            self.option_buttons.append(btn)

    def _on_option_clicked(self, option):
        current_node = self.exercise_controller.current_node
        if current_node:
            self.chat_widget.add_message(
                text=option.text,
                is_sender=True
            )

        for btn in self.option_buttons:
            btn.setEnabled(False)

        result = self.exercise_controller.choose_option(option.id)

        if result:
            self.risk_display.update_risk(result["current_score"])

            if result["trigger_calm"] and result["calm_message"]:
                self.calm_overlay.calm_finished.connect(
                    lambda: self._after_calm(result)
                )
                self.calm_overlay.show_calm(result["calm_message"])
                return

            next_node = result["next_node"]
            if next_node:
                QTimer.singleShot(300, lambda: self._display_node(next_node))

    def _after_calm(self, result):
        self.calm_overlay.calm_finished.disconnect()
        next_node = result["next_node"]
        if next_node:
            self._display_node(next_node)

    def _show_result(self):
        if not self.exercise_controller:
            return

        summary = self.exercise_controller.get_risk_summary()
        script_name = self.exercise_title.text()

        tips = self._generate_tips(summary)
        self.result_page.set_result(script_name, summary, tips)
        self._navigate_to("result")

    def _generate_tips(self, summary):
        level_key = summary.get("final_level", "safe")
        tips_map = {
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
                "您的防骗意识有待提高",
                "请牢记：三不一多原则",
                "未知链接不点击",
                "陌生来电不轻信",
                "个人信息不透露",
                "转账汇款多核实"
            ],
            "danger": [
                "您处于高风险状态！",
                "请立即学习防骗知识",
                "凡是要求转账的都是诈骗",
                "凡是要求提供密码的都是诈骗",
                "凡是自称公检法要求汇款的都是诈骗",
                "请牢记全国反诈热线：96110"
            ]
        }
        return tips_map.get(level_key, tips_map["safe"])

    def _back_to_home(self):
        self._navigate_to("home")
        if self.nav_buttons:
            self.nav_buttons[0][0].setChecked(True)

    def _retry_exercise(self):
        if self.current_script_id:
            self._start_exercise(self.current_script_id)

    def _refresh_records(self):
        for i in reversed(range(self.records_layout.count())):
            item = self.records_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        records = self.main_controller.get_exercise_records()
        if not records:
            empty_label = QLabel("暂无演练记录，去首页开始演练吧！")
            empty_label.setStyleSheet("color: #999; font-size: 14px; padding: 30px;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.records_layout.addWidget(empty_label)
            self.records_layout.addStretch()
            return

        for record in records:
            record_card = QFrame()
            record_card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
            card_layout = QHBoxLayout(record_card)
            card_layout.setContentsMargins(14, 12, 14, 12)

            info_layout = QVBoxLayout()
            name_label = QLabel(record.script_name)
            name_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #333;")
            info_layout.addWidget(name_label)

            user = self.main_controller.get_user(record.user_id)
            user_name = user.nickname if user and user.nickname else (user.username if user else "未知")
            date_label = QLabel(f"{user_name} · {record.created_at}")
            date_label.setStyleSheet("font-size: 12px; color: #999;")
            info_layout.addWidget(date_label)

            card_layout.addLayout(info_layout)
            card_layout.addStretch()

            level_color = self._get_risk_color(record.final_risk_score)
            score_label = QLabel(f"{record.final_risk_score}分")
            score_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {level_color};")
            card_layout.addWidget(score_label)

            self.records_layout.addWidget(record_card)

        self.records_layout.addStretch()

    def _get_risk_color(self, score):
        if score <= 20:
            return "#22c55e"
        elif score <= 50:
            return "#eab308"
        elif score <= 80:
            return "#f97316"
        else:
            return "#ef4444"

    def _toggle_elderly_mode(self):
        is_elderly = self.elderly_manager.toggle()
        self.elderly_btn.setChecked(is_elderly)
        self.elderly_toggle.setChecked(is_elderly)
        self.elderly_toggle.setText("关闭" if is_elderly else "开启")

    def _on_elderly_mode_changed(self, is_elderly):
        self._apply_style()

    def _export_result_pdf(self):
        if not self.exercise_controller:
            return

        summary = self.exercise_controller.get_risk_summary()
        script_name = self.exercise_title.text()
        tips = self._generate_tips(summary)

        try:
            filepath = self.pdf_generator.generate_action_card(
                script_name=script_name,
                risk_summary=summary,
                tips=tips
            )
            if filepath:
                img_path = self.pdf_generator.generate_summary_image(
                    script_name=script_name,
                    risk_summary=summary,
                    tips=tips
                )

                msg = f"家庭防骗行动卡已生成！\n\nPDF文件：{filepath}"
                if img_path:
                    msg += f"\n\n图片文件：{img_path}"

                QMessageBox.information(self, "生成成功", msg)
            else:
                QMessageBox.warning(self, "生成失败", "PDF生成失败，请检查系统字体配置。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成失败：{str(e)}")

    def _init_default_user(self):
        user = self.main_controller.get_or_create_default_user()
        if user.is_elderly_mode:
            self.elderly_manager.set_elderly_mode(True)
            self.elderly_btn.setChecked(True)
            self.elderly_toggle.setChecked(True)
            self.elderly_toggle.setText("关闭")

    def _update_user_display(self):
        user = self.main_controller.get_current_user()
        if user:
            display_name = user.nickname if user.nickname else user.username
            self.user_name_label.setText(display_name)
            if user.age:
                self.user_info_label.setText(f"{user.age}岁 · 账号：{user.username}")
            else:
                self.user_info_label.setText(f"账号：{user.username}")
        else:
            self.user_name_label.setText("当前用户")
            self.user_info_label.setText("未登录")

    def _refresh_users_list(self):
        for i in reversed(range(self.users_list_layout.count())):
            item = self.users_list_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        users = self.main_controller.list_users()
        current_user = self.main_controller.get_current_user()

        if not users:
            empty_label = QLabel("暂无用户，请创建新用户")
            empty_label.setStyleSheet("color: #999; font-size: 13px; padding: 20px;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.users_list_layout.addWidget(empty_label)
            self.users_list_layout.addStretch()
            return

        for user in users:
            user_row = QFrame()
            is_current = current_user and current_user.id == user.id
            border_color = "#3498db" if is_current else "#e5e7eb"
            bg_color = "#ebf5fb" if is_current else "white"
            user_row.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 8px;
                }}
            """)
            row_layout = QHBoxLayout(user_row)
            row_layout.setContentsMargins(14, 10, 14, 10)

            info_layout = QVBoxLayout()
            name = user.nickname if user.nickname else user.username
            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
            info_layout.addWidget(name_label)

            extras = []
            extras.append(user.username)
            if user.age:
                extras.append(f"{user.age}岁")
            if user.is_elderly_mode:
                extras.append("老人模式")
            extra_label = QLabel(" · ".join(extras))
            extra_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
            info_layout.addWidget(extra_label)

            row_layout.addLayout(info_layout)
            row_layout.addStretch()

            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(6)

            if is_current:
                current_tag = QLabel("✓ 当前使用")
                current_tag.setStyleSheet("color: #3498db; font-size: 12px; font-weight: bold; padding: 4px 10px; background-color: #d6eaf8; border-radius: 10px;")
                btn_layout.addWidget(current_tag)
            else:
                switch_btn = QPushButton("切换")
                switch_btn.setObjectName("secondaryButton")
                switch_btn.setFixedSize(60, 32)
                switch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                switch_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                switch_btn.clicked.connect(lambda checked, u=user: self._switch_user(u))
                btn_layout.addWidget(switch_btn)

            row_layout.addLayout(btn_layout)
            self.users_list_layout.addWidget(user_row)

        self.users_list_layout.addStretch()

    def _switch_user(self, user):
        self.main_controller.set_current_user(user)
        if user.is_elderly_mode != self.elderly_manager.is_elderly_mode():
            self.elderly_manager.set_elderly_mode(user.is_elderly_mode)
            self.elderly_btn.setChecked(user.is_elderly_mode)
            self.elderly_toggle.setChecked(user.is_elderly_mode)
            self.elderly_toggle.setText("关闭" if user.is_elderly_mode else "开启")
        self._update_user_display()
        self._refresh_users_list()
        QMessageBox.information(self, "切换成功", f"已切换到用户：{user.nickname if user.nickname else user.username}")

    def _show_user_manager(self):
        self._navigate_to("settings")
        self.nav_buttons[2][0].setChecked(True)

    def _show_create_user_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("创建新用户")
        dialog.setFixedWidth(380)

        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setContentsMargins(24, 20, 24, 20)
        dlg_layout.setSpacing(16)

        username_row = QVBoxLayout()
        username_label = QLabel("用户名（必填，唯一标识）")
        username_label.setStyleSheet("font-size: 13px; color: #333; font-weight: bold;")
        username_row.addWidget(username_label)
        username_input = QLineEdit()
        username_input.setPlaceholderText("例如：zhang_san")
        username_input.setFixedHeight(38)
        username_row.addWidget(username_input)
        dlg_layout.addLayout(username_row)

        nickname_row = QVBoxLayout()
        nickname_label = QLabel("昵称（显示用）")
        nickname_label.setStyleSheet("font-size: 13px; color: #333; font-weight: bold;")
        nickname_row.addWidget(nickname_label)
        nickname_input = QLineEdit()
        nickname_input.setPlaceholderText("例如：张三")
        nickname_input.setFixedHeight(38)
        nickname_row.addWidget(nickname_input)
        dlg_layout.addLayout(nickname_row)

        age_row = QVBoxLayout()
        age_label = QLabel("年龄")
        age_label.setStyleSheet("font-size: 13px; color: #333; font-weight: bold;")
        age_row.addWidget(age_label)
        age_input = QSpinBox()
        age_input.setRange(0, 120)
        age_input.setValue(30)
        age_input.setFixedHeight(38)
        age_row.addWidget(age_input)
        dlg_layout.addLayout(age_row)

        elderly_row = QHBoxLayout()
        elderly_label = QLabel("老人模式")
        elderly_label.setStyleSheet("font-size: 13px; color: #333; font-weight: bold;")
        elderly_row.addWidget(elderly_label)
        elderly_row.addStretch()
        elderly_check = QPushButton("关闭")
        elderly_check.setCheckable(True)
        elderly_check.setFixedSize(72, 32)
        elderly_check.setCursor(Qt.CursorShape.PointingHandCursor)
        elderly_check.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                border: none;
                border-radius: 16px;
                color: #666;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #22c55e;
                color: white;
            }
        """)
        elderly_check.clicked.connect(lambda: elderly_check.setText("开启" if not elderly_check.isChecked() else "关闭"))
        elderly_row.addWidget(elderly_check)
        dlg_layout.addLayout(elderly_row)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("创建")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("取消")
        buttons.button(QDialogButtonBox.StandardButton.Ok).setFixedHeight(40)
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setFixedHeight(40)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dlg_layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            username = username_input.text().strip()
            nickname = nickname_input.text().strip()
            age = age_input.value()
            is_elderly = elderly_check.isChecked()

            if not username:
                QMessageBox.warning(self, "创建失败", "用户名不能为空！")
                return

            existing = self.main_controller.create_user(username, nickname, age, is_elderly)
            self.main_controller.set_current_user(existing)
            self._update_user_display()
            self._refresh_users_list()

            if is_elderly != self.elderly_manager.is_elderly_mode():
                self.elderly_manager.set_elderly_mode(is_elderly)
                self.elderly_btn.setChecked(is_elderly)
                self.elderly_toggle.setChecked(is_elderly)
                self.elderly_toggle.setText("关闭" if is_elderly else "开启")

            QMessageBox.information(self, "创建成功", f"用户 '{username}' 创建成功，已自动切换到该用户。")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'calm_overlay'):
            self.calm_overlay.setGeometry(self.rect())
