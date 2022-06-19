# Local imports
from ada.gui.main_window import App
from ada.configuration import config
from ada.logger import logger

# Standard imports
import sys

# pyqt5 imports
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.availableGeometry() 
    config['width_ratio'] = size.width()/1280.
    config['height_ratio'] = size.width()/1280.
    logger.info('Configuring screen dimensions width = %.2f, height = %.2f' % (size.width(), size.height()))

    logger.info('Starting application')
    ex = App()

    sys.exit(app.exec_())
