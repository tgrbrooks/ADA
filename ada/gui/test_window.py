from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget)

from ada.gui.error_window import error_wrapper
from ada.components.button import Button
from ada.components.user_input import DropDown, TextEntry
from ada.data.models import get_model
from ada.data.data_manager import data_manager
import ada.configuration as config
from ada.logger import logger


# Class for a table constructor window
class TestWindow(QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)
        self.title = 'Statistical test'
        self.width = 200*config.wr
        self.height = 150*config.hr
        logger.debug('Creating test window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)

        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        window_layout.setSpacing(5*config.wr)

        test_layout = QVBoxLayout()

        self.test_option = DropDown('Test:', config.test_options, self)
        self.test_option.entry.currentTextChanged.connect(self.render_test)
        test_layout.addWidget(self.test_option)

        # List of row options
        self.data_layout = QVBoxLayout()
        self.data_option1 = DropDown('Sample 1:', [], self)
        self.data_option2 = DropDown('Sample 2:', [], self)
        for data in data_manager.get_growth_data_files():
            self.data_option1.addItem(data.label)
            self.data_option2.addItem(data.label)
        self.data_layout.addWidget(self.data_option1)
        self.data_layout.addWidget(self.data_option2)
        self.data_widget = QWidget()
        self.data_widget.setLayout(self.data_layout)
        test_layout.addWidget(self.data_widget)

        self.test_measurement = DropDown('Measurement:', config.measurement_options, self)
        self.test_measurement.entry.currentTextChanged.connect(self.render_measurement)
        test_layout.addWidget(self.test_measurement)

        self.measurement_layout = QVBoxLayout()

        self.measurement_widget = QWidget()
        self.measurement_widget.setLayout(self.measurement_layout)
        test_layout.addWidget(self.measurement_widget)
        self.measurement_widget.hide()

        # Button to add a new row
        test_button = Button("Test", self)
        test_button.clicked.connect(self.test)
        test_layout.addWidget(test_button)

        test_widget = QWidget()
        test_widget.setLayout(test_layout)
        window_layout.addWidget(test_widget)

        widget = QWidget()
        widget.setLayout(window_layout)

        self.setCentralWidget(widget)
        self.resize(self.width, self.height)

    @error_wrapper
    def render_test(self):
        option = self.test_option.currentText()
        if option == 'T-test':
            self.data_widget.show()
        else:
            self.data_widget.hide()
            
    @error_wrapper
    def render_measurement(self):
        for i in reversed(range(self.measurement_layout.count())): 
            self.measurement_layout.itemAt(i).widget().setParent(None)
        option = self.test_measurement.currentText()
        if option == 'gradient':
            self.grad_from = TextEntry('Between:', self.measurement_widget, -1)
            self.grad_from.setPlaceholderText('Y = ')
            self.measurement_layout.addWidget(self.grad_from)
            self.grad_to = TextEntry('And:', self.measurement_widget, -1)
            self.grad_to.setPlaceholderText('Y = ')
            self.measurement_layout.addWidget(self.grad_to)
            self.measurement_widget.show()
        elif option == 'time to':
            self.time_to = TextEntry('To reach:', self.measurement_widget, -1)
            self.time_to.setPlaceholderText('Y = ')
            self.measurement_layout.addWidget(self.time_to)
            self.measurement_widget.show()
        elif option == 'fit parameter':
            self.fit = DropDown('Fit:', config.fit_options, self.measurement_widget)
            self.fit.entry.currentTextChanged.connect(self.update_param_list)
            self.measurement_layout.addWidget(self.fit)
            model = get_model(self.fit.currentText(), '', '')
            self.param = DropDown('Parameter:', model.params, self.measurement_widget)
            self.measurement_layout.addWidget(self.param)
            self.fit_from = TextEntry('From:', self.measurement_widget, -1)
            self.fit_from.setPlaceholderText(config.xvar)
            self.measurement_layout.addWidget(self.fit_from)
            self.fit_to = TextEntry('To:', self.measurement_widget, -1)
            self.fit_to.setPlaceholderText(config.xvar)
            self.measurement_layout.addWidget(self.fit_to)
            self.measurement_widget.show()
        else:
            self.measurement_widget.hide()

    
    def update_param_list(self, fit_name):
        self.param.clear()
        model = get_model(fit_name, "", "")
        self.param.addItems(model.params)

    # Add the fit info to the configuration
    @error_wrapper
    def test(self):
        config.do_fit = True
        test_type = self.test_option.currentText()
        data1 = self.data_option1.currentText()
        data2 = self.data_option2.currentText()
        logger.debug('Testing %s and %s with %s' %
                     (data1, data2, test_type))
        # Get replicates of sample 1
        # Get replicates of sample 2
        # Calculate value of all replicates individually
        # Calculate test result
        # Display test result
