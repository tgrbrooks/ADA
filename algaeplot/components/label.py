from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy

import algaeplot.configuration as config


class Label(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.small_font)
        if(bold):
            text.setStyleSheet(config.default_font_bold)
        text.setStyleSheet(config.label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)

class TopLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(TopLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.small_font)
        if(bold):
            text.setStyleSheet(config.default_font_bold)
        text.setStyleSheet(config.top_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)

class LeftLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(LeftLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.small_font)
        if(bold):
            text.setStyleSheet(config.default_font_bold)
        text.setStyleSheet(config.left_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)
