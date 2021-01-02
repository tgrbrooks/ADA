from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QSizePolicy,
    QGraphicsDropShadowEffect, QHBoxLayout)

from ada.components.button import DeleteButton
import ada.configuration as config


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

class DelLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(DelLabel, self).__init__(*args, **kwargs)
        self.button = DeleteButton()
        self.text = QLabel(text)
        self.file_name = ''
        self.text.setStyleSheet(config.label_style)
        self.text.setFixedHeight(25*config.hr)
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.text)
        self.setLayout(layout)

    def clear(self):
        self.text.clear()
        self.file_name = ''

    def setText(self, text):
        self.text.setText(text.split('/')[-1])
        self.file_name = text

