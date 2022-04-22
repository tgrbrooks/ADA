from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtCore import Qt
from ada.components.layout_widget import LayoutWidget

class Form(LayoutWidget):

    def __init__(self, parent=None, align=False, style=None):
        super(Form, self).__init__(layout=QFormLayout, parent=parent, style=style)
        if align:
            self.layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.layout.setLabelAlignment(Qt.AlignCenter)

    def addRow(self, widget, pad=False):
        if pad:
            return self.layout.addRow(' ', widget)
        self.layout.addRow(widget)
        return widget

    def addRows(self, widgets, padding=None):
        for i, widget in enumerate(widgets):
            if padding is not None:
                self.addRow(widget, pad=padding[i])
            else:
                self.layout.addRow(widget)
        return widgets