from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout,
                             QGraphicsDropShadowEffect, QHBoxLayout)

from ada.components.button import DeleteButton
from ada.configuration import config
import ada.styles as styles


class Label(QWidget):
    def __init__(self, text, shadow=False, style=None, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.text = QLabel(text)
        self.text.setStyleSheet(styles.label_style)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)
        if shadow:
            shadow = QGraphicsDropShadowEffect(
                blurRadius=3*config['width_ratio'], xOffset=1*config['width_ratio'], yOffset=1*config['height_ratio'])
            self.setGraphicsEffect(shadow)
        if style:
            self.text.setStyleSheet(style)

    def setText(self, text):
        self.text.setText(text)


class TopLabel(Label):
    def __init__(self, text, *args, **kwargs):
        super(TopLabel, self).__init__(text, shadow=True, *args, **kwargs)
        self.text.setStyleSheet(styles.top_label_style)


class LeftLabel(Label):
    def __init__(self, text, *args, **kwargs):
        super(LeftLabel, self).__init__(text, *args, **kwargs)
        self.text.setStyleSheet(styles.left_label_style)


class RoundLabel(Label):
    def __init__(self, text, *args, **kwargs):
        super(RoundLabel, self).__init__(text, shadow=True, *args, **kwargs)
        self.text.setStyleSheet(styles.round_label_style)


class DelLabel(QWidget):
    def __init__(self, text, clicked=None, *args, **kwargs):
        super(DelLabel, self).__init__(*args, **kwargs)
        self.button = DeleteButton()
        self.text = QLabel(text)
        self.file_name = ''
        self.text.setStyleSheet(styles.label_style)
        self.text.setFixedHeight(25*config['height_ratio'])
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.text)
        self.setLayout(layout)
        if clicked is not None:
            self.button.clicked.connect(clicked)

    def clear(self):
        self.text.clear()
        self.file_name = ''

    def setText(self, text):
        self.text.setText(text.split('/')[-1])
        self.file_name = text
