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
            layout.addWidget(QLabel('between:'))
            self.grad_from = QLineEdit(self.widget)
            layout.addWidget(self.grad_from)
            layout.addWidget(QLabel('and:'))
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
            layout.addWidget(QLabel('to reach:'))
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
            layout.addWidget(QLabel('between time:'))
            self.start_t = QLineEdit(self.widget)
            layout.addWidget(self.start_t)
            layout.addWidget(QLabel('and:'))
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
            layout.addWidget(QLabel('at time:'))
            self.time = QLineEdit(self.widget)
            layout.addWidget(self.time)

        # Pad out the row
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget.setLayout(layout)
        self.item.setSizeHint(self.widget.sizeHint())
