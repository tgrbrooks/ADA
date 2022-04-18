from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from ada.gui.error_window import error_wrapper
from ada.components.button import Button
from ada.components.user_input import DropDown, TextEntry, ParameterBounds, CheckBox
from ada.components.spacer import Spacer
from ada.components.window import Window
from ada.components.layout_widget import LayoutWidget
from ada.data.models import get_model
from ada.data.data_manager import data_manager
import ada.configuration as config
from ada.logger import logger


# Class for a table constructor window
class FitWindow(Window):

    def __init__(self, parent=None):
        super(FitWindow, self).__init__('Fit Curve', 200, 150, QHBoxLayout, parent)
        self.rows = []
        self.bounds = []
        self.initUI()

    def initUI(self):
        fit_config = LayoutWidget(QVBoxLayout)

        # List of row options
        self.curve_option = DropDown('Data:', [], self)
        for data in data_manager.get_growth_data_files():
            self.curve_option.addItem(data.label)
        fit_config.addWidget(self.curve_option)

        self.fit_option = DropDown('Fit:', config.fit_options, self)
        fit_config.addWidget(self.fit_option)

        self.fit_from = TextEntry('From:', self, config.fit_from)
        fit_config.addWidget(self.fit_from)

        self.fit_to = TextEntry('To:', self, config.fit_to)
        fit_config.addWidget(self.fit_to)

        self.set_bounds = CheckBox('Set parameter bounds', self)
        self.set_bounds.entry.stateChanged.connect(self.render_bounds)
        fit_config.addWidget(self.set_bounds)

        # Button to add a new row
        fit_button = Button("Fit", self)
        fit_button.clicked.connect(self.fit)
        fit_config.addWidget(fit_button)

        self.window.addWidget(fit_config.widget)

        self.bound_input = LayoutWidget(QVBoxLayout)
        self.param_bounds = ParameterBounds("p", self)
        self.bound_input.addWidget(self.param_bounds)

        self.window.addWidget(self.bound_input.widget)
        self.bound_input.hide()

    @error_wrapper
    def render_bounds(self):
        self.bounds = []
        self.bound_input.clear()
        if self.set_bounds.isChecked():
            self.resize(self.width * 3, self.height)
            model = get_model(self.fit_option.currentText(), '', '')
            for i, param in enumerate(model.params):
                self.bounds.append(ParameterBounds(param, self))
                self.bound_input.addWidget(self.bounds[i])
            self.bound_input.addWidget(Spacer())
            self.bound_input.show()
        else:
            self.bound_input.hide()
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
