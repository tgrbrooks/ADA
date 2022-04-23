from PyQt5.QtWidgets import QWidget, QSizePolicy

class Spacer(QWidget):
    def __init__(self, width=None, height=None, *args, **kwargs):
        super(Spacer, self).__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
