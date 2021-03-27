import numpy as np
import math

# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect)

# Local application imports
from ada.plotter.correlation_plot import CorrelationCanvas
from ada.data.models import get_model
from ada.data.data_manager import data_manager
from ada.components.user_input import TextEntry, DropDown, CheckBox
from ada.components.button import Button, BigButton
from ada.gui.error_window import ErrorWindow
from ada.gui.file_handler import get_file_names, get_save_file_name
import ada.configuration as config
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


class CorrelationWindow(QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self.title = 'Correlations'
        self.parent = parent
        # Default dimensions
        self.left = 10 * config.wr
        self.top = 60 * config.wr
        self.width = 600 * config.wr
        self.height = 350 * config.wr
        logger.debug('Creating correlation window [left:%.2f, top:%.2f, width:%.2f, height:%.2f]' % (
            self.left, self.top, self.width, self.height))
        self.plot_config = PlotConfig()
        self.setStyleSheet(styles.main_background)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Tabs: configuration and plot
        tabs = QTabWidget()
        tabs.setStyleSheet(styles.tab_style)

        # Configuration tab
        config_layout = QVBoxLayout()
        config_layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        config_layout.setSpacing(0*config.wr)

        # X axis selection = condition variable
        # Dropdown of condition variables OR take from main plot
        self.condition = DropDown('X-axis: Average of', [], self)
        if len(data_manager.get_condition_data_files()) > 0:
            for sig in data_manager.get_condition_variables():
                self.condition.addItem(sig.name)
        config_layout.addWidget(self.condition)

        # Y axis selection = growth related measurement
        # Dropdown of y variables (OD/CD) OR take from main plot
        self.data = DropDown('Y-axis:', [], self)
        if len(data_manager.get_growth_data_files()) > 0:
            for sig in data_manager.get_growth_variables():
                self.data.addItem(sig.name)
        config_layout.addWidget(self.data)

        # Choice of fit and fit parameter
        fit_layout = QHBoxLayout()
        self.fit = DropDown('Fit:', config.fit_options, self)
        self.fit.entry.currentTextChanged.connect(self.update_param_list)
        fit_layout.addWidget(self.fit)
        model = get_model(self.fit.currentText(), '', '')
        self.param = DropDown('Parameter:', model.params, self)
        fit_layout.addWidget(self.param)
        fit_widget = QWidget()
        fit_widget.setLayout(fit_layout)
        config_layout.addWidget(fit_widget)

        range_layout = QHBoxLayout()
        self.start_t = TextEntry('Between:', self, -1)
        self.start_t.setPlaceholderText(config.xvar)
        range_layout.addWidget(self.start_t)
        self.end_t = TextEntry('And:', self, -1)
        self.end_t.setPlaceholderText(config.xvar)
        range_layout.addWidget(self.end_t)
        range_widget = QWidget()
        range_widget.setLayout(range_layout)
        config_layout.addWidget(range_widget)

        self.figure_title = TextEntry('Figure title:', self)
        config_layout.addWidget(self.figure_title)
        title_layout = QHBoxLayout()
        self.x_title = TextEntry('X-axis title:', self)
        title_layout.addWidget(self.x_title)
        self.y_title = TextEntry('Y-axis title:', self)
        title_layout.addWidget(self.y_title)
        title_widget = QWidget()
        title_widget.setLayout(title_layout)
        config_layout.addWidget(title_widget)

        options_layout = QHBoxLayout()
        self.label = CheckBox('Label', self)
        options_layout.addWidget(self.label)
        self.calc_correlation = CheckBox('Calculate correlation', self)
        options_layout.addWidget(self.calc_correlation)
        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        config_layout.addWidget(options_widget)

        # Plot button
        plot_button = Button('Plot', self)
        plot_button.clicked.connect(self.parent.update_config)
        plot_button.clicked.connect(self.update_plot)
        config_layout.addWidget(plot_button)

        config_widget = QWidget()
        config_widget.setLayout(config_layout)
        tabs.addTab(config_widget, 'Configuration')

        # Plot tab
        plot_layout = QGridLayout()
        plot_layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        plot_layout.setSpacing(10*config.wr)

        # Plot
        self.plot = CorrelationCanvas(
            self, width=10*config.wr, height=4*config.hr, dpi=100*config.wr)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=10*config.wr, xOffset=3*config.wr, yOffset=3*config.hr)
        self.plot.setGraphicsEffect(shadow)
        self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        plot_layout.addWidget(self.plot, 0, 0, 4, 4)

        # Save button
        save_button = Button('Save', self)
        save_button.clicked.connect(self.save_plot)
        plot_layout.addWidget(save_button, 4, 0, 1, 4)

        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        tabs.addTab(plot_widget, 'Plot')

        self.setCentralWidget(tabs)
        self.show()

    def update_param_list(self, fit_name):
        self.param.clear()
        model = get_model(fit_name)
        self.param.addItems(model.params)

    # Function: Update the correlation plot
    def update_plot(self):
        logger.debug('Updating the correlation plot')
        self.plot_config.clear()
        # Process the data here
        x_data, x_error = data_manager.get_averages(
                                       self.condition.currentText(),
                                       self.start_t.get_float(),
                                       self.end_t.get_float())
        y_data, y_error = data_manager.get_fit(self.data.currentText(),
                                  self.fit.currentText(),
                                  self.param.currentText(),
                                  self.start_t.get_float(),
                                  self.end_t.get_float())
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
        try:
            self.plot.plot(self.plot_config)
        except Exception as e:
            self.error = ErrorWindow(e, self)
            self.error.show()

    # Function: Save the correlation plot
    def save_plot(self):
        logger.info('Saving the correlation plot')
        try:
            self.plot.save()
        except Exception as e:
            self.error = ErrorWindow(e, self)
            self.error.show()
