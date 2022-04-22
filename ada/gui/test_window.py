from scipy.stats import ttest_ind, f_oneway
from PyQt5.QtWidgets import (QVBoxLayout, QLabel)

from ada.gui.error_window import error_wrapper
from ada.components.window import Window
from ada.components.layout_widget import LayoutWidget
from ada.components.button import Button
from ada.components.spacer import Spacer
from ada.components.user_input import DropDown, TextEntry
from ada.components.label import RoundLabel
from ada.data.models import get_model
from ada.data.data_manager import data_manager
import ada.configuration as config
from ada.logger import logger


# Class for a table constructor window
class TestWindow(Window):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(
            'Statistical test', 200, 150, QVBoxLayout, parent)
        self.initUI()

    def initUI(self):
        self.test_option = self.window.addWidget(
            DropDown('Test:', config.test_options, change_action=self.render_test))

        self.data_input = LayoutWidget(QVBoxLayout)
        self.data_option1, self.data_option2 = self.data_input.addWidgets([
            DropDown('Sample 1:', data_manager.get_growth_data_labels()),
            DropDown('Sample 2:', data_manager.get_growth_data_labels())])
        self.window.addWidget(self.data_input.widget)

        self.test_measurement = self.window.addWidget(
            DropDown('Measurement:', config.measurement_options, change_action=self.render_measurement))

        self.measurement = LayoutWidget(QVBoxLayout)
        self.window.addWidget(self.measurement.widget)
        self.measurement.hide()

        self.window.addWidget(Button("Test", clicked=self.test))

        self.statistic, self.pvalue = self.window.addWidgets([
            RoundLabel("Statistic = "), RoundLabel("P value = ")])

        self.window.addWidget(Spacer())

    @error_wrapper
    def render_test(self):
        option = self.test_option.currentText()
        if option == 'T-test':
            self.data_input.show()
        else:
            self.data_input.hide()

    @error_wrapper
    def render_measurement(self):
        self.measurement.clear()
        option = self.test_measurement.currentText()
        if option == 'gradient':
            self.signal, self.grad_from, self.grad_to = self.measurement.addWidgets([
                DropDown('Gradient of:', data_manager.get_growth_variables()),
                TextEntry('Between:', placeholder='Y = '),
                TextEntry('And:', placeholder='Y = ')])
        elif option == 'time to':
            self.signal, self.time_to = self.measurement.addWidgets([
                DropDown('Time for:', data_manager.get_growth_variables()),
                TextEntry('To reach:', placeholder='Y = ')])
        elif option == 'fit parameter':
            model = get_model(config.fit_options[0])
            self.fit, self.signal, self.param, self.fit_from, self.fit_to = self.measurement.addWidgets([
                DropDown('Fit:', config.fit_options,
                         change_action=self.update_param_list),
                DropDown('Of:', data_manager.get_growth_variables()),
                DropDown('Parameter:', model.params),
                TextEntry('From:', placeholder=config.xvar),
                TextEntry('To:', placeholder=config.xvar)])
        else:
            self.measurement.hide()
            return
        self.measurement.show()
        return

    def update_param_list(self, fit_name):
        self.param.clear()
        model = get_model(fit_name, "", "")
        self.param.addItems(model.params)

    # Add the fit info to the configuration
    @error_wrapper
    def test(self):
        config.do_fit = True
        test_option = self.test_option.currentText()
        measurement_option = self.test_measurement.currentText()
        # Calculate value of all replicates individually
        measurements = []
        for i, dat in enumerate(data_manager.get_growth_data_files()):
            if test_option == 'T-test':
                data1 = self.data_option1.currentText(error=True)
                data2 = self.data_option2.currentText(error=True)
                if data1 == data2:
                    raise RuntimeError('Samples must be different')
                if dat.label != data1 and dat.label != data2:
                    continue
            signal = self.signal.currentText()
            if measurement_option == 'gradient':
                grad_from = self.grad_from.get_float(error=True)
                grad_to = self.grad_to.get_float(error=True)
                measurements.append(data_manager.get_replicate_gradients(
                    i, signal, grad_from, grad_to))
            elif measurement_option == 'time to':
                time_to = self.time_to.get_float(error=True)
                measurements.append(
                    data_manager.get_replicate_time_to(i, signal, time_to))
            elif measurement_option == 'fit parameter':
                fit_name = self.fit.currentText(error=True)
                fit_from = self.fit_from.get_float(error=True)
                fit_to = self.fit_to.get_float(error=True)
                fit_param = self.param.currentText(error=True)
                measurements.append(data_manager.get_replicate_fits(
                    i, signal, fit_name, fit_from, fit_to, fit_param))
            else:
                raise RuntimeError('Unknown measurement')
        # Calculate test result
        statistic, pvalue = -1, -1
        if test_option == 'T-test':
            if len(measurements) != 2:
                raise RuntimeError('Unable to find data for t-test')
            statistic, pvalue = ttest_ind(measurements[0], measurements[1])
        if test_option == 'ANOVA':
            statistic, pvalue = f_oneway(*measurements)
        # Display test result
        self.statistic.setText('Statistic = ' + str(statistic))
        self.pvalue.setText('P value = ' + str(pvalue))
