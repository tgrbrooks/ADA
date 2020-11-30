from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QSizePolicy,
    QGraphicsDropShadowEffect)

import algaeplot.configuration as config


class Label(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)

class TopLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(TopLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.top_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=1, yOffset=1)
        self.setGraphicsEffect(shadow)
        self.setLayout(layout)

class LeftLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(LeftLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.left_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)

class RoundLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(RoundLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(config.round_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)
