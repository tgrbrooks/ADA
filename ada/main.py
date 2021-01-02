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
    print(size.width(), size.height())
    config.width_ratio = size.width()/1280.
    config.height_ratio = size.height()/777.

    ex = App()

    sys.exit(app.exec_())
