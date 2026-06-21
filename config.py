import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DB_PATH = os.path.join(BASE_DIR, "yindun.db")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

RISK_LEVELS = {
    "safe": {"min": 0, "max": 20, "label": "安全", "color": "#22c55e"},
    "caution": {"min": 21, "max": 50, "label": "注意", "color": "#eab308"},
    "warning": {"min": 51, "max": 80, "label": "警告", "color": "#f97316"},
    "danger": {"min": 81, "max": 100, "label": "危险", "color": "#ef4444"},
}

CALM_COUNTDOWN_SECONDS = 10

ELDERLY_MODE = {
    "font_size_base": 16,
    "button_min_height": 50,
    "high_contrast": False,
}

os.makedirs(SCRIPTS_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
