# Local imports
from reader.dataholder import DataHolder

# Standard imports
import random

# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        empty_data = DataHolder()
        self.plot(empty_data)

    def plot(self, data):
        if(data.empty):
            self.axes.set_title('Empty plot')
            self.draw()
        else:
            algem_data = data.data_files[0] 
            xdata = algem_data.xaxis.data
            ydata = algem_data.signals[5].data
            self.axes.plot(xdata, ydata, 'r-')
            self.axes.set_title('Filled plot')
            self.draw()

