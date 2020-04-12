from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget

class ErrorWindow(QMainWindow):
    
    def __init__(self, message, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.title = 'Error'
        self.left = 50
        self.top = 50
        self.width = 150
        self.height = 100
        self.message = message
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(5)

        text = QLabel(self.message)
        text.setStyleSheet('font-size: 14pt; font-weight: bold; font-family: Courier;')

        layout.addWidget(text, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

