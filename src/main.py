# Local imports
from src.gui.mainwindow import App

# Standard imports
import sys

# pyqt5 imports
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = App()
    
    sys.exit(app.exec_())
