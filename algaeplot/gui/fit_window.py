import csv
import numpy as np

from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QLabel, QWidget,
                             QPushButton, QComboBox, QLineEdit)

from algaeplot.gui.error_window import ErrorWindow
from algaeplot.components.label import Label
from algaeplot.components.button import Button
from algaeplot.type_functions import isfloat
import algaeplot.configuration as config


# Class for a table constructor window
class FitWindow(QMainWindow):

    def __init__(self, parent=None):
        super(FitWindow, self).__init__(parent)
        self.title = 'Fit Curve'
        self.width = 250
        self.height = 150
        self.parent = parent
        self.rows = []
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        fit_layout = QGridLayout()
        fit_layout.setContentsMargins(5, 5, 5, 5)
        fit_layout.setSpacing(5)

        # List of row options
        self.curve_option = QComboBox(self)
        for data in self.parent.data.data_files:
            self.curve_option.addItem(data.label)
        fit_layout.addWidget(self.curve_option, 0, 0, 1, 2)

        self.fit_option = QComboBox(self)
        self.fit_option.addItem("Flat line")
        self.fit_option.addItem("Linear")
        self.fit_option.addItem("Quadratic")
        self.fit_option.addItem("Exponential")
        fit_layout.addWidget(self.fit_option, 1, 0, 1, 2)

        fit_layout.addWidget(Label('From:'), 2, 0)
        fit_layout.addWidget(Label('To:'), 2, 1)

        self.fit_from = QLineEdit(self)
        fit_layout.addWidget(self.fit_from, 3, 0)

        self.fit_to = QLineEdit(self)
        fit_layout.addWidget(self.fit_to, 3, 1)

        # Button to add a new row
        fit_button = Button("Fit", self)
        fit_button.clicked.connect(self.fit)
        fit_layout.addWidget(fit_button, 4, 0, 1, 2)

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
