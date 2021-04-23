from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget

import ada.configuration as config
import ada.styles as styles
from ada.logger import logger


class ErrorWindow(QMainWindow):

    def __init__(self, error, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.title = 'Error'
        self.width = 250*config.wr
        self.height = 100*config.hr
        logger.debug('Creating error window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        logger.exception(error)
        self.message = str(error)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.setStyleSheet(styles.error_background)

        layout = QGridLayout()
        layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        layout.setSpacing(5*config.wr)

        text = QLabel(self.message)
        text.setStyleSheet(styles.error_font)
        text.setWordWrap(True)

        layout.addWidget(text, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

def error_wrapper(func):
    def inner(self):
        try:
            func(self)
        except Exception as e:
            self.error = ErrorWindow(e, self)
            self.error.show()
    return inner