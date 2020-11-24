from PyQt5.QtWidgets import QListWidgetItem, QHBoxLayout, QVBoxLayout, QLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QListWidget

from algaeplot.components.button import AddButton, DeleteButton
import algaeplot.configuration as config


class DataListItem():

    def __init__(self, text, index, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        del_button = DeleteButton()
        del_button.clicked.connect(parent.remove_item)
        add_button = AddButton()
        add_button.clicked.connect(parent.add_to_item)
        add_button.clicked.connect(parent.update_data_list)
        label = QLabel(text)

        hwidget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(del_button)
        layout.addWidget(add_button)
        layout.addWidget(label)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        hwidget.setLayout(layout)
        vlayout = QVBoxLayout()
        vlayout.addWidget(hwidget)
        if(len(parent.data.replicate_files[index]) > 1):
            for j in range(1, len(parent.data.replicate_files[index]), 1):
                hlayout = QHBoxLayout()
                hlayout.addWidget(QLabel('-'))
                sub_del_button = DeleteButton()
                hlayout.addWidget(sub_del_button)
                sub_del_button.clicked.connect(
                    lambda: parent.remove_replicate(j)
                )
                hlayout.addWidget(QLabel(
                    parent.data.replicate_files[index][j].name.split('/')[-1]
                ))
                hlayout.addStretch()
                hlayout.setSizeConstraint(QLayout.SetFixedSize)
                subwidget = QWidget()
                subwidget.setLayout(hlayout)
                vlayout.addWidget(subwidget)
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.addStretch()
        vlayout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget.setLayout(vlayout)
        self.item.setSizeHint(self.widget.sizeHint())

class ConditionListItem():

    def __init__(self, text, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        del_button = DeleteButton()
        del_button.clicked.connect(parent.remove_condition_item)
        label = QLabel(text)

        layout = QHBoxLayout()
        layout.addWidget(del_button)
        layout.addWidget(label)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget.setLayout(layout)
        self.item.setSizeHint(self.widget.sizeHint())
