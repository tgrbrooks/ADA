from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from ada.gui.error_window import error_wrapper
from ada.components.button import Button
from ada.components.user_input import DropDown, TextEntry, ParameterBounds, CheckBox
from ada.components.spacer import Spacer
from ada.components.window import Window
from ada.components.layout_widget import LayoutWidget
from ada.data.models import get_model
from ada.data.data_manager import data_manager
from ada.configuration import config
import ada.options as opt
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
        self.curve_option, self.fit_option, self.fit_from, self.fit_to, self.set_bounds, _ = fit_config.addWidgets([
            DropDown('Data:', data_manager.get_growth_data_labels()),
            DropDown('Fit:', opt.fit_options),
            TextEntry('From:', default=config['fit']['from']),
            TextEntry('To:', default=config['fit']['to']),
            CheckBox('Set parameter bounds', change_action=self.render_bounds),
            Button("Fit", clicked=self.fit)])

        self.window.addWidget(fit_config.widget)

        self.bound_input = LayoutWidget(QVBoxLayout)
        self.param_bounds = self.bound_input.addWidget(ParameterBounds("p"))

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
                self.bounds.append(ParameterBounds(param))
                self.bound_input.addWidget(self.bounds[i])
            self.bound_input.addWidget(Spacer())
            self.bound_input.show()
        else:
            self.bound_input.hide()
            self.resize(self.width, self.height)


    # Add the fit info to the configuration
    @error_wrapper
    def fit(self):
        logger.debug('Fitting %s with %s' %
                     (self.curve_option.currentText(), self.fit_option.currentText()))
        config['fit'] = {
            'do_fit': True,
            'curve': self.curve_option.currentText(),
            'type': self.fit_option.currentText(),
            'from': self.fit_from.get_float(),
            'to': self.fit_to.get_float(),
            'start': [bound.get_start() for bound in self.bounds],
            'min': [bound.get_min() for bound in self.bounds],
            'max': [bound.get_max() for bound in self.bounds]
        }
        if len(config['fit']['start']) == 0:
            config['fit']['start'] = None
            config['fit']['min'] = None
            config['fit']['max'] = None
        self.parent.update_plot()
        self.close()
