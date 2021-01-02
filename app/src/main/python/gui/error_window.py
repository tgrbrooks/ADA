from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget

import configuration as config


class ErrorWindow(QMainWindow):

    def __init__(self, message, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.title = 'Error'
        self.width = 250*config.wr
        self.height = 100*config.hr
        self.message = message
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.setStyleSheet(config.error_background)

        layout = QGridLayout()
        layout.setContentsMargins(5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        layout.setSpacing(5*config.wr)

        text = QLabel(self.message)
        text.setStyleSheet(config.error_font)
        text.setWordWrap(True)

        layout.addWidget(text, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
