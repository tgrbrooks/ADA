from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QGraphicsDropShadowEffect, QSizePolicy)

import ada.configuration as config
import ada.styles as styles


class Button(QPushButton):
    def __init__(self, text, parent=None, tooltip=None, *args, **kwargs):
        super(Button, self).__init__(text, parent, *args, **kwargs)
        self.setStyleSheet(styles.main_button_style)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=5*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)
        if tooltip is not None:
            self.setToolTip(tooltip)


class BigButton(QPushButton):
    def __init__(self, text, parent=None, tooltip=None, *args, **kwargs):
        super(BigButton, self).__init__(text, parent, *args, **kwargs)
        self.setStyleSheet(styles.big_button_style)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=5*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)
        self.setFixedHeight(60*config.hr)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        if tooltip is not None:
            self.setToolTip(tooltip)


class AddButton(QPushButton):
    def __init__(self, parent=None, *args, **kwargs):
        super(AddButton, self).__init__('+', parent, *args, **kwargs)
        self.setStyleSheet(styles.add_button_style)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=3*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)
        self.setFixedHeight(16*config.hr)
        self.setFixedWidth(16*config.wr)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


class DeleteButton(QPushButton):
    def __init__(self, parent=None, *args, **kwargs):
        super(DeleteButton, self).__init__('x', parent, *args, **kwargs)
        self.setStyleSheet(styles.delete_button_style)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=3*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)
        self.setFixedHeight(16*config.hr)
        self.setFixedWidth(16*config.wr)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
