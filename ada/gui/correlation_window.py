import numpy as np

# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect)

# Local application imports
from ada.plotter.correlation_plot import CorrelationCanvas
from ada.data.models import get_model
from ada.components.user_input import TextEntry, DropDown
from ada.components.button import Button, BigButton
from ada.gui.error_window import ErrorWindow
from ada.gui.file_handler import get_file_names, get_save_file_name
import ada.configuration as config
import ada.styles as styles
from ada.logger import logger


class CorrelationWindow(QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self.title = 'Correlations'
        self.parent = parent
        # Default dimensions
        self.left = 10 * config.wr
        self.top = 60 * config.wr
        self.width = 500 * config.wr
        self.height = 350 * config.wr
        logger.debug('Creating correlation window [left:%.2f, top:%.2f, width:%.2f, height:%.2f]' % (
            self.left, self.top, self.width, self.height))
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
        config_layout.setSpacing(5*config.wr)

        # X axis selection = condition variable
        # Dropdown of condition variables OR take from main plot
        self.condition = DropDown('X-axis: Average of', [], self)
        if len(self.parent.condition_data.data_files) > 0:
            for sig in self.parent.condition_data.data_files[0].signals:
                self.condition.addItem(sig.name)
        config_layout.addWidget(self.condition)
        # Average between times
        average_layout = QHBoxLayout()
        self.start_t = TextEntry('Between:', self, -1)
        self.start_t.setPlaceholderText(config.xvar)
        average_layout.addWidget(self.start_t)
        self.end_t = TextEntry('And:', self, -1)
        self.end_t.setPlaceholderText(config.xvar)
        average_layout.addWidget(self.end_t)
        average_widget = QWidget()
        average_widget.setLayout(average_layout)
        config_layout.addWidget(average_widget)

        # Y axis selection = growth related measurement
        # Dropdown of y variables (OD/CD) OR take from main plot
        self.data = DropDown('Y-axis:', [], self)
        if len(self.parent.data.data_files) > 0:
            for sig in self.parent.data.data_files[0].signals:
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
        self.fit_from = TextEntry('From:', self, -1)
        self.fit_from.setPlaceholderText(config.xvar)
        range_layout.addWidget(self.fit_from)
        self.fit_to = TextEntry('To:', self, -1)
        self.fit_to.setPlaceholderText(config.xvar)
        range_layout.addWidget(self.fit_to)
        range_widget = QWidget()
        range_widget.setLayout(range_layout)
        config_layout.addWidget(range_widget)

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
        model = get_model(fit_name, "", "")
        self.param.addItems(model.params)

    # Function: Update the correlation plot
    def update_plot(self):
        logger.debug('Updating the correlation plot')
        # Process the data here
        x_data = []
        y_data = []
        try:
            self.plot.plot(x_data, y_data)
        except Exception as e:
            logger.error(str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    # Function: Save the correlation plot
    def save_plot(self):
        logger.info('Saving the correlation plot')
        try:
            self.plot.save()
        except Exception as e:
            logger.error(str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()