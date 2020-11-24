from PyQt5.QtWidgets import QWidget, QListWidget, QGraphicsDropShadowEffect

import algaeplot.configuration as config


class List(QListWidget):
    def __init__(self, parent=False, tooltip=None, *args, **kwargs):
        super(List, self).__init__(parent, *args, **kwargs)
        
        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=1, yOffset=1)
        self.setGraphicsEffect(shadow)
        if tooltip is not None:
            self.setToolTip(tooltip)
