from PyQt5.QtWidgets import (QWidget)


class LayoutWidget(QWidget):

    def __init__(self, layout, parent=None):
        super(LayoutWidget, self).__init__(parent)
        self.layout = layout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

    def addWidget(self, widget):
        return self.layout.addWidget(widget)

    def show(self):
        return self.widget.show()

    def hide(self):
        return self.widget.hide()

    def clear(self): 
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)
