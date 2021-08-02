from matplotlib.colors import is_color_like

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from ada.components.button import Button
from ada.components.user_input import DropDown, TextEntry
import ada.configuration as config
from ada.logger import logger


class LineStyleWindow(QMainWindow):

    def __init__(self, plot_data, parent=None):
        super(LineStyleWindow, self).__init__(parent)
        self.title = 'Line Style'
        self.width = 150*config.wr
        self.height = 100*config.hr
        logger.debug('Creating line style window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        self.data = plot_data
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

        self.marker_style = DropDown('Marker style:', list(config.marker_style_options.keys()), self)
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
