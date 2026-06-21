from PyQt6.QtCore import QObject, pyqtSignal


class ElderlyModeManager(QObject):
    mode_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._is_elderly_mode = False

    def is_elderly_mode(self):
        return self._is_elderly_mode

    def set_elderly_mode(self, enabled: bool):
        if self._is_elderly_mode != enabled:
            self._is_elderly_mode = enabled
            self.mode_changed.emit(enabled)

    def toggle(self):
        self.set_elderly_mode(not self._is_elderly_mode)
        return self._is_elderly_mode

    def get_font_scale(self):
        return 1.3 if self._is_elderly_mode else 1.0
