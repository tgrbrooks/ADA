import csv
import numpy as np

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QLabel, QWidget,
                             QPushButton, QComboBox, QLineEdit, QHBoxLayout)

from gui.error_window import error_wrapper
from components.label import Label
from components.button import Button
from components.user_input import DropDown, TextEntry, ParameterBounds, CheckBox
from components.spacer import Spacer
from data.models import get_model
from data.data_manager import data_manager
from type_functions import isfloat
import configuration as config
import styles as styles
from logger import logger


# Class for a table constructor window
class FitWindow(QMainWindow):

    def __init__(self, parent=None):
        super(FitWindow, self).__init__(parent)
        self.title = 'Fit Curve'
        self.width = 200*config.wr
        self.height = 150*config.hr
        logger.debug('Creating fit window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        self.parent = parent
        self.rows = []
        self.bounds = []
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)

        window_layout = QHBoxLayout()
        window_layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        window_layout.setSpacing(5*config.wr)

        fit_layout = QVBoxLayout()

        # List of row options
        self.curve_option = DropDown('Data:', [], self)
        for data in data_manager.get_growth_data_files():
            self.curve_option.addItem(data.label)
        fit_layout.addWidget(self.curve_option)

        self.fit_option = DropDown('Fit:', config.fit_options, self)
        fit_layout.addWidget(self.fit_option)

        self.fit_from = TextEntry('From:', self, config.fit_from)
        fit_layout.addWidget(self.fit_from)

        self.fit_to = TextEntry('To:', self, config.fit_to)
        fit_layout.addWidget(self.fit_to)

        self.set_bounds = CheckBox('Set parameter bounds', self)
        self.set_bounds.entry.stateChanged.connect(self.render_bounds)
        fit_layout.addWidget(self.set_bounds)

        # Button to add a new row
        fit_button = Button("Fit", self)
        fit_button.clicked.connect(self.fit)
        fit_layout.addWidget(fit_button)

        fit_widget = QWidget()
        fit_widget.setLayout(fit_layout)
        window_layout.addWidget(fit_widget)

        self.bound_layout = QVBoxLayout()
        self.param_bounds = ParameterBounds("p", self)
        self.bound_layout.addWidget(self.param_bounds)

        self.bound_widget = QWidget()
        self.bound_widget.setLayout(self.bound_layout)
        window_layout.addWidget(self.bound_widget)
        self.bound_widget.hide()

        widget = QWidget()
        widget.setLayout(window_layout)

        self.setCentralWidget(widget)
        self.resize(self.width, self.height)

    @error_wrapper
    def render_bounds(self):
        self.bounds = []
        for i in reversed(range(self.bound_layout.count())): 
            self.bound_layout.itemAt(i).widget().setParent(None)
        if self.set_bounds.isChecked():
            self.resize(self.width * 3, self.height)
            model = get_model(self.fit_option.currentText(), '', '')
            for i, param in enumerate(model.params):
                self.bounds.append(ParameterBounds(param, self))
                self.bound_layout.addWidget(self.bounds[i])
            self.bound_layout.addWidget(Spacer())
            self.bound_widget.setLayout(self.bound_layout)
            self.bound_widget.show()
        else:
            self.bound_widget.hide()
            self.resize(self.width, self.height)


    # Add the fit info to the configuration
    @error_wrapper
    def fit(self):
        config.do_fit = True
        config.fit_curve = self.curve_option.currentText()
        config.fit_type = self.fit_option.currentText()
        logger.debug('Fitting %s with %s' %
                     (config.fit_curve, config.fit_type))
        config.fit_from = self.fit_from.get_float()
        config.fit_to = self.fit_to.get_float()
        config.fit_start = []
        config.fit_min = []
        config.fit_max = []
        for bound in self.bounds:
            config.fit_start.append(bound.get_start())
            config.fit_min.append(bound.get_min())
            config.fit_max.append(bound.get_max())
        if len(config.fit_start) == 0:
            config.fit_start = None
            config.fit_min = None
            config.fit_max = None
        self.parent.update_plot()
        self.close()
