from PyQt5.QtWidgets import (QMainWindow, QWidget)

import ada.configuration as config
from ada.logger import logger
from ada.components.layout_widget import LayoutWidget


# Base class for pop up windows
class Window(QMainWindow):

    def __init__(self, name, width, height, layout, parent=None):
        super(Window, self).__init__(parent)
        self.title = name
        self.width = width*config.wr
        self.height = height*config.hr
        logger.debug('Creating %s window [width:%.2f, height:%.2f]' % (
            name, self.width, self.height))
        self.parent = parent

        self.setWindowTitle(self.title)

        self.window = LayoutWidget(layout)
        self.window.layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        self.window.layout.setSpacing(5*config.wr)

        self.setCentralWidget(self.window.widget)
        self.resize(self.width, self.height)