from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QSizePolicy

import ada.configuration as config
import ada.styles as styles


class Button(QPushButton):
    def __init__(self, text, parent=None, tooltip=None, clicked=None, shadow=True, *args, **kwargs):
        super(Button, self).__init__(text, parent, *args, **kwargs)
        self.setStyleSheet(styles.main_button_style)
        if shadow:
            button_shadow = QGraphicsDropShadowEffect(
                blurRadius=5*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
            self.setGraphicsEffect(button_shadow)
        if tooltip is not None:
            self.setToolTip(tooltip)
        if clicked is not None:
            self.clicked.connect(clicked)

    def connect(self, func):
        return self.clicked.connect(func)


class BigButton(Button):
    def __init__(self, text, parent=None, tooltip=None, clicked=None, *args, **kwargs):
        super(BigButton, self).__init__(text, parent, tooltip, clicked, shadow=True, *args, **kwargs)
        self.setStyleSheet(styles.big_button_style)
        self.setFixedHeight(60*config.hr)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


class AddButton(Button):
    def __init__(self, parent=None, clicked=None, *args, **kwargs):
        super(AddButton, self).__init__('+', parent, clicked=clicked, shadow=True, *args, **kwargs)
        self.setStyleSheet(styles.add_button_style)
        self.setFixedHeight(16*config.hr)
        self.setFixedWidth(16*config.wr)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


class DeleteButton(Button):
    def __init__(self, parent=None, clicked=None, *args, **kwargs):
        super(DeleteButton, self).__init__('x', parent, clicked=None, shadow=True, *args, **kwargs)
        self.setStyleSheet(styles.delete_button_style)
        self.setFixedHeight(16*config.hr)
        self.setFixedWidth(16*config.wr)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
