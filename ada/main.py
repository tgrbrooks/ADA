# Local imports
from ada.gui.main_window import App
import ada.configuration as config
from ada.logger import logger

# Standard imports
import sys
import logging

# pyqt5 imports
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.availableGeometry()
    config.wr = size.width()/1280.
    config.hr = size.width()/1280.
    logger.info('Configuring screen dimensions width = %.2f, height = %.2f' % (size.width(), size.height()))

    logger.info('Starting application')
    ex = App()

    sys.exit(app.exec_())
    logger.info('Closing application')
