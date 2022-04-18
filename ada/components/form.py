from PyQt5.QtWidgets import QWidget, QFormLayout
from ada.components.layout_widget import LayoutWidget

class Form(LayoutWidget):

    def __init__(self, parent=None):
        super(Form, self).__init__(layout=QFormLayout, parent=parent)

    def addRow(self, widget, pad=False):
        if pad:
            return self.layout.addRow(' ', widget)
        return self.layout.addRow(widget)
