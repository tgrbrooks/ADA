from PyQt5.QtWidgets import QWidget
import ada.configuration as config


class LayoutWidget(QWidget):

    def __init__(self, layout, margin=None, spacing=None, parent=None):
        super(LayoutWidget, self).__init__(parent)
        self.layout = layout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        if margin:
            self.layout.setContentsMargins(
                margin*config.wr, margin*config.hr, margin*config.wr, margin*config.hr)
        if spacing:
            self.layout.setSpacing(spacing*config.wr)

    def addWidget(self, widget, *args):
        return self.layout.addWidget(widget, *args)

    def show(self):
        return self.widget.show()

    def hide(self):
        return self.widget.hide()

    def clear(self): 
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
