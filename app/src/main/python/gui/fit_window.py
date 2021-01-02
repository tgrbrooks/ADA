import csv
import numpy as np

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QLabel, QWidget,
                             QPushButton, QComboBox, QLineEdit)

from gui.error_window import ErrorWindow
from components.label import Label
from components.button import Button
from components.user_input import DropDown, TextEntry
from type_functions import isfloat
import configuration as config


# Class for a table constructor window
class FitWindow(QMainWindow):

    def __init__(self, parent=None):
        super(FitWindow, self).__init__(parent)
        self.title = 'Fit Curve'
        self.width = 250*config.wr
        self.height = 150*config.hr
        self.parent = parent
        self.rows = []
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        fit_layout = QVBoxLayout()
        fit_layout.setContentsMargins(5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        fit_layout.setSpacing(5*config.wr)

        # List of row options
        self.curve_option = DropDown('Data:', [], self)
        for data in self.parent.data.data_files:
            self.curve_option.addItem(data.label)
        fit_layout.addWidget(self.curve_option)

        self.fit_option = DropDown('Fit:', config.fit_options, self)
        fit_layout.addWidget(self.fit_option)

        self.fit_from = TextEntry('From:', self)
        fit_layout.addWidget(self.fit_from)

        self.fit_to = TextEntry('To:', self)
        fit_layout.addWidget(self.fit_to)

        # Button to add a new row
        fit_button = Button("Fit", self)
        fit_button.clicked.connect(self.fit)
        fit_layout.addWidget(fit_button)

        widget = QWidget()
        widget.setLayout(fit_layout)

        self.setCentralWidget(widget)

    # Add the fit info to the configuration
    def fit(self):
        config.do_fit = True
        config.fit_curve = self.curve_option.currentText()
        config.fit_type = self.fit_option.currentText()
        if isfloat(self.fit_from.text()):
            config.fit_from = float(self.fit_from.text())
        else:
            config.fit_from = 0
        if isfloat(self.fit_to.text()):
            config.fit_to = float(self.fit_to.text())
        else:
            config.fit_to = 0
        self.parent.update_plot()
        self.close()
