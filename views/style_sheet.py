NORMAL_STYLE = """
QWidget {
    font-family: "Microsoft YaHei", "PingFang SC", "SimHei", sans-serif;
    font-size: 14px;
    color: #333333;
}

QMainWindow {
    background-color: #f5f7fa;
}

#sidebarWidget {
    background-color: #2c3e50;
    color: white;
}

#sidebarWidget QLabel {
    color: white;
}

#sidebarWidget QPushButton {
    background-color: transparent;
    color: white;
    border: none;
    padding: 12px 20px;
    text-align: left;
    font-size: 15px;
}

#sidebarWidget QPushButton:hover {
    background-color: #34495e;
}

#sidebarWidget QPushButton:checked {
    background-color: #3498db;
}

#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #2c3e50;
    padding: 10px 0;
}

#riskScoreLabel {
    font-size: 32px;
    font-weight: bold;
}

#riskLevelLabel {
    font-size: 16px;
    font-weight: bold;
}

QPushButton#primaryButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 15px;
    font-weight: bold;
}

QPushButton#primaryButton:hover {
    background-color: #2980b9;
}

QPushButton#primaryButton:pressed {
    background-color: #1a5276;
}

QPushButton#secondaryButton {
    background-color: #ecf0f1;
    color: #333333;
    border: 1px solid #bdc3c7;
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 15px;
}

QPushButton#secondaryButton:hover {
    background-color: #d5dbdb;
}

QPushButton#optionButton {
    background-color: white;
    border: 2px solid #3498db;
    border-radius: 8px;
    padding: 12px 20px;
    text-align: left;
    font-size: 14px;
}

QPushButton#optionButton:hover {
    background-color: #ebf5fb;
    border-color: #2980b9;
}

QPushButton#optionButton:disabled {
    background-color: #f5f5f5;
    border-color: #cccccc;
    color: #999999;
}

QFrame#riskPanel {
    background-color: white;
    border-radius: 10px;
}

QScrollArea {
    background-color: transparent;
    border: none;
}

QScrollBar:vertical {
    width: 8px;
    background: #f0f0f0;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #c0c0c0;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #a0a0a0;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QProgressBar {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    background-color: #f0f0f0;
    text-align: center;
    height: 20px;
}

QProgressBar::chunk {
    border-radius: 6px;
}

QFrame#scriptCard {
    background-color: white;
    border-radius: 10px;
    border: 2px solid #e8e8e8;
}

QFrame#scriptCard:hover {
    border-color: #3498db;
    background-color: #f8fafc;
}

QLabel#scriptTitle {
    font-size: 16px;
    font-weight: bold;
    color: #2c3e50;
}

QLabel#scriptDesc {
    font-size: 13px;
    color: #7f8c8d;
}

QLabel#difficultyTag {
    background-color: #e3f2fd;
    color: #1976d2;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}

QLabel#recordItem {
    background-color: white;
    padding: 10px;
    border-radius: 8px;
    border-bottom: 1px solid #eee;
}
"""

ELDERLY_STYLE = """
QWidget {
    font-family: "Microsoft YaHei", "PingFang SC", "SimHei", sans-serif;
    font-size: 18px;
    color: #000000;
}

QMainWindow {
    background-color: #ffffff;
}

#sidebarWidget {
    background-color: #1a252f;
    color: white;
}

#sidebarWidget QLabel {
    color: white;
    font-size: 20px;
}

#sidebarWidget QPushButton {
    background-color: transparent;
    color: white;
    border: none;
    padding: 18px 24px;
    text-align: left;
    font-size: 20px;
    font-weight: bold;
    min-height: 50px;
}

#sidebarWidget QPushButton:hover {
    background-color: #2c3e50;
}

#sidebarWidget QPushButton:checked {
    background-color: #e74c3c;
}

#titleLabel {
    font-size: 26px;
    font-weight: bold;
    color: #000000;
    padding: 15px 0;
}

#riskScoreLabel {
    font-size: 42px;
    font-weight: bold;
}

#riskLevelLabel {
    font-size: 22px;
    font-weight: bold;
}

QPushButton#primaryButton {
    background-color: #e74c3c;
    color: white;
    border: 3px solid #c0392b;
    border-radius: 10px;
    padding: 16px 32px;
    font-size: 20px;
    font-weight: bold;
    min-height: 56px;
}

QPushButton#primaryButton:hover {
    background-color: #c0392b;
}

QPushButton#secondaryButton {
    background-color: #ffffff;
    color: #000000;
    border: 3px solid #7f8c8d;
    border-radius: 10px;
    padding: 16px 32px;
    font-size: 20px;
    font-weight: bold;
    min-height: 56px;
}

QPushButton#secondaryButton:hover {
    background-color: #ecf0f1;
}

QPushButton#optionButton {
    background-color: #ffffff;
    border: 3px solid #e74c3c;
    border-radius: 10px;
    padding: 16px 24px;
    text-align: left;
    font-size: 18px;
    font-weight: bold;
    min-height: 60px;
}

QPushButton#optionButton:hover {
    background-color: #fdedec;
    border-color: #c0392b;
}

QFrame#riskPanel {
    background-color: #fff9e6;
    border: 3px solid #f39c12;
    border-radius: 12px;
}

QProgressBar {
    border: 3px solid #333333;
    border-radius: 10px;
    background-color: #f0f0f0;
    text-align: center;
    height: 28px;
    font-size: 16px;
    font-weight: bold;
}

QProgressBar::chunk {
    border-radius: 7px;
}

QFrame#scriptCard {
    background-color: #ffffff;
    border-radius: 12px;
    border: 3px solid #333333;
}

QLabel#scriptTitle {
    font-size: 22px;
    font-weight: bold;
    color: #000000;
}

QLabel#scriptDesc {
    font-size: 16px;
    color: #333333;
}

QLabel#difficultyTag {
    background-color: #e74c3c;
    color: white;
    padding: 6px 14px;
    border-radius: 15px;
    font-size: 16px;
    font-weight: bold;
}
"""


def get_style_sheet(is_elderly_mode=False):
    return ELDERLY_STYLE if is_elderly_mode else NORMAL_STYLE
