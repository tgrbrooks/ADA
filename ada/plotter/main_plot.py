# Standard imports
import random
from math import factorial
import numpy as np
from scipy.optimize import curve_fit

# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.colors import is_color_like
import matplotlib.pyplot as plt
import matplotlib.style
from matplotlib.text import Text
import matplotlib as mpl

# Local imports
from ada.plotter.cursor import Cursor, SnapToCursor
from ada.data.models import get_model
from ada.data.data_manager import data_manager
from ada.gui.line_style_window import LineStyleWindow
from ada.gui.file_handler import save_file

import ada.configuration as config
from ada.logger import logger


class PlotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=1200):

        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        self.condition_axes = self.axes.twinx()
        self.condition_axes.set_axis_off()
        self.axes.set_zorder(self.condition_axes.get_zorder() + 1)
        self.axes.patch.set_visible(False)
        self.dragged = None

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
        self.plot()

    def plot(self):
        logger.debug('Creating plot')

        # Reset the plot and configure the base style
        logger.debug('Resetting plot and configuring style')
        self.set_style()
        self.clear_axes()
        self.plot_list = []
        self.set_axes_style()

        # Return an empty plot if there's no data
        if(data_manager.growth_data.empty and data_manager.condition_data.empty):
            logger.debug('No data present')
            self.axes.set_title('Empty plot')
            self.draw()
            return

        # Plot the condition data on a separate axis if it exists
        if not data_manager.condition_data.empty:
            logger.debug('Plotting condition data')
            self.create_condition_axis()
            self.plot_condition_data()
            # Configure the axis range
            self.set_condition_range()

        self.x_title = ''
        self.y_title = ''
        self.xdata_list = []
        self.ydata_list = []
        self.plot_data()

        logger.debug('Creating events')
        self.create_events()

        # If we're fitting the data
        if config.do_fit:
            logger.debug('Fitting the data')
            self.fit_data()

        # Switch grid on/off
        self.axes.grid(config.grid)

        self.set_axes_scale()
        self.set_titles()
        self.set_axes_ranges()

        self.set_cursor()

        self.set_plot_styles()
        self.set_legends()

        # Show the plot
        self.draw()

    def set_style(self):
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
        return

    def clear_axes(self):
        # Clear axes and set default visibility
        self.axes.clear()
        # Remove and recreate the twinned axis to prevent the x axis getting
        # somehow remembered
        self.condition_axes.remove()
        self.condition_axes = self.axes.twinx()
        self.condition_axes.set_axis_off()
        self.axes.patch.set_visible(False)
        self.axes.spines['right'].set_visible(True)
        return

    def set_axes_style(self):
        # More style settings
        if(config.font_style != ''):
            self.axes.xaxis.label.set_family(config.font_style)
            self.axes.yaxis.label.set_family(config.font_style)
            self.condition_axes.yaxis.label.set_family(config.font_style)
        if(config.title_size >= 0):
            self.axes.xaxis.label.set_size(config.title_size)
            self.axes.yaxis.label.set_size(config.title_size)
            self.condition_axes.yaxis.label.set_size(config.title_size)
        return

    def create_condition_axis(self):
        self.condition_axes.set_axis_on()
        # Configure axis colour and visibility
        caxis_colour = 'red'
        if(is_color_like(config.axis_colour)):
            caxis_colour = config.axis_colour
        self.condition_axes.spines['right'].set_color(caxis_colour)
        self.axes.spines['right'].set_visible(False)
        self.condition_axes.tick_params(axis='y', colors=caxis_colour)
        self.condition_axes.yaxis.label.set_color(caxis_colour)
        return

    def plot_condition_data(self):
        # Loop over the condition data files
        for i in range(data_manager.num_condition_files()):
            # Get the condition data in the right time units. averaging if required
            xdata, ydata, yerr = data_manager.get_condition_data(i)
            ytitle = data_manager.get_condition_ytitle(i)
            self.condition_axes.set_ylabel(ytitle)
            legend_label = data_manager.get_condition_legend(i)

            # Plot the condition data with different colour cycle
            col = 'r'
            if i < len(config.conf_colors):
                col = config.conf_colors[i]

            if(config.condition_average != -1):
                condition_plot = \
                    self.condition_axes.errorbar(xdata,
                                                 ydata,
                                                 yerr, fmt='--',
                                                 capsize=2, color=col,
                                                 label=legend_label)
                self.plot_list.append([condition_plot[0]])
            elif yerr is not None:
                condition_plot = \
                    self.condition_axes.plot(xdata, ydata,
                                             '--', color=col,
                                             label=legend_label)
                fill_area = self.condition_axes.fill_between(xdata, ydata-yerr,
                                                   ydata+yerr, color=col, alpha=0.4)
                self.plot_list.append([condition_plot[0], fill_area])
            else:
                print(xdata, ydata)
                condition_plot = \
                    self.condition_axes.plot(xdata, ydata,
                                             '--', color=col,
                                             label=legend_label)
                self.plot_list.append([condition_plot[0]])

    def plot_data(self):
        for i in range(data_manager.num_growth_files()):
            xdata, ydata, yerr = data_manager.get_xy_data(i, config.yvar)
            self.x_title, self.y_title = data_manager.get_titles(i)
            legend_label = data_manager.get_growth_legend(i)

            if yerr is not None:
                growth_plot = self.axes.plot(xdata, ydata, '-',
                                             label=legend_label)
                fill_area = self.axes.fill_between(xdata, ydata-yerr,
                                                   ydata+yerr, alpha=0.4)
                self.plot_list.append([growth_plot[0], fill_area])
            else:
                if config.ynormlog:
                    ydata = np.log(ydata/ydata[0])

                growth_plot = self.axes.plot(xdata, ydata, '-',
                                             label=legend_label)
                self.plot_list.append([growth_plot[0]])

            self.xdata_list.append(xdata)
            self.ydata_list.append(ydata)

    def create_events(self):
        # Show event information
        self.event_annotation = self.axes.annotate('',
                                                   xy=(0, 0),
                                                   xytext=(-20, 20),
                                                   textcoords="offset points",
                                                   bbox=dict(
                                                       boxstyle="round", fc="w"),
                                                   arrowprops=dict(arrowstyle="->"))
        self.event_annotation.set_visible(False)
        self.annotation_names = []
        annotation_xpos = []
        annotation_ypos = []
        if config.show_events:
            for i, data in enumerate(data_manager.get_growth_data_files()):
                for data_event in data.events:
                    event_label = data_event.datetime.strftime(
                        '%d/%m/%Y %H:%M:%S')
                    for lab in data_event.labels:
                        event_label += '\n' + lab
                    self.annotation_names.append(event_label)
                    event_xpos = data_event.get_xpos(config.xvar)
                    annotation_xpos.append(event_xpos)
                    x_idx = np.abs(self.xdata_list[i] - event_xpos).argmin()
                    event_ypos = self.ydata_list[i][x_idx]
                    annotation_ypos.append(event_ypos)
            self.event_scatter = self.axes.scatter(annotation_xpos,
                                                   annotation_ypos,
                                                   s=10,
                                                   c='black')
        return

    def fit_data(self):
        logger.debug('Fitting %s with %s' %
                     (config.fit_curve, config.fit_type))
        # Find the curve to fit
        fit_index = -1
        for i, dat in enumerate(data_manager.get_growth_data_files()):
            if config.fit_curve == dat.label:
                fit_index = i
        # If the data hasn't been found
        if fit_index == -1:
            return

        fit_x, _, _ = data_manager.get_fit_data(fit_index)
        x_unit, y_unit = data_manager.get_units(fit_index)

        model = get_model(config.fit_type, x_unit, y_unit)
        func = model.func()

        fit_result, covm = data_manager.get_fit(fit_index)
        self.axes.plot(fit_x, func(fit_x, *fit_result),
                       '-', color='r', label='Fit')

        bounding_box = dict(boxstyle="round", ec=(
            1., 0.5, 0.5), fc=(1., 0.8, 0.8))
        if config.show_fit_text:
            self.axes.text(0.25, 0.95, model.latex,
                           transform=self.axes.transAxes,
                           bbox=bounding_box, picker=True)

        if config.show_fit_result and not config.show_fit_errors:
            self.axes.text(0.25, 0.65, model.param_text(fit_result),
                           transform=self.axes.transAxes,
                           bbox=bounding_box, picker=True)

        if config.show_fit_result and config.show_fit_errors:
            self.axes.text(0.25, 0.65, model.param_text_error(fit_result, covm),
                           transform=self.axes.transAxes,
                           bbox=bounding_box, picker=True)

        return

    def set_axes_scale(self):
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
        return

    def set_titles(self):
        # Configure axis labels
        self.axes.set_title('')
        if(config.title != ''):
            self.axes.set_title(config.title)
        self.axes.set_xlabel(self.x_title)
        self.axes.set_ylabel(self.y_title)
        return

    def set_condition_range(self):
        condition_ymin = self.condition_axes.get_ybound()[0]
        if(config.condition_ymin != -1):
            condition_ymin = config.condition_ymin
        condition_ymax = self.condition_axes.get_ybound()[1]
        if(config.condition_ymax != -1):
            condition_ymax = config.condition_ymax
        self.condition_axes.set_ylim([condition_ymin, condition_ymax])
        return

    def set_axes_ranges(self):
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
        return

    def set_cursor(self):
        # Control mouse clicking behaviour
        # Create a special cursor that snaps to growth curves
        self.cursor = SnapToCursor(self.axes, self.xdata_list, self.ydata_list,
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
                if isinstance(event.artist, Text):
                    self.dragged = event.artist
                    self.pick_pos = (event.mouseevent.xdata,
                                     event.mouseevent.ydata)
                return True

            def onpress(event):
                _, line_i, min_dist = \
                    self.find_closest(self.plot_list, event.xdata, event.ydata)
                if min_dist < 5:
                    self.linewindow = LineStyleWindow(self.plot_list[line_i],
                                                      line_i, self)
                    self.linewindow.show()
                return True

            def on_release_event(event):
                if self.dragged is not None:
                    old_pos = self.dragged.get_position()
                    inv = self.axes.transAxes.inverted()
                    pick_pos = inv.transform(self.axes.transData.transform(
                        (self.pick_pos[0], self.pick_pos[1])))
                    event_pos = inv.transform(
                        self.axes.transData.transform((event.xdata, event.ydata)))
                    new_pos = (old_pos[0] + event_pos[0] - pick_pos[0],
                               old_pos[1] + event_pos[1] - pick_pos[1])
                    self.dragged.set_position(new_pos)
                    self.dragged = None
                    self.draw_idle()
                return True

            # Connect action to button press
            self.cid = self.mpl_connect('button_press_event', onpress)
            self.mpl_connect('pick_event', onpick)
            self.mpl_connect("button_release_event", on_release_event)

            def update_annotation(ind):
                evt_pos = self.event_scatter.get_offsets()[ind["ind"][0]]
                self.event_annotation.xy = evt_pos
                event_text = self.annotation_names[ind["ind"][0]]
                self.event_annotation.set_text(event_text)

            def onhover(event):
                vis = self.event_annotation.get_visible()
                cont = None
                if event.inaxes == self.axes:
                    cont, ind = self.event_scatter.contains(event)
                if cont:
                    update_annotation(ind)
                    self.event_annotation.set_visible(True)
                    self.draw_idle()
                else:
                    if vis:
                        self.event_annotation.set_visible(False)
                        self.draw_idle()

            if config.show_events:
                self.mpl_connect('motion_notify_event', onhover)
        return

    def set_plot_styles(self):
        # Apply any saved changes from the line style configuration
        # TODO behaviour when data added/removed
        for pconf in self.plot_config:
            if(pconf[0] > len(self.plot_list)):
                continue
            self.plot_list[pconf[0]][0].set_color(pconf[1][0])
            self.plot_list[pconf[0]][0].set_linestyle(pconf[1][1])
            if len(self.plot_list[pconf[0]]) > 1:
                self.plot_list[pconf[0]][1].set_color(pconf[1][0])
        return

    def set_legends(self):
        # Switch legend on/off
        if(config.legend):
            self.legend_on = True
            self.legend_title = config.legend_title
            leg = self.axes.legend(title=config.legend_title,
                                   loc='upper left')
            leg.set_draggable(True)

        # Toggle condition legend on
        if(config.condition_legend and not data_manager.condition_data.empty):
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
        return

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
