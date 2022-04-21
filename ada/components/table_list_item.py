from PyQt5.QtWidgets import QListWidgetItem, QHBoxLayout, QWidget

from ada.components.button import DeleteButton
from ada.components.label import RoundLabel
from ada.components.user_input import DropDown, TextEntry, CheckBox
from ada.components.layout_widget import LayoutWidget
from ada.data.models import get_model
from ada.data.data_manager import data_manager
import ada.configuration as config


class TableListItem():

    def __init__(self, text, parent=None):
        self.item = QListWidgetItem()
        self.type = text

        # Horizontal box layout
        layout = LayoutWidget(QHBoxLayout)

        spacer = layout.addWidget(QWidget())
        spacer.setFixedWidth(10*config.wr)

        # Add a delete button
        layout.addWidget(DeleteButton(clicked=parent.remove_item))

        # Add a label with row type
        if(text == 'profile'):
            layout.addWidget(RoundLabel('Profile'))

        if(text == 'reactor'):
            layout.addWidget(RoundLabel('Reactor'))

        # Add other options based on type
        # Gradient needs a start and end measurement point in Y
        if(text == 'gradient'):
            self.data, self.grad_from, self.grad_to = layout.addWidgets([
                DropDown('Gradient of:', data_manager.get_growth_variables()),
                TextEntry('Between:', default=-1, placeholder='Y = '),
                TextEntry('And:', default=-1, placeholder='Y = ')])

        # Time to needs a Y point to reach
        if(text == 'time to'):
            self.data, self.time_to = layout.addWidgets([
                DropDown('Time for:', data_manager.get_growth_variables()),
                TextEntry('To reach:', default=-1, placeholder='Y = ')])

        # Average of a condition needs condition and start and end time
        if(text == 'average of condition'):
            self.condition, self.start_t, self.end_t = layout.addWidgets([
                DropDown('Average of:', data_manager.get_condition_variables()),
                TextEntry('Between:', default=-1, placeholder=config.xvar),
                TextEntry('And:', default=-1, placeholder=config.xvar)])

        # Condition at time needs condition and time
        if(text == 'condition at time'):
            self.condition, self.time = layout.addWidgets([
                DropDown('Value of:', data_manager.get_condition_variables()),
                TextEntry('At:', default=-1, placeholder=config.xvar)])

        # Value of fit parameter needs fit and parameter
        if(text == 'fit parameter'):
            model = get_model(config.fit_options[0], '', '')
            self.fit, self.data, self.param, self.fit_from, self.fit_to, self.show_error = layout.addWidgets([
                DropDown('Fit:', config.fit_options, change_action=self.update_param_list),
                DropDown('Data:', data_manager.get_growth_variables()),
                DropDown('Parameter:', model.params),
                TextEntry('From:', default=-1, placeholder=config.xvar),
                TextEntry('To:', default=-1, placeholder=config.xvar),
                CheckBox("Show error")])

        # Pad out the row
        layout.layout.addStretch()
        layout.layout.setSpacing(5)
        layout.layout.setContentsMargins(10, 10, 50, 5)

        self.widget = layout.widget
        self.item.setSizeHint(self.widget.sizeHint())

    def update_param_list(self, fit_name):
        self.param.clear()
        model = get_model(fit_name, "", "")
        self.param.addItems(model.params)
