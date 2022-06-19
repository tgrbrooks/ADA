from PyQt5.QtWidgets import (QListWidgetItem, QHBoxLayout, QVBoxLayout, QLayout,
                             QLabel, QCheckBox)

from ada.data.data_manager import data_manager
from ada.components.button import AddButton, DeleteButton
from ada.components.spacer import Spacer
from ada.components.layout_widget import LayoutWidget
from ada.components.label import Label
from ada.configuration import config
import ada.styles as styles


class DataListItem():

    def __init__(self, text, index, parent=None):
        self.item = QListWidgetItem()
        list_item = LayoutWidget(QVBoxLayout, margin=0, spacing=0)

        data = LayoutWidget(QHBoxLayout)
        show_box = QCheckBox()
        show_box.setChecked(data_manager.get_growth_file(index).visible)
        show_box.clicked.connect(parent.set_visibility)
        data_label = Label(text, shadow=False, style=styles.default_font_bold)
        data.addWidgets([
            DeleteButton(clicked=parent.remove_item),
            AddButton(clicked=parent.add_to_item),
            show_box,
            data_label.text])
        data.layout.addStretch()
        data.layout.setSizeConstraint(QLayout.SetFixedSize)
        list_item.addWidget(data.widget)

        for j in range(1, data_manager.num_replicates(index), 1):
            replicate = LayoutWidget(QHBoxLayout)
            replicate_label = Label(data_manager.get_replicates(index)[j].label, shadow=False, style=styles.small_font)
            replicate.addWidgets([
                QLabel('-'),
                DeleteButton(clicked=(lambda: parent.remove_replicate(j))),
                replicate_label.text])
            replicate.layout.addStretch()
            replicate.layout.setSizeConstraint(QLayout.SetFixedSize)
            list_item.addWidget(replicate.widget)

        list_item.layout.addStretch()
        list_item.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget = list_item.widget
        self.item.setSizeHint(self.widget.sizeHint())


class ConditionListItem():

    def __init__(self, text, index, parent=None):
        self.item = QListWidgetItem()
        list_item = LayoutWidget(QVBoxLayout, margin=0, spacing=0)

        data = LayoutWidget(QHBoxLayout)
        show_box = QCheckBox()
        show_box.setChecked(data_manager.get_condition_file(index).visible)
        show_box.clicked.connect(parent.set_condition_visibility)
        data_label = Label(text, shadow=False, style=styles.default_font_bold)

        data.addWidgets([
            DeleteButton(clicked=parent.remove_condition_item),
            show_box,
            data_label.text])
        data.layout.addStretch()
        data.layout.setSizeConstraint(QLayout.SetFixedSize)
        list_item.addWidget(data.widget)

        for j in range(1, data_manager.num_condition_replicates(index), 1):
            replicate = LayoutWidget(QHBoxLayout)
            replicate_label = Label(data_manager.condition_data.replicate_files[index][j].label, shadow=False, style=styles.small_font)
            replicate.addWidgets([
                QLabel('-'),
                DeleteButton(clicked=(lambda: parent.remove_condition_replicate(j))),
                replicate_label.text])
            replicate.layout.addStretch()
            replicate.layout.setSizeConstraint(QLayout.SetFixedSize)
            list_item.addWidget(replicate)

        list_item.layout.addStretch()
        list_item.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.widget = list_item.widget
        self.item.setSizeHint(self.widget.sizeHint())


class DelListItem():

    def __init__(self, text):
        self.item = QListWidgetItem()

        item = LayoutWidget(QHBoxLayout)
        label = Label(text, style=styles.default_font_bold)
        _, self.button, _ = item.addWidgets([
            Spacer(width=5*config['width_ratio']),
            DeleteButton(),
            label.text])

        item.layout.addStretch()
        item.layout.setSizeConstraint(QLayout.SetFixedSize)
        item.layout.setSpacing(5)
        item.layout.setContentsMargins(5, 10, 5, 5)

        self.widget = item.widget
        self.item.setSizeHint(self.widget.sizeHint())
