import numpy as np

# Related third party imports
from PyQt5.QtWidgets import (QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect)

# Local application imports
from ada.plotter.correlation_plot import CorrelationCanvas
from ada.data.models import get_model
from ada.data.data_manager import data_manager
from ada.components.user_input import TextEntry, DropDown, CheckBox
from ada.components.button import Button
from ada.components.window import Window
from ada.components.layout_widget import LayoutWidget
from ada.gui.error_window import error_wrapper
import ada.configuration as config
import ada.options as opt
import ada.styles as styles
from ada.logger import logger


class PlotConfig():
    def __init__(self):
        self.clear()

    def clear(self):
        self.title = ''
        self.x_title = None
        self.y_title = None
        self.x_data = []
        self.y_data = []
        self.x_error = []
        self.y_error = []
        self.labels = []
        self.correlation_coeff = None


class CorrelationWindow(Window):

    def __init__(self, parent):
        super(CorrelationWindow, self).__init__('Correlations', 600, 350, parent=parent, tabbed=True)
        # Default dimensions
        self.left = 10 * config.wr
        self.top = 60 * config.wr
        self.plot_config = PlotConfig()
        self.setStyleSheet(styles.main_background)
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Configuration tab
        corr_config = LayoutWidget(QVBoxLayout, margin=5, spacing=0)

        # X axis selection = condition variable
        # Dropdown of condition variables OR take from main plot
        self.condition = corr_config.addWidget(
            DropDown('X-axis: Average of', data_manager.get_condition_variables()))

        # Y axis selection = growth related measurement
        # Dropdown of y variables (OD/CD) OR take from main plot
        self.data = corr_config.addWidget(
            DropDown('Y-axis:', data_manager.get_growth_variables()))

        # Choice of fit and fit parameter
        fit_option = LayoutWidget(QHBoxLayout)
        model = get_model(opt.fit_options[0])
        self.fit, self.param = fit_option.addWidgets([
            DropDown('Fit:', opt.fit_options, change_action=self.update_param_list),
            DropDown('Parameter:', model.params)])
        corr_config.addWidget(fit_option.widget)

        range_option = LayoutWidget(QHBoxLayout)
        self.start_t, self.end_t = range_option.addWidgets([
            TextEntry('Between:', default=-1, placeholder=config.xvar),
            TextEntry('And:', default=-1, placeholder=config.xvar)])
        corr_config.addWidget(range_option.widget)

        self.figure_title = corr_config.addWidget(TextEntry('Figure title:'))
        title_option = LayoutWidget(QHBoxLayout)
        self.x_title, self.y_title = title_option.addWidgets([
            TextEntry('X-axis title:'),
            TextEntry('Y-axis title:')])
        corr_config.addWidget(title_option.widget)

        options = LayoutWidget(QHBoxLayout)
        self.label, self.calc_correlation = options.addWidgets([
            CheckBox('Label'),
            CheckBox('Calculate correlation')])
        corr_config.addWidget(options.widget)

        # Plot button
        corr_config.addWidget(Button('Plot', clicked=self.update_plot))

        self.tabs.addTab(corr_config.widget, 'Configuration')

        # Plot tab
        plot_view = LayoutWidget(QGridLayout, margin=5, spacing=10)

        # Plot
        self.plot = plot_view.addWidget(
            CorrelationCanvas(self, width=10*config.wr, height=4*config.hr, dpi=100*config.wr), 0, 0, 4, 4)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=10*config.wr, xOffset=3*config.wr, yOffset=3*config.hr)
        self.plot.setGraphicsEffect(shadow)
        self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Save button
        plot_view.addWidget(Button('Save', clicked=self.save_plot), 4, 0, 1, 4)

        self.tabs.addTab(plot_view.widget, 'Plot')

    def update_param_list(self, fit_name):
        self.param.clear()
        model = get_model(fit_name)
        self.param.addItems(model.params)

    # Function: Update the correlation plot
    @error_wrapper
    def update_plot(self):
        self.parent.update_config()
        logger.debug('Updating the correlation plot')
        self.plot_config.clear()
        # Process the data here
        x_data, x_error = data_manager.get_averages(
                                       self.condition.currentText(),
                                       self.start_t.get_float(),
                                       self.end_t.get_float())
        y_data, y_error = data_manager.get_all_fit_params(self.data.currentText(),
                                  self.fit.currentText(),
                                  self.start_t.get_float(),
                                  self.end_t.get_float(),
                                  self.param.currentText())
        tunit = 's'
        if config.xvar == 'minutes':
            tunit = 'min'
        if config.xvar == 'hours':
            tunit = 'hr'
        if config.xvar == 'days':
            tunit = 'day'

        # Create the X axis title
        x_title = self.x_title.text()
        if x_title == '':
            condition_unit = data_manager.get_condition_unit(self.condition.currentText())
            x_title = ('Average %s [%s]'
                       % (self.condition.currentText(),
                          condition_unit))
        self.plot_config.x_title = x_title

        # Create the Y axis title
        y_title = self.y_title.text()
        if y_title == '':
            data_unit = data_manager.get_growth_unit(self.data.currentText())
            model = get_model(self.fit.currentText(), tunit, data_unit)
            y_title = ('%s [%s] (%s)'
                       % (model.get_latex_param(self.param.currentText()),
                          model.get_units(self.param.currentText()),
                          self.data.currentText()))
        self.plot_config.y_title = y_title

        self.plot_config.title = self.figure_title.text()
        labels = []
        for dat in data_manager.get_growth_data_files():
            labels.append('Name: %s\nReactor: %s\nProfile: %s' %
                          (dat.label, dat.reactor, dat.profile))

        # Remove any broken fits
        for i, yerr in enumerate(y_error):
            logger.debug('Fit %i: x=%.2f (%.2f), y=%.2f (%.2f)' %
                         (i, x_data[i], x_error[i], y_data[i], y_error[i]))
            if y_data[i] == 1 and yerr > 50:
                logger.warning('Fit ' + str(i) + ' failed')
            else:
                self.plot_config.x_data.append(x_data[i])
                self.plot_config.y_data.append(y_data[i])
                self.plot_config.x_error.append(x_error[i])
                self.plot_config.y_error.append(y_error[i])
                if self.label.isChecked():
                    self.plot_config.labels.append(labels[i])

        # Work out correlation coefficient
        if self.calc_correlation.isChecked():
            corr_coef = np.corrcoef(
                self.plot_config.x_data, self.plot_config.y_data)
            self.plot_config.correlation_coeff = corr_coef[1][0]
        else:
            self.plot_config.correlation_coeff = None

        self.plot.plot(self.plot_config)

    # Function: Save the correlation plot
    @error_wrapper
    def save_plot(self):
        logger.info('Saving the correlation plot')
        self.plot.save()
