from matplotlib.colors import is_color_like

from PyQt5.QtWidgets import QVBoxLayout

from ada.components.button import Button
from ada.components.user_input import DropDown, TextEntry
from ada.components.window import Window
import ada.configuration as config
from ada.logger import logger


class LineStyleWindow(Window):

    def __init__(self, plot_data, parent=None):
        super(LineStyleWindow, self).__init__('Line Style', 150, 100, QVBoxLayout, parent)
        self.data = plot_data
        self.initUI()

    def initUI(self):
        self.line_style = DropDown('Line style:', config.line_style_options, self)
        self.window.addWidget(self.line_style)

        self.line_colour = TextEntry('Line colour:', self)
        self.window.addWidget(self.line_colour)

        self.marker_style = DropDown('Marker style:', list(config.marker_style_options.keys()), self)
        self.window.addWidget(self.marker_style)

        apply_button = Button("Apply", self)
        apply_button.clicked.connect(self.apply_changes)
        self.window.addWidget(apply_button)

    def apply_changes(self):
        logger.debug('Trying to set colour %s and style %s' %
                     (self.line_colour.text(), self.line_style.currentText()))
        try:
            if(is_color_like(self.line_colour.text())):
                self.data.style["color"] = self.line_colour.text()
            self.data.style["linestyle"] = self.line_style.currentText()
            self.data.style["marker"] = config.marker_style_options[self.marker_style.currentText()]
            self.parent.set_plot_styles()
            self.parent.draw()
            self.close()
        except Exception as e:
            logger.exception(e)
            logger.warning('Unable change style, skipping')
            pass
