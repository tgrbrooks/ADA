# Local imports
from reader.dataholder import DataHolder
from gui.configuration import Configuration

# Standard imports
import random
from math import factorial
import numpy as np

# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

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
                if(config.smooth):
                    ydata = savitzky_golay(ydata, 61, 0)
                self.axes.plot(xdata, ydata, '-', label=data.label)
 
            if(config.legend):
                self.axes.legend()

            # Configure axis labels
            self.axes.set_title('')
            if( config.title != ''):
                self.axes.set_title(config.title)
            self.axes.set_xlabel(x_title)
            self.axes.set_ylabel(y_title)
            self.draw()


    def save(self):
       self.fig.savefig('graph.png')

