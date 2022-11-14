from PyQt5.QtWidgets import QGridLayout, QLabel

import styles as styles
from logger import logger
from components.window import Window


class ErrorWindow(Window):

    def __init__(self, error, parent=None):
        super(ErrorWindow, self).__init__('Error', 250, 100, QGridLayout, parent)
        logger.exception(error)
        self.message = str(error)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(styles.error_background)

        text = self.window.addWidget(QLabel(self.message), 0, 0)
        text.setStyleSheet(styles.error_font)
        text.setWordWrap(True)

def error_wrapper(func):
    def inner(self):
        try:
            func(self)
        except Exception as e:
            self.error = ErrorWindow(e, self)
            self.error.show()
    return inner
