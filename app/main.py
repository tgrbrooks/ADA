# Local imports
from gui.main_window import App
import configuration as config
from ada.logger import logger
from fbs_runtime.application_context.PyQt5 import ApplicationContext

# Standard imports
import sys

# pyqt5 imports
#from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    appctxt = ApplicationContext()

    screen = appctxt.app.primaryScreen()
    size = screen.availableGeometry()
    config.wr = size.width()/1280.
    config.hr = size.width()/1280.
    logger.info('Configuring screen dimensions width = %.2f, height = %.2f' % (size.width(), size.height()))

    logger.info('Starting application')
    ex = App()

    sys.exit(appctxt.app.exec_())
    logger.info('Closing application')
