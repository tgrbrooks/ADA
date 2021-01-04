# Local imports
from gui.main_window import App
import configuration as config
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
    #config.hr = size.height()/777.

    ex = App()

    sys.exit(appctxt.app.exec_())
