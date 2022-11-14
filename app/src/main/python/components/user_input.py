import numpy as np

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSizePolicy,
                             QLineEdit, QGraphicsDropShadowEffect, QSpinBox, QComboBox, QCheckBox,
                             QRadioButton)

from components.label import LeftLabel
from type_functions import isfloat, isint
import configuration as config
import styles as styles


class UserInput(QWidget):
    def __init__(self, tooltip=None, shadow=False, *args, **kwargs):
        super(UserInput, self).__init__(*args, **kwargs)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        if shadow:
            shadow_effect = QGraphicsDropShadowEffect(
                blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.wr)
            self.setGraphicsEffect(shadow_effect)

        if tooltip is not None:
            self.setToolTip(tooltip)

class TextEntry(UserInput):
    def __init__(self, text, parent=None, default=None, placeholder=None, tooltip=None, *args, **kwargs):
        super(TextEntry, self).__init__(tooltip, shadow=True, *args, **kwargs)

        self.default = default
        self.name = text

        self.layout.addWidget(LeftLabel(text))
        self.entry = QLineEdit(parent)
        self.entry.setStyleSheet(styles.right_line_edit_style)
        if default is not None and default != -1:
            self.entry.setPlaceholderText(str(default))
        self.layout.addWidget(self.entry)

        if placeholder is not None:
            self.entry.setPlaceholderText(placeholder)

    def currentText(self, error=False):
        text = self.entry.currentText()
        if error and (text == '' or text is None):
            raise RuntimeError(self.name + 'could not be interpreted as a string')
        return self.entry.currentText()

    def text(self, error=False):
        text = self.entry.text()
        if error and (text == '' or text is None):
            raise RuntimeError(self.name + 'could not be interpreted as a string')
        return text

    def setPlaceholderText(self, text):
        return self.entry.setPlaceholderText(text)

    def get_float(self, error=False):
        if isfloat(self.entry.text()):
            return float(self.entry.text())
        if error:
            raise RuntimeError(self.name + ' could not be interpreted as a number')
        return self.default

    def get_int(self, error=False):
        if isint(self.entry.text()):
            return int(self.entry.text())
        if error:
            raise RuntimeError(self.name + ' could not be interpreted as a number')
        return self.default


class ParameterBounds(UserInput):
    def __init__(self, text, parent=None, *args, **kwargs):
        super(ParameterBounds, self).__init__(tooltip=None, shadow=True, *args, **kwargs)

        self.layout.addWidget(LeftLabel(text))

        self.start = QLineEdit(parent)
        self.start.setPlaceholderText('Start')
        self.start.setStyleSheet(styles.mid_line_edit_style)
        self.layout.addWidget(self.start)

        self.min = QLineEdit(parent)
        self.min.setPlaceholderText('Min')
        self.min.setStyleSheet(styles.mid_line_edit_style)
        self.layout.addWidget(self.min)

        self.max = QLineEdit(parent)
        self.max.setPlaceholderText('Max')
        self.max.setStyleSheet(styles.right_line_edit_style)
        self.layout.addWidget(self.max)

    def get_start(self, error=False):
        start_str = self.start.text()
        if isfloat(start_str):
            return float(start_str)
        if error:
            raise RuntimeError('Start not a number')
        return 1

    def get_min(self, error=False):
        min_str = self.min.text()
        if isfloat(min_str):
            return float(min_str)
        if error:
            raise RuntimeError('Minimum bound not a number')
        return -np.inf

    def get_max(self, error=False):
        max_str = self.max.text()
        if isfloat(max_str):
            return float(max_str)
        if error:
            raise RuntimeError('Maximum bound not a number')
        return np.inf


class SpinBox(UserInput):
    def __init__(self, text, start, min_val, max_val, parent=None, *args, **kwargs):
        super(SpinBox, self).__init__(tooltip=None, shadow=True, *args, **kwargs)

        self.start = start
        self.layout.addWidget(LeftLabel(text))

        self.entry = QSpinBox(parent)
        self.entry.setMinimum(min_val)
        self.entry.setMaximum(max_val)
        self.entry.setValue(start)
        self.entry.setSingleStep(1)
        self.entry.setStyleSheet(styles.spinbox_style)
        self.layout.addWidget(self.entry)

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


class DropDown(UserInput):
    def __init__(self, text, options, parent=None, change_action=None, tooltip=None, edit=False, index=None, *args, **kwargs):
        super(DropDown, self).__init__(tooltip, shadow=True, *args, **kwargs)

        self.name = text
        self.layout.addWidget(LeftLabel(text))

        self.entry = QComboBox(parent)
        self.entry.addItems(options)
        self.entry.setStyleSheet(styles.dropdown_style)
        self.entry.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.layout.addWidget(self.entry)

        if change_action is not None:
            self.entry.currentTextChanged.connect(change_action)

        if edit:
            self.entry.setEditable(True)
            self.entry.setInsertPolicy(2)
        
        if index is not None:
            self.setCurrentIndex(index)

    def currentText(self, error=False):
        text = self.entry.currentText()
        if error and (text == '' or text is None):
            raise RuntimeError(self.name + 'could not be interpreted as a string')
        return text

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
    
    def connect(self, func):
        return self.entry.currentTextChanged.connect(func)

    def setCurrentIndex(self, index):
        return self.entry.setCurrentIndex(index)

    def get_list(self):
        output_list = []
        for i in range(self.entry.count()):
            output_list.append(self.entry.itemText(i))
        return output_list


class CheckBox(UserInput):
    def __init__(self, text, parent=None, tooltip=None, change_action=None, checked=False, style=None, *args, **kwargs):
        super(CheckBox, self).__init__(tooltip, shadow=True, *args, **kwargs)

        self.entry = QCheckBox(parent)
        self.entry.setText(text)
        self.entry.setStyleSheet(styles.round_label_style)
        self.layout.addWidget(self.entry)

        if change_action is not None:
            self.entry.stateChanged.connect(change_action)

        self.entry.setChecked(checked)

        if style is not None:
            self.entry.setStyleSheet(style)

    def isChecked(self):
        return self.entry.isChecked()


class RadioButton(UserInput):
    def __init__(self, text1, text2, parent=None, tooltip=None, *args, **kwargs):
        super(RadioButton, self).__init__(tooltip, shadow=False, *args, **kwargs)

        self.button1 = QRadioButton(text1, parent)
        self.button1.setStyleSheet(styles.left_label_style)
        self.button1.setChecked(True)
        self.layout.addWidget(self.button1)

        self.button2 = QRadioButton(text2, parent)
        self.button2.setStyleSheet(styles.right_label_style)
        self.layout.addWidget(self.button2)

    def isChecked(self):
        if self.button1.isChecked():
            return False
        else:
            return True

