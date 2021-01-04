# Local imports
from ada.gui.main_window import App
import ada.configuration as config

# Standard imports
import sys

# pyqt5 imports
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    size = screen.availableGeometry()
    config.wr = size.width()/1280.
    config.hr = size.width()/1280.
    #config.hr = size.height()/777.

    ex = App()

    sys.exit(app.exec_())
