# Standard imports
import random
import numpy as np
from scipy.optimize import curve_fit

# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.style

# Local imports
from ada.data.processor import (process_data, average_data,
                                   time_average, exponent_text)
from ada.data.models import get_model
from ada.gui.file_handler import save_file

import ada.configuration as config
from ada.logger import logger


class CorrelationCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = self.fig.add_subplot(111)

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        self.parent = parent

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        self.plot()

    def plot(self, xdata=[], ydata=[], x_error=None, y_error=None, title='', x_title='', y_title=''):
        logger.debug('Creating correlation plot')

        self.axes.clear()
        self.axes.errorbar(xdata, ydata, y_error, x_error, '.')
        self.axes.set_title(title)
        self.axes.set_xlabel(x_title)
        self.axes.set_ylabel(y_title)
        self.draw()
        return

    # Function to save figure through file handler gui
    def save(self):
        save_file(self.fig)