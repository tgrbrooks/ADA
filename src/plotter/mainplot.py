# Local imports
from src.reader.dataholder import DataHolder
from src.gui.configuration import Configuration
from src.plotter.cursor import Cursor, SnapToCursor
from src.plotter.functions import process_data, average_data, time_average
from src.gui.linestylewindow import LineStyleWindow
from src.gui.filehandler import save_file

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
        if(config.title_size >= 0):
            mpl.rcParams['axes.titlesize'] = config.title_size
            mpl.rcParams['figure.titlesize'] = config.title_size
        if(config.legend_size >= 0):
            mpl.rcParams['legend.fontsize'] = config.legend_size
            mpl.rcParams['legend.title_fontsize'] = config.legend_size
        if(config.label_size >= 0):
            mpl.rcParams['xtick.labelsize'] = config.label_size
            mpl.rcParams['ytick.labelsize'] = config.label_size
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
        if(config.title_size >= 0):
            self.axes.xaxis.label.set_size(config.title_size)
            self.axes.yaxis.label.set_size(config.title_size)
            self.condition_axes.yaxis.label.set_size(config.title_size)

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

            legend_label = config.label_names[i]
            if(config.extra_info != 'none' and not config.only_extra):
                legend_label = legend_label + ' (' + dat.get_header_info(config.extra_info) + ')'
            elif(config.extra_info != 'none' and config.only_extra):
                legend_label = dat.get_header_info(config.extra_info)

            # Apply alignment, outlier removal, and smoothing
            xdata, ydata = process_data(xdata, ydata, config)

            # If there are replicate files then average the data
            if(len(data.replicate_files[i]) > 1):
                xdatas = [xdata]
                ydatas = [ydata]
                for j in range(1, len(data.replicate_files[i]), 1):
                    rep_xdata, rep_xtitle = self.convert_xdata(data.replicate_files[i][j].xaxis, config)
                    rep_ydata, rep_ytitle = self.get_ydata(data.replicate_files[i][j].signals, config)
                    rep_xdata, rep_ydata = process_data(rep_xdata, rep_ydata, config)
                    xdatas.append(rep_xdata)
                    ydatas.append(rep_ydata)
                xdata, ydata, yerr = average_data(xdatas, ydatas, config.std_err)
                growth_plot = self.axes.plot(xdata, ydata, '-', label=legend_label)
                fill_area = self.axes.fill_between(xdata, ydata-yerr, ydata+yerr, alpha=0.4)
                plot_list.append([growth_plot[0], fill_area])
            else:
                growth_plot = self.axes.plot(xdata, ydata, '-', label=legend_label)
                plot_list.append([growth_plot[0]])

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

                # Get the legend label with any extra info specified in the configuration
                legend_label = config.condition_label_names[i]
                if(config.condition_extra_info != 'none' and not config.condition_only_extra):
                    legend_label = legend_label + ' (' + dat.get_header_info(config.condition_extra_info) + ')'
                elif(config.condition_extra_info != 'none' and config.condition_only_extra):
                    legend_label = dat.get_header_info(config.condition_extra_info)

                # Plot the condition data with different colour cycle
                col = 'r'
                if( i < len(colors) ):
                    col = colors[i]

                # Average condition data over time
                if(config.condition_average != -1):
                    # Do something
                    condition_xdata, condition_ydata, condition_yerr = time_average(condition_xdata, condition_ydata, config.condition_average, config.std_err)
                    condition_plot = self.condition_axes.errorbar(condition_xdata, condition_ydata, condition_yerr, fmt='--', capsize=2, color = col, label=legend_label)
                    plot_list.append([condition_plot[0]])
                else:
                    condition_plot = self.condition_axes.plot(condition_xdata, condition_ydata, '--', color = col, label=legend_label)
                    plot_list.append([condition_plot[0]])

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
                selected_line, line_i, min_dist = self.find_closest(plot_list, event.xdata, event.ydata)
                if min_dist < 5:
                    self.linewindow = LineStyleWindow(plot_list[line_i], line_i, self)
                    self.linewindow.show()
            # Connect action to button press
            self.cid = self.mpl_connect('button_press_event', onpick)

        # Apply any saved changes from the line style configuration
        # TODO behaviour when data added/removed
        for pconf in self.plot_config:
            if(pconf[0] > len(plot_list)):
                continue
            plot_list[pconf[0]][0].set_color(pconf[1][0])
            plot_list[pconf[0]][0].set_linestyle(pconf[1][1])
            if len(plot_list[pconf[0]]) > 1:
                plot_list[pconf[0]][1].set_color(pconf[1][0])

        # Switch legend on/off
        if(config.legend):
            self.legend_on = True
            self.legend_title = config.legend_title
            leg = self.axes.legend(title=config.legend_title, loc = 'upper left')
            leg.set_draggable(True)
        # Toggle condition legend on
        if(config.condition_legend):
            self.condition_legend_on = True
            self.condition_legend_title = config.condition_legend_title
            cond_leg = self.condition_axes.legend(title=config.condition_legend_title, loc='lower right')
            cond_leg.set_draggable(True)

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

    # Function to find the closest curve to an x,y point
    def find_closest(self, plots, x, y):
        min_dist = 99999
        min_ind = -1
        # Transform to display coordinates
        x_display, y_display = self.axes.transData.transform_point((x, y))
        for i, plot in enumerate(plots):
            xdata_display = np.array([])
            ydata_display = np.array([])
            # Transform all points to display coordinates
            for j, xold in enumerate(plot[0].get_xdata()):
                xnew, ynew = plot[0].axes.transData.transform_point((xold, plot[0].get_ydata()[j]))
                xdata_display = np.append(xdata_display, xnew)
                ydata_display = np.append(ydata_display, ynew)
            dist = np.sqrt(np.power(xdata_display-x_display,2)+np.power(ydata_display-y_display,2))
            dist_i = np.argmin(dist)
            distance = dist[dist_i]
            if(distance < min_dist):
                min_dist = distance
                min_ind = i
        if (min_ind == -1):
            raise RuntimeError('No selected plot')
        return plots[min_ind][0], min_ind, min_dist

    # Function to save figure through file handler gui
    def save(self, config):
        save_file(self.fig)



