from PyQt5.QtWidgets import (QListWidgetItem, QHBoxLayout, QLayout,
    QPushButton, QLabel, QWidget, QLineEdit, QComboBox, QSizePolicy)

from algaeplot.components.button import DeleteButton
from algaeplot.components.label import Label, RoundLabel
from algaeplot.components.user_input import DropDown, TextEntry
import algaeplot.configuration as config


class TableListItem():

    def __init__(self, text, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        self.type = text

        # Horizontal box layout
        layout = QHBoxLayout()

        spacer = QWidget()
        spacer.setFixedWidth(10)
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
            if len(parent.parent.data.data_files) > 0:
                for sig in parent.parent.data.data_files[0].signals:
                    self.data.addItem(sig.name)
            layout.addWidget(self.data)
            self.grad_from = TextEntry('Between:', self.widget)
            layout.addWidget(self.grad_from)
            self.grad_to = TextEntry('And:', self.widget)
            layout.addWidget(self.grad_to)

        # Time to needs a Y point to reach
        if(text == 'time to'):
            self.data = DropDown('Time for:', [], self.widget)
            if len(parent.parent.data.data_files) > 0:
                for sig in parent.parent.data.data_files[0].signals:
                    self.data.addItem(sig.name)
            layout.addWidget(self.data)
            self.time_to = TextEntry('To reach:', self.widget)
            layout.addWidget(self.time_to)

        # Average of a condition needs condition and start and end time
        if(text == 'average of condition'):
            self.condition = DropDown('Average of:', [], self.widget)
            if len(parent.parent.condition_data.data_files) > 0:
                for sig in parent.parent.condition_data.data_files[0].signals:
                    self.condition.addItem(sig.name)
            layout.addWidget(self.condition)
            self.start_t = TextEntry('Between time:', self.widget)
            layout.addWidget(self.start_t)
            self.end_t = TextEntry('And:', self.widget)
            layout.addWidget(self.end_t)

        # Condition at time needs condition and time
        if(text == 'condition at time'):
            self.condition = DropDown('Value of:', [], self.widget)
            if len(parent.parent.condition_data.data_files) > 0:
                for sig in parent.parent.condition_data.data_files[0].signals:
                    self.condition.addItem(sig.name)
            layout.addWidget(self.condition)
            self.time = TextEntry('At time:', self.widget)
            layout.addWidget(self.time)

        # Value of fit parameter needs fit and parameter
        if(text == 'fit parameter'):
            self.fit = DropDown('Fit:', [], self.widget)
            self.fit.addItem('y = p0')
            self.fit.addItem('y = p1*x + p0')
            self.fit.addItem('y = p2*x^2 + p1*x + p0')
            self.fit.addItem('y = p0*exp(p1*x)')
            self.fit.entry.setFixedWidth(220)
            self.fit.entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addWidget(self.fit)
            self.data = DropDown('Data:', [], self.widget)
            if len(parent.parent.data.data_files) > 0:
                for sig in parent.parent.data.data_files[0].signals:
                    self.data.addItem(sig.name)
            layout.addWidget(self.data)
            self.param = DropDown('Parameter:', [], self.widget)
            self.param.addItem('p0')
            self.param.addItem('p1')
            self.param.addItem('p2')
            self.param.entry.setFixedWidth(75)
            self.param.entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addWidget(self.param)
            self.fit_from = TextEntry('From:', self.widget)
            layout.addWidget(self.fit_from)
            self.fit_to = TextEntry('To:', self.widget)
            layout.addWidget(self.fit_to)

        # Pad out the row
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget.setLayout(layout)
        self.item.setSizeHint(self.widget.sizeHint())
