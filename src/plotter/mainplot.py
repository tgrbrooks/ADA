# Local imports
from reader.dataholder import DataHolder
from gui.configuration import Configuration
from plotter.cursor import Cursor, SnapToCursor
from gui.linestylewindow import LineStyleWindow
from gui.filehandler import save_file

# Standard imports
import random
from math import factorial
import numpy as np

# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import is_color_like
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

        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        self.condition_axes = self.axes.twinx()
        self.condition_axes.set_axis_off()
        self.axes.set_zorder(self.condition_axes.get_zorder()+1) 
        self.axes.patch.set_visible(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.legend_on = False
        self.condition_legend_on = False
        self.plot_config = []

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
        plot_list = []

        # More style settings
        if(config.font_style != ''):
            self.axes.xaxis.label.set_family(config.font_style)
            self.axes.yaxis.label.set_family(config.font_style)
            self.condition_axes.yaxis.label.set_family(config.font_style)
        if(config.font_size >= 0):
            self.axes.xaxis.label.set_size(config.font_size)
            self.axes.yaxis.label.set_size(config.font_size)
            self.condition_axes.yaxis.label.set_size(config.font_size)

        if(data.empty and condition_data.empty):
            self.axes.set_title('Empty plot')
            self.draw()
            return
         
        x_title = ''
        y_title = ''
        xdata_list = []
        ydata_list = []
        for i, dat in enumerate(data.data_files):
            # Convert the units of time if needed
            xdata, x_title = self.convert_xdata(dat.xaxis, config)
            # Get the y axis data for plotting
            ydata, y_title = self.get_ydata(dat.signals, config)

            # Apply alignment, outlier removal, and smoothing
            xdata, ydata = self.process_data(xdata, ydata, config)

            # If there are replicate files then average the data
            if(len(data.replicate_files[i]) > 1):
                xdatas = [xdata]
                ydatas = [ydata]
                for j in range(1, len(data.replicate_files[i]), 1):
                    rep_xdata, rep_xtitle = self.convert_xdata(data.replicate_files[i][j].xaxis, config)
                    rep_ydata, rep_ytitle = self.get_ydata(data.replicate_files[i][j].signals, config)
                    rep_xdata, rep_ydata = self.process_data(rep_xdata, rep_ydata, config)
                    xdatas.append(rep_xdata)
                    ydatas.append(rep_ydata)
                xdata, ydata, yerr = self.average_data(xdatas, ydatas)
                growth_plot = self.axes.plot(xdata, ydata, '-', label=config.label_names[i])
                self.axes.fill_between(xdata, ydata-yerr, ydata+yerr, alpha=0.4)
                plot_list.append(growth_plot[0])
            else:
                growth_plot = self.axes.plot(xdata, ydata, '-', label=config.label_names[i])
                plot_list.append(growth_plot[0])

            xdata_list.append(xdata)
            ydata_list.append(ydata) 

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

        # Plot the condition data on a separate axis if it exists
        colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
        if not condition_data.empty:
            self.condition_axes.set_axis_on()
            # Configure axis colour and visibility
            caxis_colour = 'red'
            if(is_color_like(config.axis_colour)):
                caxis_colour = config.axis_colour
            self.condition_axes.spines['right'].set_color(caxis_colour)
            self.axes.spines['right'].set_visible(False)
            self.condition_axes.tick_params(axis='y', colors=caxis_colour)
            self.condition_axes.yaxis.label.set_color(caxis_colour)

            # Loop over the condition data files
            for i, cdata in enumerate(condition_data.data_files):
                # Get the x data in the right time units
                condition_xdata, condition_x_title = self.convert_xdata(cdata.xaxis, config)

                # Get the desired condition data and configure title
                condition_ydata, condition_y_title = self.get_ydata(cdata.signals, config, True)
                self.condition_axes.set_ylabel(condition_y_title)

                # Plot the condition data with different colour cycle
                col = 'r'
                if( i < len(colors) ):
                    col = colors[i]

                # Average condition data over time
                if(config.condition_average != -1):
                    # Do something
                    condition_xdata, condition_ydata, condition_yerr = self.time_average(condition_xdata, condition_ydata, config.condition_average)
                    condition_plot = self.condition_axes.errorbar(condition_xdata, condition_ydata, condition_yerr, fmt='--', capsize=2, color = col, label=config.condition_label_names[i])
                    plot_list.append(condition_plot[0])
                else:
                    condition_plot = self.condition_axes.plot(condition_xdata, condition_ydata, '--', color = col, label=config.condition_label_names[i])
                    plot_list.append(condition_plot[0])

            # Configure the axis range
            condition_ymin = self.condition_axes.get_ybound()[0]
            if(config.condition_ymin != -1):
                condition_ymin = config.condition_ymin
            condition_ymax = self.condition_axes.get_ybound()[1]
            if(config.condition_ymax != -1):
                condition_ymax = config.condition_ymax
            self.condition_axes.set_ylim([condition_ymin, condition_ymax])

        # Control mouse clicking behaviour
        # Create a special cursor that snaps to growth curves
        self.cursor = SnapToCursor(self.axes, xdata_list, ydata_list, useblit=False, color='red', linewidth=1)
        # Configure the measurement cursor
        if(config.cursor):
            # Clean up previous attributes
            if hasattr(self, 'cid'):
                self.mpl_disconnect(self.cid)

            # Define actions for button press: measure gradient
            def onclick(event):
                self.cursor.onmove(event)
            # Connect action to button press
            self.cid = self.mpl_connect('button_press_event', onclick)
        # Otherwise allow user to change line style
        else:
            delattr(self, 'cursor')
            # Clean up previous attributes
            if hasattr(self, 'cid'):
                self.mpl_disconnect(self.cid)
                
            # Define action on button press: open line style window
            def onpick(event):
                selected_line, line_i = self.find_closest(plot_list, event.xdata, event.ydata)
                self.linewindow = LineStyleWindow(selected_line, line_i, self)
                self.linewindow.show()
            # Connect action to button press
            self.cid = self.mpl_connect('button_press_event', onpick)

        # Apply any saved changes from the line style configuration
        # TODO behaviour when data added/removed
        for pconf in self.plot_config:
            if(pconf[0] > len(plot_list)):
                continue
            plot_list[pconf[0]].set_color(pconf[1][0])
            plot_list[pconf[0]].set_linestyle(pconf[1][1])

        # Switch legend on/off
        if(config.legend):
            self.legend_on = True
            self.legend_title = config.legend_title
            self.axes.legend(title=config.legend_title, loc = 'upper left')
        # Toggle condition legend on
        if(config.condition_legend):
            self.condition_legend_on = True
            self.condition_legend_title = config.condition_legend_title
            self.condition_axes.legend(title=config.condition_legend_title, loc='lower right')

        # Show the plot
        self.draw()

    # Function to convert the time data into the desired unit and get the axis title
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

        if(config.xunit.lower() == 'none'):
            x_title = x_title.replace("["+xaxisdata.unit+"]", "")
        else:
            x_title = x_title.replace("["+xaxisdata.unit+"]", "["+x_unit+"]")
        return xdata, x_title

    # Function to retrieve y data from list of possible signals
    def get_ydata(self, signals, config, condition=False):
        ydata = signals[0].data
        y_title = ''
        found_ydata = False
        yvar = config.yvar
        name = config.yname
        unit = config.yunit
        if condition:
            yvar = config.condition_yvar
            name = config.condition_yname
            unit = config.condition_yunit
        for sig in signals:
            if sig.name == yvar:
                found_ydata = True
                ydata = sig.data
                y_title = sig.title()
                if(name != ''):
                    y_title = y_title.replace(sig.name, name)
                if(unit.lower() == 'none'):
                    y_title = y_title.replace("["+sig.unit+"]", "")
                elif(unit != ''):
                    y_title = y_title.replace("["+sig.unit+"]", "["+unit+"]")
        if not found_ydata:
            raise RuntimeError('Could not find signal %s' % (yvar))
        return ydata, y_title

    # Function to apply alignment, outlier removal and smoothing
    def process_data(self, xdata, ydata, config):
        # Align at time 0 if option selected
        if config.align:
            xdata - xdata[0]

        # remove outliers
        if(config.remove_above >= 0 or config.remove_below >= 0 or config.auto_remove):
            xdata, ydata = self.remove_outliers(xdata, ydata, config)    

        # Smooth the data
        if(config.smooth):
            ydata = savitzky_golay(ydata, 61, 0)
        return xdata, ydata

    # Function to remove outliers in the data
    def remove_outliers(self, xdata, ydata, config):
        data_index = 0
        while data_index < len(ydata):
            if(config.remove_above >= 0 and ydata[data_index] > config.remove_above):
                ydata = np.delete(ydata, data_index)
                xdata = np.delete(xdata, data_index)
                data_index = data_index - 1
            if(config.remove_below >= 0 and ydata[data_index] < config.remove_below):
                ydata = np.delete(ydata, data_index)
                xdata = np.delete(xdata, data_index)
                data_index = data_index -1
            # TODO apply automatic
            #if(config.auto_remove):
            data_index = data_index + 1
        return xdata, ydata

    # Function to average replicate data sets
    def average_data(self, xdatas, ydatas):
        new_xdata = np.array([])
        new_ydata = np.array([])
        new_yerr = np.array([])
        if len(xdatas) <= 1:
            return xdatas[0], ydatas[0]
        for i, x_i in enumerate(xdatas[0]):
            ys = np.array([ydatas[0][i]])
            for j in range(1, len(xdatas), 1):
                result = np.where(xdatas[j] == x_i)
                if(len(result) == 1):
                    ys = np.append(ys, ydatas[j][result[0]])
            # Only average time points shared by all curves
            if(ys.size != len(xdatas)):
                continue
            mean = np.mean(ys)
            std_dev = np.std(ys, ddof=1)
            #std_err = std_dev/np.sqrt(ys.size)
            new_xdata = np.append(new_xdata, x_i)
            new_ydata = np.append(new_ydata, mean)
            new_yerr = np.append(new_yerr, std_dev)
        return new_xdata, new_ydata, new_yerr

    # Function to average data over time period
    def time_average(self, xdata, ydata, window):
        new_xdata = np.array([])
        new_ydata = np.array([])
        new_yerr = np.array([])
        w_i = 1
        i = 0
        while(i < len(xdata)):
            data = np.array([])
            while(i < len(xdata) and xdata[i] < w_i*window):
                #mean = mean + ydata[i]
                data = np.append(data, ydata[i])
                i = i + 1
            mean = np.mean(data)
            std_dev = np.std(data, ddof=1)
            if(data.size == 0):
                continue
            new_xdata = np.append(new_xdata, (w_i-1)*window + window/2.)
            new_ydata = np.append(new_ydata, mean)
            if(data.size == 1):
                new_yerr = np.append(new_yerr, 0)
            else:
                new_yerr = np.append(new_yerr, std_dev)
            w_i = w_i + 1
        return new_xdata, new_ydata, new_yerr

    # Function to find the closest curve to an x,y point TODO how to handle different axis units? (will break if y units very different)
    def find_closest(self, plots, x, y):
        min_dist = 99999
        min_ind = -1
        for i, plot in enumerate(plots):
            dist = np.argmin(np.sqrt(np.power(plot.get_xdata()-x,2)+np.power(plot.get_ydata()-y,2)))
            if(dist < min_dist):
                min_dist = dist
                min_ind = i
        if (min_ind == -1):
            raise RuntimeError('No selected plot')
        return plots[min_ind], min_ind

    # Function to save figure through file handler gui
    def save(self, config):
        save_file(self.fig)

