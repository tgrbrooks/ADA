from PyQt5.QtWidgets import QGridLayout, QLabel

import ada.styles as styles
from ada.logger import logger
from ada.components.window import Window


class ErrorWindow(Window):

    def __init__(self, error, parent=None):
        super(ErrorWindow, self).__init__('Error', 250, 100, QGridLayout, parent)
        logger.exception(error)
        self.message = str(error)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(styles.error_background)

        text = QLabel(self.message)
        text.setStyleSheet(styles.error_font)
        text.setWordWrap(True)

        self.window.addWidget(text, 0, 0)

def error_wrapper(func):
    def inner(self):
        try:
            func(self)
        except Exception as e:
            self.error = ErrorWindow(e, self)
            self.error.show()
    return inner