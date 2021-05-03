import numpy as np

from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QSizePolicy,
                             QLineEdit, QGraphicsDropShadowEffect, QSpinBox, QComboBox, QCheckBox,
                             QRadioButton)

from ada.components.label import LeftLabel
from ada.type_functions import isfloat, isint
import ada.configuration as config
import ada.styles as styles


class TextEntry(QWidget):
    def __init__(self, text, parent=None, default=None, *args, **kwargs):
        super(TextEntry, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.default = default

        text = LeftLabel(text, True)
        layout.addWidget(text)

        self.entry = QLineEdit(parent)
        self.entry.setStyleSheet(styles.right_line_edit_style)
        if default is not None and default != -1:
            self.entry.setPlaceholderText(str(default))
        layout.addWidget(self.entry)

        self.setLayout(layout)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.wr)
        self.setGraphicsEffect(shadow)

    def currentText(self):
        return self.entry.currentText()

    def text(self):
        return self.entry.text()

    def setPlaceholderText(self, text):
        return self.entry.setPlaceholderText(text)

    def get_float(self):
        if isfloat(self.entry.text()):
            return float(self.entry.text())
        return self.default

    def get_int(self):
        if isint(self.entry.text()):
            return int(self.entry.text())
        return self.default


class ParameterBounds(QWidget):
    def __init__(self, text, parent=None, *args, **kwargs):
        super(ParameterBounds, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        text = LeftLabel(text, True)
        layout.addWidget(text)

        self.start = QLineEdit(parent)
        self.start.setPlaceholderText('Start')
        self.start.setStyleSheet(styles.mid_line_edit_style)
        layout.addWidget(self.start)

        self.min = QLineEdit(parent)
        self.min.setPlaceholderText('Min')
        self.min.setStyleSheet(styles.mid_line_edit_style)
        layout.addWidget(self.min)

        self.max = QLineEdit(parent)
        self.max.setPlaceholderText('Max')
        self.max.setStyleSheet(styles.right_line_edit_style)
        layout.addWidget(self.max)

        self.setLayout(layout)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.wr)
        self.setGraphicsEffect(shadow)

    def get_start(self):
        start_str = self.start.text()
        if isfloat(start_str):
            return float(start_str)
        return 1

    def get_min(self):
        min_str = self.min.text()
        if isfloat(min_str):
            return float(min_str)
        return -np.inf

    def get_max(self):
        max_str = self.max.text()
        if isfloat(max_str):
            return float(max_str)
        return np.inf


class SpinBox(QWidget):
    def __init__(self, text, start, min_val, max_val, parent=None, *args, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.start = start

        text = LeftLabel(text, True)
        layout.addWidget(text)

        self.entry = QSpinBox(parent)
        self.entry.setMinimum(min_val)
        self.entry.setMaximum(max_val)
        self.entry.setValue(start)
        self.entry.setSingleStep(1)
        self.entry.setStyleSheet(styles.spinbox_style)
        layout.addWidget(self.entry)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)

    def currentText(self):
        return str(self.entry.value())

    def text(self):
        return self.entry.text()

    def get_float(self):
        if isfloat(self.entry.text()):
            return float(self.entry.text())
        return self.start

    def get_int(self):
        if isint(self.entry.text()):
            return int(self.entry.text())
        return self.start


class DropDown(QWidget):
    def __init__(self, text, options, parent=None, *args, **kwargs):
        super(DropDown, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        text = LeftLabel(text, True)
        layout.addWidget(text)

        self.entry = QComboBox(parent)
        self.entry.addItems(options)
        self.entry.setStyleSheet(styles.dropdown_style)
        self.entry.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        layout.addWidget(self.entry)

        self.setLayout(layout)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)

    def currentText(self):
        return self.entry.currentText()

    def currentTextChanged(self, value):
        return self.entry.currentTextChanged(value)

    def clear(self):
        return self.entry.clear()

    def addItem(self, item):
        return self.entry.addItem(item)

    def addItems(self, items):
        return self.entry.addItems(items)

    def itemText(self, index):
        return self.entry.itemText(index)

    def count(self):
        return self.entry.count()

    def setCurrentIndex(self, index):
        return self.entry.setCurrentIndex(index)

    def get_list(self):
        output_list = []
        for i in range(self.entry.count()):
            output_list.append(self.entry.itemText(i))
        return output_list


class CheckBox(QWidget):
    def __init__(self, text, parent=None, *args, **kwargs):
        super(CheckBox, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.entry = QCheckBox(parent)
        self.entry.setText(text)
        self.entry.setStyleSheet(styles.round_label_style)
        layout.addWidget(self.entry)

        self.setLayout(layout)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)

    def isChecked(self):
        return self.entry.isChecked()


class RadioButton(QWidget):
    def __init__(self, text1, text2, parent=None, *args, **kwargs):
        super(RadioButton, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.button1 = QRadioButton(text1, parent)
        self.button1.setStyleSheet(styles.left_label_style)
        self.button1.setChecked(True)
        layout.addWidget(self.button1)

        self.button2 = QRadioButton(text2, parent)
        self.button2.setStyleSheet(styles.right_label_style)
        layout.addWidget(self.button2)

        self.setLayout(layout)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.hr)
        self.setGraphicsEffect(shadow)

    def isChecked(self):
        if self.button1.isChecked():
            return False
        else:
            return True

