from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QSizePolicy,
                             QLineEdit, QGraphicsDropShadowEffect, QSpinBox, QComboBox, QCheckBox)

from ada.components.label import LeftLabel
import ada.configuration as config
import ada.styles as styles


class TextEntry(QWidget):
    def __init__(self, text, parent=None, *args, **kwargs):
        super(TextEntry, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        text = LeftLabel(text, True)
        layout.addWidget(text)

        self.entry = QLineEdit(parent)
        self.entry.setStyleSheet(styles.right_line_edit_style)
        layout.addWidget(self.entry)

        self.setLayout(layout)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=2*config.wr, xOffset=1*config.wr, yOffset=1*config.wr)
        self.setGraphicsEffect(shadow)

    def currentText(self):
        return self.entry.currentText()

    def text(self):
        return self.entry.text()


class SpinBox(QWidget):
    def __init__(self, text, start, min_val, max_val, parent=None, *args, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        text = LeftLabel(text, True)
        layout.addWidget(text)

        self.entry = QSpinBox(parent)
        self.entry.setValue(start)
        self.entry.setMinimum(min_val)
        self.entry.setMaximum(max_val)
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
