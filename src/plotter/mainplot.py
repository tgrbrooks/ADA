# Local imports
from reader.dataholder import DataHolder
from gui.configuration import Configuration

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
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        empty_data = DataHolder()
        empty_config = Configuration()
        self.plot(empty_data, empty_config)

    def plot(self, data, config):
        self.axes.cla()
        if(data.empty):
            self.axes.set_title('Empty plot')
            self.draw()
        else:
            x_title = ''
            y_title = ''
            for data in data.data_files:
                # Convert the units of time if needed
                xdata = data.xaxis.data
                x_title = data.xaxis.title()
                if(config.xname != ''):
                    x_title = x_title.replace(data.xaxis.name, config.xname)
                x_unit = data.xaxis.unit
                if(config.xvar == 'minutes'):
                    xdata = xdata / 60.
                    x_unit = 'min'
                if(config.xvar == 'hours'):
                    xdata = xdata / (60.*60.)
                    x_unit = 'hr'
                if(config.xvar == 'days'):
                    xdata = xdata / (60.*60.*24.)
                    x_unit = 'day'
                if(config.xunit != ''):
                    x_unit = config.xunit
                x_title = x_title.replace("["+data.xaxis.unit+"]", "["+x_unit+"]")

                # Get the y axis data for plotting
                ydata = data.signals[0].data
                for sig in data.signals:
                    if sig.name == config.yvar:
                        ydata = sig.data
                        y_title = sig.title()
                        if(config.yname != ''):
                            y_title = y_title.replace(sig.name, config.yname)
                        if(config.yunit != ''):
                            y_title = y_title.replace("["+sig.unit+"]", "["+config.yunit+"]")

                # Plot the data
                self.axes.plot(xdata, ydata, 'r-')
 
            # Configure axis labels
            self.axes.set_title('')
            if( config.title != ''):
                self.axes.set_title(config.title)
            self.axes.set_xlabel(x_title)
            self.axes.set_ylabel(y_title)
            self.draw()

    def save(self):
       self.fig.savefig('graph.png')

