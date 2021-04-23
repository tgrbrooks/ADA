from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QSizePolicy,
                             QGraphicsDropShadowEffect, QHBoxLayout)

from components.button import DeleteButton
import configuration as config
import styles as styles


class Label(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(styles.label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)


class TopLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(TopLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(styles.top_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=3*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)
        self.setLayout(layout)


class LeftLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(LeftLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(styles.left_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        self.setLayout(layout)


class RoundLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(RoundLabel, self).__init__(*args, **kwargs)
        text = QLabel(text)
        text.setStyleSheet(styles.round_label_style)
        layout = QVBoxLayout()
        layout.addWidget(text)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=3*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)
        self.setLayout(layout)


class DelLabel(QWidget):
    def __init__(self, text, bold=False, *args, **kwargs):
        super(DelLabel, self).__init__(*args, **kwargs)
        self.button = DeleteButton()
        self.text = QLabel(text)
        self.file_name = ''
        self.text.setStyleSheet(styles.label_style)
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
