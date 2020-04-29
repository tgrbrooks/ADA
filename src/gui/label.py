from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class Label(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet('font-size: 12pt; font-family: Courier;')
        if(bold):
            text.setStyleSheet(
                'font-size: 14pt; font-weight: bold; font-family: Courier;'
            )
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)
