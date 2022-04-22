from PyQt5.QtWidgets import QListWidget, QSizePolicy

import ada.styles as styles


class List(QListWidget):
    def __init__(self, parent=None, tooltip=None, scroll=False, spacing=None, style=None, *args, **kwargs):
        super(List, self).__init__(parent, *args, **kwargs)

        self.setStyleSheet(styles.scroll_style)

        if tooltip is not None:
            self.setToolTip(tooltip)

        if scroll:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if spacing is not None:
            self.setSpacing(spacing)

        if style is not None:
            self.setStyleSheet(style)
