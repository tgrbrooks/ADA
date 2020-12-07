from matplotlib.colors import is_color_like

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtWidgets import QLineEdit, QPushButton, QComboBox

from ada.components.button import Button
from ada.components.user_input import DropDown, TextEntry
import ada.configuration as config


class LineStyleWindow(QMainWindow):

    def __init__(self, artist, line_i, parent=None):
        super(LineStyleWindow, self).__init__(parent)
        self.title = 'Line Style'
        self.width = 150
        self.height = 100
        self.artist = artist
        self.line_i = line_i
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.line_style = DropDown('Line style:', [], self)
        self.line_style.addItem('solid')
        self.line_style.addItem('dashed')
        self.line_style.addItem('dashdot')
        self.line_style.addItem('dotted')
        layout.addWidget(self.line_style)

        self.line_colour = TextEntry('Line colour:', self)
        layout.addWidget(self.line_colour)

        apply_button = Button("Apply", self)
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def apply_changes(self):
        try:
            if(is_color_like(self.line_colour.text())):
                self.artist[0].set_color(self.line_colour.text())
                if(len(self.artist) > 1):
                    self.artist[1].set_color(self.line_colour.text())
            self.artist[0].set_linestyle(self.line_style.currentText())
            if(self.parent.legend_on):
                self.parent.axes.legend(
                    title=self.parent.legend_title,
                    loc='upper left'
                )
            if(self.parent.condition_legend_on):
                self.parent.condition_axes.legend(
                    title=self.parent.condition_legend_title,
                    loc='lower right'
                )
            self.parent.draw()
            self.parent.plot_config.append([
                self.line_i,
                [self.artist[0].get_color(), self.artist[0].get_linestyle()]
            ])
            self.close()
        except Exception:
            pass
