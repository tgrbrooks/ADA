from PyQt5.QtWidgets import QListWidgetItem, QHBoxLayout, QVBoxLayout, QLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QListWidget

from data.data_manager import data_manager
from components.button import AddButton, DeleteButton
from components.spacer import Spacer
import configuration as config
import styles as styles


class DataListItem():

    def __init__(self, text, index, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        del_button = DeleteButton()
        del_button.clicked.connect(parent.remove_item)
        add_button = AddButton()
        add_button.clicked.connect(parent.add_to_item)
        label = QLabel(text)
        label.setStyleSheet(styles.default_font_bold)

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
        for j in range(1, data_manager.num_replicates(index), 1):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel('-'))
            sub_del_button = DeleteButton()
            hlayout.addWidget(sub_del_button)
            sub_del_button.clicked.connect(
                lambda: parent.remove_replicate(j)
            )
            inner_label = QLabel(
                data_manager.growth_data.replicate_files[index][j].label
            )
            inner_label.setStyleSheet(styles.small_font)
            hlayout.addWidget(inner_label)
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

    def __init__(self, text, index, parent=None):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        del_button = DeleteButton()
        del_button.clicked.connect(parent.remove_condition_item)
        label = QLabel(text)
        label.setStyleSheet(styles.default_font_bold)

        hwidget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(del_button)
        layout.addWidget(label)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        hwidget.setLayout(layout)
        vlayout = QVBoxLayout()
        vlayout.addWidget(hwidget)
        for j in range(1, data_manager.num_condition_replicates(index), 1):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel('-'))
            sub_del_button = DeleteButton()
            hlayout.addWidget(sub_del_button)
            sub_del_button.clicked.connect(
                lambda: parent.remove_condition_replicate(j)
            )
            inner_label = QLabel(
                data_manager.condition_data.replicate_files[index][j].label
            )
            inner_label.setStyleSheet(styles.small_font)
            hlayout.addWidget(inner_label)
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


class DelListItem():

    def __init__(self, text):
        self.item = QListWidgetItem()
        self.widget = QWidget()
        self.button = DeleteButton()
        label = QLabel(text)
        label.setStyleSheet(styles.default_font)

        layout = QHBoxLayout()
        spacer = Spacer()
        spacer.setFixedWidth(5*config.wr)
        layout.addWidget(spacer)
        layout.addWidget(self.button)
        layout.addWidget(label)
        layout.addStretch()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 10, 5, 5)

        self.widget.setLayout(layout)
        self.item.setSizeHint(self.widget.sizeHint())
