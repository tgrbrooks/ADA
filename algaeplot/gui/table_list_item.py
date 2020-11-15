from PyQt5.QtWidgets import QListWidgetItem, QHBoxLayout, QLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QLineEdit, QComboBox


class TableListItem():

    def __init__(self, text, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        self.type = text

        # Horizontal box layout
        layout = QHBoxLayout()

        # Add a delete button
        del_button = QPushButton('del')
        del_button.setStyleSheet(
            'background-color: #eb5a46; border-radius: 5px; padding: 2px'
        )
        del_button.clicked.connect(parent.remove_item)
        layout.addWidget(del_button)

        # Add a label with row type
        if(text == 'profile'):
            layout.addWidget(QLabel('Profile'))

        if(text == 'reactor'):
            layout.addWidget(QLabel('Reactor'))

        # Add other options based on type
        # Gradient needs a start and end measurement point in Y
        if(text == 'gradient'):
            layout.addWidget(QLabel('Gradient of:'))
            self.data = QComboBox(self.widget)
            if len(parent.parent.data.data_files) > 0:
                for sig in parent.parent.data.data_files[0].signals:
                    self.data.addItem(sig.name)
            layout.addWidget(self.data)
            layout.addWidget(QLabel('Between:'))
            self.grad_from = QLineEdit(self.widget)
            layout.addWidget(self.grad_from)
            layout.addWidget(QLabel('And:'))
            self.grad_to = QLineEdit(self.widget)
            layout.addWidget(self.grad_to)

        # Time to needs a Y point to reach
        if(text == 'time to'):
            layout.addWidget(QLabel('Time for:'))
            self.data = QComboBox(self.widget)
            if len(parent.parent.data.data_files) > 0:
                for sig in parent.parent.data.data_files[0].signals:
                    self.data.addItem(sig.name)
            layout.addWidget(self.data)
            layout.addWidget(QLabel('To reach:'))
            self.time_to = QLineEdit(self.widget)
            layout.addWidget(self.time_to)

        # Average of a condition needs condition and start and end time
        if(text == 'average of condition'):
            layout.addWidget(QLabel('Average of:'))
            self.condition = QComboBox(self.widget)
            if len(parent.parent.condition_data.data_files) > 0:
                for sig in parent.parent.condition_data.data_files[0].signals:
                    self.condition.addItem(sig.name)
            layout.addWidget(self.condition)
            layout.addWidget(QLabel('Between time:'))
            self.start_t = QLineEdit(self.widget)
            layout.addWidget(self.start_t)
            layout.addWidget(QLabel('And:'))
            self.end_t = QLineEdit(self.widget)
            layout.addWidget(self.end_t)

        # Condition at time needs condition and time
        if(text == 'condition at time'):
            layout.addWidget(QLabel('Value of:'))
            self.condition = QComboBox(self.widget)
            if len(parent.parent.condition_data.data_files) > 0:
                for sig in parent.parent.condition_data.data_files[0].signals:
                    self.condition.addItem(sig.name)
            layout.addWidget(self.condition)
            layout.addWidget(QLabel('At time:'))
            self.time = QLineEdit(self.widget)
            layout.addWidget(self.time)

        # Value of fit parameter needs fit and parameter
        if(text == 'fit parameter'):
            layout.addWidget(QLabel('Fit:'))
            self.fit = QComboBox(self.widget)
            self.fit.addItem('y = p0')
            self.fit.addItem('y = p1*x + p0')
            self.fit.addItem('y = p2*x^2 + p1*x + p0')
            self.fit.addItem('y = p0*exp(p1*x)')
            layout.addWidget(self.fit)
            layout.addWidget(QLabel('Of:'))
            self.data = QComboBox(self.widget)
            if len(parent.parent.data.data_files) > 0:
                for sig in parent.parent.data.data_files[0].signals:
                    self.data.addItem(sig.name)
            layout.addWidget(self.data)
            layout.addWidget(QLabel('Parameter:'))
            self.param = QComboBox(self.widget)
            self.param.addItem('p0')
            self.param.addItem('p1')
            self.param.addItem('p2')
            layout.addWidget(self.param)
            layout.addWidget(QLabel('From:'))
            self.fit_from = QLineEdit(self.widget)
            layout.addWidget(self.fit_from)
            layout.addWidget(QLabel('To:'))
            self.fit_to = QLineEdit(self.widget)
            layout.addWidget(self.fit_to)

        # Pad out the row
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget.setLayout(layout)
        self.item.setSizeHint(self.widget.sizeHint())
