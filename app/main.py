# Local imports
from gui.mainwindow import App
from fbs_runtime.application_context.PyQt5 import ApplicationContext

# Standard imports
import sys

# pyqt5 imports
#from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    appctxt = ApplicationContext()

    ex = App()

    sys.exit(appctxt.app.exec_())
