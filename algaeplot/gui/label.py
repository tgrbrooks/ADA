from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

import algaeplot.configuration as config


class Label(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.small_font)
        if(bold):
            text.setStyleSheet(config.default_font_bold)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)
