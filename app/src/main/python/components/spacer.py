from PyQt5.QtWidgets import QWidget, QSizePolicy

import configuration as config


class Spacer(QWidget):
    def __init__(self, *args, **kwargs):
        super(Spacer, self).__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
