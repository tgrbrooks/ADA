from PyQt5.QtWidgets import QListWidget, QSizePolicy

import ada.styles as styles


class List(QListWidget):
    def __init__(self, parent=False, tooltip=None, scroll=False, *args, **kwargs):
        super(List, self).__init__(parent, *args, **kwargs)

        self.setStyleSheet(styles.scroll_style)

        if tooltip is not None:
            self.setToolTip(tooltip)

        if scroll:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
