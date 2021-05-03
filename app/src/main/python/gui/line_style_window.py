from matplotlib.colors import is_color_like

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtWidgets import QLineEdit, QPushButton, QComboBox

from components.button import Button
from components.user_input import DropDown, TextEntry
import configuration as config
from logger import logger


class LineStyleWindow(QMainWindow):

    def __init__(self, artist, line_i, parent=None):
        super(LineStyleWindow, self).__init__(parent)
        self.title = 'Line Style'
        self.width = 150*config.wr
        self.height = 100*config.hr
        logger.debug('Creating line style window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        self.artist = artist
        self.line_i = line_i
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QVBoxLayout()
        layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        layout.setSpacing(5*config.wr)

        self.line_style = DropDown('Line style:', config.line_style_options, self)
        layout.addWidget(self.line_style)

        self.line_colour = TextEntry('Line colour:', self)
        layout.addWidget(self.line_colour)

        self.marker_style = DropDown('Marker style:', config.marker_style_options, self)
        layout.addWidget(self.marker_style)

        apply_button = Button("Apply", self)
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def apply_changes(self):
        logger.debug('Trying to set colour %s and style %s' %
                     (self.line_colour.text(), self.line_style.currentText()))
        try:
            if(is_color_like(self.line_colour.text())):
                for i in range(len(self.artist)):
                    self.artist[i].set_color(self.line_colour.text())
            self.artist[0].set_linestyle(self.line_style.currentText())
            self.artist[0].set_marker(self.marker_style.currentText())
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
                [self.artist[0].get_color(), self.artist[0].get_linestyle(), self.artist[0].get_marker()]
            ])
            self.close()
        except Exception as e:
            logger.exception(e)
            logger.warning('Unable change style, skipping')
            pass
