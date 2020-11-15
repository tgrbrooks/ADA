from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget

import algaeplot.configuration as config


class ErrorWindow(QMainWindow):

    def __init__(self, message, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.title = 'Error'
        self.width = 150
        self.height = 100
        self.message = message
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QGridLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        text = QLabel(self.message)
        text.setStyleSheet(config.default_font_bold)

        layout.addWidget(text, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
