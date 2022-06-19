from PyQt5.QtWidgets import (QMainWindow, QTabWidget)

from ada.configuration import config
import ada.styles as styles
from ada.logger import logger
from ada.components.layout_widget import LayoutWidget


# Base class for pop up windows
class Window(QMainWindow):

    def __init__(self, name, width, height, layout=None, parent=None, tabbed=False):
        super(Window, self).__init__(parent)
        self.title = name
        self.width = width*config['width_ratio']
        self.height = height*config['height_ratio']
        logger.debug('Creating %s window [width:%.2f, height:%.2f]' % (
            name, self.width, self.height))
        self.parent = parent

        self.setWindowTitle(self.title)

        if tabbed:
            self.tabs = QTabWidget()
        else:
            self.window = LayoutWidget(layout)
            self.window.layout.setContentsMargins(
                5*config['width_ratio'], 5*config['height_ratio'], 5*config['width_ratio'], 5*config['height_ratio'])
            self.window.layout.setSpacing(5*config['width_ratio'])

        if tabbed:
            self.tabs.setStyleSheet(styles.tab_style)
            self.setCentralWidget(self.tabs)
        else:
            self.setCentralWidget(self.window.widget)
        self.resize(self.width, self.height)