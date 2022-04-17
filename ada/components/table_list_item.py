from PyQt5.QtWidgets import QListWidgetItem, QHBoxLayout, QWidget

from ada.components.button import DeleteButton
from ada.components.label import RoundLabel
from ada.components.user_input import DropDown, TextEntry, CheckBox
from ada.data.models import get_model
from ada.data.data_manager import data_manager
import ada.configuration as config


class TableListItem():

    def __init__(self, text, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        self.type = text

        # Horizontal box layout
        layout = QHBoxLayout()

        spacer = QWidget()
        spacer.setFixedWidth(10*config.wr)
        layout.addWidget(spacer)

        # Add a delete button
        del_button = DeleteButton()
        del_button.clicked.connect(parent.remove_item)
        layout.addWidget(del_button)

        # Add a label with row type
        if(text == 'profile'):
            layout.addWidget(RoundLabel('Profile'))

        if(text == 'reactor'):
            layout.addWidget(RoundLabel('Reactor'))

        # Add other options based on type
        # Gradient needs a start and end measurement point in Y
        if(text == 'gradient'):
            self.data = DropDown('Gradient of:', [], self.widget)
            for sig in data_manager.get_growth_variables():
                self.data.addItem(sig)
            layout.addWidget(self.data)
            self.grad_from = TextEntry('Between:', self.widget, -1)
            self.grad_from.setPlaceholderText('Y = ')
            layout.addWidget(self.grad_from)
            self.grad_to = TextEntry('And:', self.widget, -1)
            self.grad_to.setPlaceholderText('Y = ')
            layout.addWidget(self.grad_to)

        # Time to needs a Y point to reach
        if(text == 'time to'):
            self.data = DropDown('Time for:', [], self.widget)
            for sig in data_manager.get_growth_variables():
                self.data.addItem(sig)
            layout.addWidget(self.data)
            self.time_to = TextEntry('To reach:', self.widget, -1)
            self.time_to.setPlaceholderText('Y = ')
            layout.addWidget(self.time_to)

        # Average of a condition needs condition and start and end time
        if(text == 'average of condition'):
            self.condition = DropDown('Average of:', [], self.widget)
            for sig in data_manager.get_condition_variables():
                self.condition.addItem(sig)
            layout.addWidget(self.condition)
            self.start_t = TextEntry('Between:', self.widget, -1)
            self.start_t.setPlaceholderText(config.xvar)
            layout.addWidget(self.start_t)
            self.end_t = TextEntry('And:', self.widget, -1)
            self.end_t.setPlaceholderText(config.xvar)
            layout.addWidget(self.end_t)

        # Condition at time needs condition and time
        if(text == 'condition at time'):
            self.condition = DropDown('Value of:', [], self.widget)
            for sig in data_manager.get_condition_variables():
                self.condition.addItem(sig)
            layout.addWidget(self.condition)
            self.time = TextEntry('At:', self.widget, -1)
            self.time.setPlaceholderText(config.xvar)
            layout.addWidget(self.time)

        # Value of fit parameter needs fit and parameter
        if(text == 'fit parameter'):
            self.fit = DropDown('Fit:', config.fit_options, self.widget)
            self.fit.entry.currentTextChanged.connect(self.update_param_list)
            layout.addWidget(self.fit)
            self.data = DropDown('Data:', [], self.widget)
            for sig in data_manager.get_growth_variables():
                self.data.addItem(sig)
            layout.addWidget(self.data)
            model = get_model(self.fit.currentText(), '', '')
            self.param = DropDown('Parameter:', model.params, self.widget)
            layout.addWidget(self.param)
            self.fit_from = TextEntry('From:', self.widget, -1)
            self.fit_from.setPlaceholderText(config.xvar)
            layout.addWidget(self.fit_from)
            self.fit_to = TextEntry('To:', self.widget, -1)
            self.fit_to.setPlaceholderText(config.xvar)
            layout.addWidget(self.fit_to)
            self.show_error = CheckBox("Show error")
            layout.addWidget(self.show_error)

        # Pad out the row
        layout.addStretch()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 50, 5)

        self.widget.setLayout(layout)
        self.item.setSizeHint(self.widget.sizeHint())

    def update_param_list(self, fit_name):
        self.param.clear()
        model = get_model(fit_name, "", "")
        self.param.addItems(model.params)
