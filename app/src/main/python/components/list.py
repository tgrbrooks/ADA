from PyQt5.QtWidgets import QWidget, QListWidget, QGraphicsDropShadowEffect

import configuration as config
import styles as styles


class List(QListWidget):
    def __init__(self, parent=False, tooltip=None, *args, **kwargs):
        super(List, self).__init__(parent, *args, **kwargs)

        self.setStyleSheet(styles.scroll_style)

        if tooltip is not None:
            self.setToolTip(tooltip)
