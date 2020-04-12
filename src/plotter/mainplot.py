# Local imports
from reader.dataholder import DataHolder
from gui.configuration import Configuration
from plotter.cursor import Cursor, SnapToCursor

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
import matplotlib.style
import matplotlib as mpl

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
        self.condition_axes = self.axes.twinx()
        self.condition_axes.set_axis_off()
        self.axes.set_zorder(self.condition_axes.get_zorder()+1) 
        self.axes.patch.set_visible(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        empty_data = DataHolder()
        empty_condition = DataHolder()
        empty_config = Configuration()
        self.plot(empty_data, empty_condition, empty_config)

    def plot(self, data, condition_data, config):

        # Style configuration
        if(config.style != ''):
            if(config.style == 'default'):
                mpl.style.use('default')
            if(config.style == 'greyscale'):
                mpl.style.use('grayscale')
            if(config.style == 'colour blind'):
                mpl.style.use('seaborn-colorblind')
            if(config.style == 'pastel'):
                mpl.style.use('seaborn-pastel')
            if(config.style == 'deep'):
                mpl.style.use('seaborn-colorblind')
        if(config.font_style != ''):
            mpl.rcParams['font.family'] = config.font_style
        if(config.font_size >= 0):
            mpl.rcParams['font.size'] = config.font_size
        if(config.line_width >= 0):
            mpl.rcParams['lines.linewidth'] = config.line_width

        # Clear axes and set default visibility
        self.axes.clear()
        self.condition_axes.clear()
        self.condition_axes.set_axis_off()
        self.axes.patch.set_visible(False)
        self.axes.spines['right'].set_visible(True)

        # More style settings
        if(config.font_style != ''):
            self.axes.xaxis.label.set_family(config.font_style)
            self.axes.yaxis.label.set_family(config.font_style)
            self.condition_axes.yaxis.label.set_family(config.font_style)
        if(config.font_size >= 0):
            self.axes.xaxis.label.set_size(config.font_size)
            self.axes.yaxis.label.set_size(config.font_size)
            self.condition_axes.yaxis.label.set_size(config.font_size)

        if(data.empty):
            self.axes.set_title('Empty plot')
            self.draw()
            return
         
        x_title = ''
        y_title = ''
        xdata_list = []
        ydata_list = []
        for i, data in enumerate(data.data_files):
            # Convert the units of time if needed
            xdata, x_title = self.convert_xdata(data.xaxis, config)

            # Align at time 0 if option selected
            if config.align:
                xdata - xdata[0]

            # Get the y axis data for plotting
            ydata = data.signals[0].data
            for sig in data.signals:
                found_ydata = False
                if sig.name == config.yvar:
                    found_ydata = True
                    ydata = sig.data
                    y_title = sig.title()
                    if(config.yname != ''):
                        y_title = y_title.replace(sig.name, config.yname)
                    if(config.yunit != ''):
                        y_title = y_title.replace("["+sig.unit+"]", "["+config.yunit+"]")
                if not found_ydata:
                    raise RuntimeError('Could not find signal %s in %s' % (config.yvar, data.name)) 

            # Plot the data
            if(config.smooth):
                ydata = savitzky_golay(ydata, 61, 0)
            self.axes.plot(xdata, ydata, '-', label=config.label_names[i])

            xdata_list.append(xdata)
            ydata_list.append(ydata)
 
        # Switch legend on/off
        if(config.legend):
            self.axes.legend()

        # Switch grid on/off
        self.axes.grid(config.grid)

        # Configure axis labels
        self.axes.set_title('')
        if( config.title != ''):
            self.axes.set_title(config.title)
        self.axes.set_xlabel(x_title)
        self.axes.set_ylabel(y_title)

        # Set the axis range
        xmin = self.axes.get_xbound()[0]
        if(config.xmin != -1):
            xmin = config.xmin
        xmax = self.axes.get_xbound()[1]
        if(config.xmax != -1):
            xmax = config.xmax
        ymin = self.axes.get_ybound()[0]
        if(config.ymin != -1):
            ymin = config.ymin
        ymax = self.axes.get_ybound()[1]
        if(config.ymax != -1):
            ymax = config.ymax
        self.axes.set_xlim([xmin, xmax])
        self.axes.set_ylim([ymin, ymax])

        # Configure the measurement cursor
        if(config.cursor):
            self.cursor = SnapToCursor(self.axes, xdata_list, ydata_list, useblit=False, color='red', linewidth=1)

            def onclick(event):
                self.cursor.onmove(event)
            self.mpl_connect('button_press_event', onclick)

        # Plot the condition data on a separate axis if it exists
        if not condition_data.empty:
            self.condition_axes.set_axis_on()
            self.condition_axes.spines['right'].set_color('red')
            self.axes.spines['right'].set_visible(False)
            self.condition_axes.tick_params(axis='y', colors='red')
            self.condition_axes.yaxis.label.set_color('red')
            cdata = condition_data.data_files[0]
            condition_xdata, condition_x_title = self.convert_xdata(cdata.xaxis, config)
            condition_ydata = cdata.signals[0].data
            for sig in cdata.signals:
                if sig.name == config.condition_yvar:
                    condition_ydata = sig.data
                    condition_y_title = sig.title()
                    if(config.condition_yname != ''):
                        condition_y_title = condition_y_title.replace(sig.name, config.condition_yname)
                    if(config.condition_yunit != ''):
                        condition_y_title = condition_y_title.replace("["+sig.unit+"]", "["+config.yunit+"]")
            self.condition_axes.set_ylabel(condition_y_title)
            self.condition_axes.plot(condition_xdata, condition_ydata, 'r-', label=config.condition_label_names[0])

            # Configure the axis range
            condition_ymin = self.condition_axes.get_ybound()[0]
            if(config.condition_ymin != -1):
                condition_ymin = config.condition_ymin
            condition_ymax = self.condition_axes.get_ybound()[1]
            if(config.condition_ymax != -1):
                condition_ymax = config.condition_ymax
            self.condition_axes.set_ylim([condition_ymin, condition_ymax])


        # Show the plot
        self.draw()

    def convert_xdata(self, xaxisdata, config):
        xdata = xaxisdata.data
        x_title = xaxisdata.title()
        if(config.xname != ''):
            x_title = x_title.replace(xaxisdata.name, config.xname)
        x_unit = xaxisdata.unit
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
        x_title = x_title.replace("["+xaxisdata.unit+"]", "["+x_unit+"]")
        return xdata, x_title

    def save(self, config):
        if(config.file_name == ''):
            self.fig.savefig('graph.png')
        elif(config.file_name.find('.') == -1):
            self.fig.savefig(config.file_name + '.png')
        else:
            self.fig.savefig(config.file_name)

