from PyQt5.QtWidgets import QWidget
from ada.configuration import config


class LayoutWidget(QWidget):

    def __init__(self, layout, margin=None, spacing=None, parent=None, style=None):
        super(LayoutWidget, self).__init__(parent)
        self.layout = layout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        if margin is not None:
            self.layout.setContentsMargins(
                margin*config['width_ratio'], margin*config['height_ratio'], margin*config['width_ratio'], margin*config['height_ratio'])
        if spacing is not None:
            self.layout.setSpacing(spacing*config['width_ratio'])
        if style:
            self.widget.setStyleSheet(style)

    def addWidget(self, widget, *args):
        self.layout.addWidget(widget, *args)
        return widget

    def addWidgets(self, widgets):
        for widget in widgets:
            self.layout.addWidget(widget)
        return widgets

    def show(self):
        return self.widget.show()

    def hide(self):
        return self.widget.hide()

    def clear(self): 
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
