# Standard imports
import random
from math import factorial
import numpy as np

# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.colors import is_color_like
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl

# Local imports
from ada.reader.data_holder import DataHolder
from ada.plotter.cursor import Cursor, SnapToCursor
from ada.plotter.functions import (process_data, average_data,
    time_average, exponent_text)
from ada.gui.line_style_window import LineStyleWindow
from ada.gui.file_handler import save_file

import ada.configuration as config


class PlotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        self.condition_axes = self.axes.twinx()
        self.condition_axes.set_axis_off()
        self.axes.set_zorder(self.condition_axes.get_zorder() + 1)
        self.axes.patch.set_visible(False)

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        self.parent = parent

        self.legend_on = False
        self.condition_legend_on = False
        self.plot_config = []

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        empty_data = DataHolder()
        empty_condition = DataHolder()
        self.plot(empty_data, empty_condition)

    def plot(self, data, condition_data):

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
        # Remove and recreate the twinned axis to prevent the x axis getting
        # somehow remembered
        self.condition_axes.remove()
        self.condition_axes = self.axes.twinx()
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
            condition_xdata, condition_x_title = \
                self.convert_xdata(cdata.xaxis)

            # Get the desired condition data and configure title
            condition_ydata, condition_y_title = \
                self.get_ydata(cdata.signals, True)
            self.condition_axes.set_ylabel(condition_y_title)

            # Get the legend label with any extra info specified in
            # the configuration
            legend_label = config.condition_label_names[i]
            if (config.condition_extra_info != 'none' and not
                    config.condition_only_extra):
                legend_label = \
                    (legend_label + ' ('
                     + cdata.get_header_info(config.condition_extra_info)
                     + ')')
            elif (config.condition_extra_info != 'none' and
                    config.condition_only_extra):
                legend_label = \
                    cdata.get_header_info(config.condition_extra_info)

            # Plot the condition data with different colour cycle
            col = 'r'
            if(i < len(colors)):
                col = colors[i]

            # Average condition data over time
            if(config.condition_average != -1):
                # Do something
                condition_xdata, condition_ydata, condition_yerr = \
                    time_average(condition_xdata, condition_ydata,
                                 config.condition_average, config.std_err)
                condition_plot = \
                    self.condition_axes.errorbar(condition_xdata,
                                                 condition_ydata,
                                                 condition_yerr, fmt='--',
                                                 capsize=2, color=col,
                                                 label=legend_label)
                plot_list.append([condition_plot[0]])
            else:
                condition_plot = \
                    self.condition_axes.plot(condition_xdata, condition_ydata,
                                             '--', color=col,
                                             label=legend_label)
                plot_list.append([condition_plot[0]])

        # Configure the axis range
        if not condition_data.empty:
            condition_ymin = self.condition_axes.get_ybound()[0]
            if(config.condition_ymin != -1):
                condition_ymin = config.condition_ymin
            condition_ymax = self.condition_axes.get_ybound()[1]
            if(config.condition_ymax != -1):
                condition_ymax = config.condition_ymax
            self.condition_axes.set_ylim([condition_ymin, condition_ymax])

        x_title = ''
        y_title = ''
        xdata_list = []
        ydata_list = []
        for i, dat in enumerate(data.data_files):
            # Convert the units of time if needed
            xdata, x_title = self.convert_xdata(dat.xaxis)
            # Get the y axis data for plotting
            ydata, y_title = self.get_ydata(dat.signals)

            legend_label = config.label_names[i]
            if(config.extra_info != 'none' and not config.only_extra):
                legend_label = (legend_label + ' ('
                                + dat.get_header_info(config.extra_info) + ')')
            elif(config.extra_info != 'none' and config.only_extra):
                legend_label = dat.get_header_info(config.extra_info)

            # Apply alignment, outlier removal, and smoothing
            xdata, ydata = process_data(xdata, ydata)

            # If there are replicate files then average the data
            if(len(data.replicate_files[i]) > 1):
                xdatas = [xdata]
                ydatas = [ydata]
                for j in range(1, len(data.replicate_files[i]), 1):
                    rep_xdata, rep_xtitle = \
                        self.convert_xdata(data.replicate_files[i][j].xaxis)
                    rep_ydata, rep_ytitle = \
                        self.get_ydata(data.replicate_files[i][j].signals)
                    rep_xdata, rep_ydata = process_data(rep_xdata, rep_ydata)
                    xdatas.append(rep_xdata)
                    ydatas.append(rep_ydata)

                xdata, ydata, yerr = average_data(xdatas, ydatas,
                                                  config.std_err)

                if config.ynormlog:
                    yerr = yerr/ydata
                    ydata = np.log(ydata/ydata[0])

                growth_plot = self.axes.plot(xdata, ydata, '-',
                                             label=legend_label)
                fill_area = self.axes.fill_between(xdata, ydata-yerr,
                                                   ydata+yerr, alpha=0.4)
                plot_list.append([growth_plot[0], fill_area])
            else:
                if config.ynormlog:
                    ydata = np.log(ydata/ydata[0])

                growth_plot = self.axes.plot(xdata, ydata, '-',
                                             label=legend_label)
                plot_list.append([growth_plot[0]])

            
            xdata_list.append(xdata)
            ydata_list.append(ydata)

        # Show event information
        event_annotation = self.axes.annotate('',
                                        xy=(0, 0),
                                        xytext=(-20,20),
                                        textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="w"),
                                        arrowprops=dict(arrowstyle="->"))
        event_annotation.set_visible(False)
        annotation_names = []
        annotation_xpos = []
        annotation_ypos = []
        if config.show_events:
            for i, data in enumerate(data.data_files):
                for data_event in data.events:
                    event_label = data_event.datetime.strftime('%d/%m/%Y %H:%M:%S')
                    for lab in data_event.labels:
                        event_label += '\n' + lab
                    annotation_names.append(event_label)
                    event_xpos = self.convert_xpos(data_event.xpos)
                    annotation_xpos.append(event_xpos)
                    x_idx = np.abs(xdata_list[i] - event_xpos).argmin()
                    event_ypos = ydata_list[i][x_idx]
                    annotation_ypos.append(event_ypos)
            event_scatter = self.axes.scatter(annotation_xpos,
                                              annotation_ypos,
                                              s=10,
                                              c='black')

        # If we're fitting the data
        if config.do_fit:
            # Find the curve to fit
            fit_index = -1
            for i, data in enumerate(data.data_files):
                if config.fit_curve == data.label:
                    fit_index = i
            fit_x = xdata_list[fit_index]
            fit_y = ydata_list[fit_index]

            # If the data has been found
            if fit_index != -1:
                # Set the polynomial degree for the fit
                fit_degree = 0
                if (config.fit_type == 'linear' or 
                    config.fit_type == 'exponential'):
                    fit_degree = 1
                elif config.fit_type == 'quadratic':
                    fit_degree = 2

                # Only fit the data in the given range
                from_index = np.abs(fit_x - config.fit_from).argmin()
                to_index = np.abs(fit_x - config.fit_to).argmin()
                fit_x = fit_x[from_index:to_index]
                fit_y = fit_y[from_index:to_index]

                # Need to manipulate the y data and weights if fitting an exp
                weights = None
                if config.fit_type == 'exponential':
                    weights = np.sqrt(fit_y)
                    fit_y = np.log(fit_y)

                # Get the fit results
                fit_result = np.polyfit(fit_x, fit_y, fit_degree, w=weights)

                # Plot the resultant function
                plot_x = np.linspace(config.fit_from, config.fit_to, 1000)
                x_unit = ''
                if(len(x_title.split('[')) > 1):
                    x_unit = (x_title.split('[')[1]).split(']')[0]
                y_unit = ''
                if(len(y_title.split('[')) > 1):
                    y_unit = (y_title.split('[')[1]).split(']')[0]

                # Flat line fit result
                plot_y = 0. * plot_x + fit_result[0]
                fit_func_text = '$y = p$'
                param_text = ('p = ' + exponent_text(fit_result[0]) + ' ' +
                              y_unit)

                # Linear fit result
                if config.fit_type == 'linear':
                    plot_y = fit_result[0] * plot_x + fit_result[1]
                    fit_func_text = '$y = p_1 \cdot x + p_0$'
                    param_text = ('$p_0$ = ' + exponent_text(fit_result[1]) +
                                  ' ' + y_unit + '\n' +
                                  '$p_1$ = ' + exponent_text(fit_result[0]) +
                                  ' ' + y_unit + '/' + x_unit)

                # Quadratic fit result
                elif config.fit_type == 'quadratic':
                    plot_y = (fit_result[0] * np.power(plot_x,2) +
                             fit_result[1] * plot_x + fit_result[2])
                    fit_func_text = '$y = p_2 \cdot x^2 + p_1 \cdot x + p_0$'
                    param_text = ('$p_0$ = ' + exponent_text(fit_result[2]) +
                                  ' ' + y_unit + '\n' +
                                  '$p_1$ = ' + exponent_text(fit_result[1]) +
                                  ' ' + y_unit + '/' + x_unit + '\n' +
                                  '$p_2$ = ' + exponent_text(fit_result[0]) +
                                  ' ' + y_unit + '/' + x_unit + '$^2$')

                #qExponential fit result
                elif config.fit_type == 'exponential':
                    plot_y = np.exp(fit_result[0] * plot_x + fit_result[1])
                    fit_func_text = '$y = p_0 \cdot \exp(p_1 \cdot x)$'
                    param_text = ('$p_0$ = ' +
                                  exponent_text(np.exp(fit_result[1])) +
                                  ' ' + y_unit + '\n' +
                                  '$p_1$ = ' + exponent_text(fit_result[0]) +
                                  ' ' + y_unit + '/' + x_unit)

                fit_plot = self.axes.plot(plot_x, plot_y, '-', color='r', 
                                          label='Fit')
                self.axes.text(0.25, 0.95, fit_func_text,
                               transform=self.axes.transAxes,
                               bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5),
                                         fc=(1., 0.8, 0.8)))
                self.axes.text(0.25, 0.75, param_text,
                               transform=self.axes.transAxes,
                               bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5),
                                         fc=(1., 0.8, 0.8)))

        # Switch grid on/off
        self.axes.grid(config.grid)

        if(config.ylog):
            self.axes.set_yscale('log')
        else:
            self.axes.set_yscale('linear')
        if(config.xlog):
            self.axes.set_xscale('log')
            self.condition_axes.set_xscale('log')
        else:
            self.axes.set_xscale('linear')
            self.condition_axes.set_xscale('linear')
        if(config.condition_ylog):
            self.condition_axes.set_yscale('log')
        else:
            self.condition_axes.set_yscale('linear')

        # Configure axis labels
        self.axes.set_title('')
        if(config.title != ''):
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

        # Control mouse clicking behaviour
        # Create a special cursor that snaps to growth curves
        self.cursor = SnapToCursor(self.axes, xdata_list, ydata_list,
                                   useblit=False, color='red', linewidth=1)

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
                selected_line, line_i, min_dist = \
                    self.find_closest(plot_list, event.xdata, event.ydata)
                if min_dist < 5:
                    self.linewindow = LineStyleWindow(plot_list[line_i],
                                                      line_i, self)
                    self.linewindow.show()
            # Connect action to button press
            self.cid = self.mpl_connect('button_press_event', onpick)

            def update_annotation(ind):
                evt_pos = event_scatter.get_offsets()[ind["ind"][0]]
                event_annotation.xy = evt_pos
                event_text = annotation_names[ind["ind"][0]]
                event_annotation.set_text(event_text)

            def onhover(event):
                vis = event_annotation.get_visible()
                cont = None
                if event.inaxes == self.axes:
                    cont, ind = event_scatter.contains(event)
                if cont:
                    update_annotation(ind)
                    event_annotation.set_visible(True)
                    self.draw_idle()
                else:
                    if vis:
                        event_annotation.set_visible(False)
                        self.draw_idle()

            if config.show_events:
                self.mpl_connect('motion_notify_event', onhover)

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
            leg = self.axes.legend(title=config.legend_title,
                                   loc='upper left')
            leg.set_draggable(True)

        # Toggle condition legend on
        if(config.condition_legend and not condition_data.empty):
            self.condition_legend_on = True
            self.condition_legend_title = config.condition_legend_title
            handles, labels = self.condition_axes.get_legend_handles_labels()
            cond_leg = self.axes.legend(
                handles, labels,
                title=config.condition_legend_title, loc='lower right'
            )
            cond_leg.set_draggable(True)
            if(config.legend):
                self.axes.add_artist(leg)

        # Show the plot
        self.draw()

    # Function to convert the time data into the desired unit and
    # get the axis title
    def convert_xdata(self, xaxisdata):
        xdata = xaxisdata.data
        x_title = xaxisdata.title()
        if(config.xname != ''):
            x_title = x_title.replace(xaxisdata.name, config.xname)
        x_unit = xaxisdata.unit
        if(config.xvar == 'seconds'):
            x_unit = 'sec'
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

    def convert_xpos(self, xpos):
        xpos_out = xpos
        if(config.xvar == 'minutes'):
            xpos_out = xpos / 60.
        if(config.xvar == 'hours'):
            xpos_out = xpos / (60.*60.)
        if(config.xvar == 'days'):
            xpos_out = xpos / (60.*60.*24.)

        return xpos_out

    # Function to retrieve y data from list of possible signals
    def get_ydata(self, signals, condition=False):
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
                # Loaded calibration curve takes precedence
                if yvar == 'CD' and self.parent.calibration is not None:
                    continue
                found_ydata = True
                ydata = sig.data
                y_title = sig.title()
                if(name != ''):
                    y_title = y_title.replace(sig.name, name)
                if(unit.lower() == 'none'):
                    y_title = y_title.replace("["+sig.unit+"]", "")
                elif(unit != ''):
                    y_title = y_title.replace("["+sig.unit+"]", "["+unit+"]")
            elif yvar == 'CD' and self.parent.calibration is not None and sig.name == 'OD':
                found_ydata = True
                ydata = self.parent.calibration.calibrate_od(sig.data)
                y_title = 'CD'
        if config.ynormlog and name == '' and not condition:
            y_title = 'ln('+yvar+'/'+yvar+'$_{0}$)'
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
                xnew, ynew = plot[0].axes.transData.transform_point(
                    (xold, plot[0].get_ydata()[j])
                )
                xdata_display = np.append(xdata_display, xnew)
                ydata_display = np.append(ydata_display, ynew)
            dist = np.sqrt(np.power(xdata_display - x_display, 2)
                           + np.power(ydata_display - y_display, 2))
            dist_i = np.argmin(dist)
            distance = dist[dist_i]
            if(distance < min_dist):
                min_dist = distance
                min_ind = i
        if (min_ind == -1):
            raise RuntimeError('No selected plot')
        return plots[min_ind][0], min_ind, min_dist

    # Function to save figure through file handler gui
    def save(self):
        save_file(self.fig)
