# Standard imports
import numpy as np

# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.colors import is_color_like
from matplotlib.text import Text
import matplotlib as mpl
import matplotlib.style as style

# Local imports
from ada.plotter.cursor import SnapToCursor
from ada.data.models import get_model
from ada.data.data_manager import data_manager
from ada.gui.line_style_window import LineStyleWindow
from ada.gui.file_handler import save_file

from ada.configuration import config
from ada.logger import logger


class PlotObject():
    def __init__(self, data, plots, plot_type):
        self.data = data
        self.type = plot_type
        self.plots = []
        if plot_type == "line":
            self.plots = [plots[0]]
        elif self.type == "errorbar":
            self.plots = [plots[0], plots[1][0], plots[1][1], plots[2][0]]
        elif self.type == "fill":
            self.plots = [plots[0][0], plots[1]]

    def set_style(self):
        if "style" in self.data.style:
            if config['style']['plot_style'] != self.data.style["style"]:
                return
        else:
            return
        if "color" in self.data.style:
            self.set_color(self.data.style["color"])
        if "marker" in self.data.style:
            self.set_marker(self.data.style["marker"])
        if "linestyle" in self.data.style:
            self.set_linestyle(self.data.style["linestyle"])

    def save_style(self):
        self.data.style["style"] = config['style']['plot_style']
        self.data.style["color"] = self.plots[0].get_color()
        self.data.style["marker"] = self.plots[0].get_marker()
        self.data.style["linestyle"] = self.plots[0].get_linestyle()

    def set_color(self, color):
        for i, _ in enumerate(self.plots):
            self.plots[i].set_color(color)

    def set_marker(self, color):
        self.plots[0].set_marker(color)

    def set_linestyle(self, color):
        self.plots[0].set_linestyle(color)


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
        if config['fit']['do_fit']:
            logger.debug('Fitting the data')
            self.fit_data()

        # Switch grid on/off
        self.axes.grid(config['style']['grid'])

        self.set_axes_scale()
        self.set_titles()
        self.set_axes_ranges()

        self.set_cursor()

        self.set_plot_styles()
        self.set_legends()

        # Show the plot
        self.draw()
        self.save_plot_styles()

    def set_style(self):
        # Style configuration
        if(config['style']['plot_style'] != ''):
            if(config['style']['plot_style'] == 'default'):
                style.use('default')
            if(config['style']['plot_style'] == 'greyscale'):
                style.use('grayscale')
            if(config['style']['plot_style'] == 'colour blind'):
                style.use('seaborn-colorblind')
            if(config['style']['plot_style'] == 'pastel'):
                style.use('seaborn-pastel')
            if(config['style']['plot_style'] == 'deep'):
                style.use('seaborn-colorblind')
        if(config['style']['font_style'] != ''):
            mpl.rcParams['font.family'] = config['style']['font_style']
        if(config['style']['title_size'] >= 0):
            mpl.rcParams['axes.titlesize'] = config['style']['title_size']
            mpl.rcParams['figure.titlesize'] = config['style']['title_size']
        if(config['style']['legend_size'] >= 0):
            mpl.rcParams['legend.fontsize'] = config['style']['legend_size']
            mpl.rcParams['legend.title_fontsize'] = config['style']['legend_size']
        if(config['style']['label_size'] >= 0):
            mpl.rcParams['xtick.labelsize'] = config['style']['label_size']
            mpl.rcParams['ytick.labelsize'] = config['style']['label_size']
        if(config['style']['line_width'] >= 0):
            mpl.rcParams['lines.linewidth'] = config['style']['line_width']
        if(config['style']['marker_size'] >= 0):
            mpl.rcParams['lines.markersize'] = config['style']['marker_size']
        if(config['style']['save_dpi'] >= 0):
            mpl.rcParams['savefig.dpi'] = config['style']['save_dpi']
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
        if(config['style']['font_style'] != ''):
            self.axes.xaxis.label.set_family(config['style']['font_style'])
            self.axes.yaxis.label.set_family(config['style']['font_style'])
            self.condition_axes.yaxis.label.set_family(config['style']['font_style'])
        if(config['style']['title_size'] >= 0):
            self.axes.xaxis.label.set_size(config['style']['title_size'])
            self.axes.yaxis.label.set_size(config['style']['title_size'])
            self.condition_axes.yaxis.label.set_size(config['style']['title_size'])
        return

    def create_condition_axis(self):
        self.condition_axes.set_axis_on()
        # Configure axis colour and visibility
        caxis_colour = 'red'
        if(is_color_like(config['style']['axis_colour'])):
            caxis_colour = config['style']['axis_colour']
        self.condition_axes.spines['right'].set_color(caxis_colour)
        self.axes.spines['right'].set_visible(False)
        self.condition_axes.tick_params(axis='y', colors=caxis_colour)
        self.condition_axes.yaxis.label.set_color(caxis_colour)
        return

    def plot_condition_data(self):
        # Loop over the condition data files
        for i in range(data_manager.num_condition_files()):
            if not data_manager.get_condition_file(i).visible:
                continue
            # Get the condition data in the right time units. averaging if required
            xdata, ydata, yerr = data_manager.get_condition_data(i)
            ytitle = data_manager.get_condition_ytitle(i)
            self.condition_axes.set_ylabel(ytitle)
            legend_label = data_manager.get_condition_legend(i)

            # Plot the condition data with different colour cycle
            col = 'r'
            if i < len(opt.conf_colors):
                col = opt.conf_colors[i]

            if(config['data']['condition_average'] is not None):
                condition_plot = self.condition_axes.errorbar(xdata,
                                                              ydata,
                                                              yerr, fmt='--',
                                                              capsize=config['style']['capsize'], color=col,
                                                              label=legend_label)
                self.plot_list.append(PlotObject(data_manager.get_condition_file(i),
                                                 condition_plot,
                                                 "errorbar"))
            elif yerr is not None:
                condition_plot = self.condition_axes.plot(xdata, ydata,
                                                          '--', color=col,
                                                          label=legend_label)
                fill_area = self.condition_axes.fill_between(xdata, ydata-yerr,
                                                             ydata+yerr, color=col, alpha=0.4)
                self.plot_list.append(PlotObject(data_manager.get_condition_file(i),
                                                 [condition_plot, fill_area],
                                                 "fill"))
            else:
                condition_plot = self.condition_axes.plot(xdata, ydata,
                                                          '--', color=col,
                                                          label=legend_label)
                self.plot_list.append(PlotObject(data_manager.get_condition_file(i),
                                                 condition_plot,
                                                 "line"))

    def plot_data(self):
        for i in range(data_manager.num_growth_files()):
            if not data_manager.get_growth_file(i).visible:
                continue
            xdata, ydata, yerr = data_manager.get_xy_data(i, config['plot']['y_axis']['variable'])
            self.x_title, self.y_title = data_manager.get_titles(i)
            legend_label = data_manager.get_growth_legend(i)

            if(config['data']['growth_average'] is not None):
                growth_plot = self.axes.errorbar(xdata,
                                                 ydata,
                                                 yerr, fmt='-',
                                                 capsize=config['style']['capsize'],
                                                 label=legend_label)
                self.plot_list.append(PlotObject(data_manager.get_growth_file(i),
                                                 growth_plot,
                                                 "errorbar"))
            elif yerr is not None:
                growth_plot = self.axes.plot(xdata, ydata, '-',
                                             label=legend_label)
                fill_area = self.axes.fill_between(xdata, ydata-yerr,
                                                   ydata+yerr, alpha=0.4)
                self.plot_list.append(PlotObject(data_manager.get_growth_file(i),
                                                 [growth_plot, fill_area],
                                                 "fill"))
            else:
                growth_plot = self.axes.plot(xdata, ydata, '-',
                                             label=legend_label)
                self.plot_list.append(PlotObject(data_manager.get_growth_file(i),
                                                 growth_plot,
                                                 "line"))

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
        if config['data']['show_events']:
            for i, data in enumerate(data_manager.get_growth_data_files()):
                for data_event in data.events:
                    event_label = data_event.datetime.strftime(
                        '%d/%m/%Y %H:%M:%S')
                    for lab in data_event.labels:
                        event_label += '\n' + lab
                    self.annotation_names.append(event_label)
                    event_xpos = data_event.get_xpos(config['plot']['x_axis']['variable'])
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
                     (config['fit']['curve'], config['fit']['type']))
        # Find the curve to fit
        fit_index = -1
        for i, dat in enumerate(data_manager.get_growth_data_files()):
            if config['fit']['curve'] == dat.label:
                fit_index = i
        # If the data hasn't been found
        if fit_index == -1:
            return

        fit_x, _, _ = data_manager.get_fit_data(fit_index)
        x_unit, y_unit = data_manager.get_units(fit_index)

        model = get_model(config['fit']['type'], x_unit, y_unit)
        func = model.func()

        fit_result, covm = data_manager.get_fit(fit_index)
        self.axes.plot(fit_x, func(fit_x, *fit_result),
                       '-', color='r', label='Fit')

        bounding_box = dict(boxstyle="round", ec=(
            1., 0.5, 0.5), fc=(1., 0.8, 0.8))
        if config['stats']['show_fit_text']:
            self.axes.text(0.25, 0.95, model.latex,
                           transform=self.axes.transAxes,
                           bbox=bounding_box, picker=True)

        if config['stats']['show_fit_result'] and not config['stats']['show_fit_errors']:
            self.axes.text(0.25, 0.65, model.param_text(fit_result),
                           transform=self.axes.transAxes,
                           bbox=bounding_box, picker=True)

        if config['stats']['show_fit_result'] and config['stats']['show_fit_errors']:
            self.axes.text(0.25, 0.65, model.param_text_error(fit_result, covm),
                           transform=self.axes.transAxes,
                           bbox=bounding_box, picker=True)

        return

    def set_axes_scale(self):
        if(config['plot']['y_axis']['log']):
            self.axes.set_yscale('log')
        else:
            self.axes.set_yscale('linear')
        if(config['plot']['x_axis']['log']):
            self.axes.set_xscale('log')
            self.condition_axes.set_xscale('log')
        else:
            self.axes.set_xscale('linear')
            self.condition_axes.set_xscale('linear')
        if(config['plot']['condition_axis']['log']):
            self.condition_axes.set_yscale('log')
        else:
            self.condition_axes.set_yscale('linear')
        return

    def set_titles(self):
        # Configure axis labels
        self.axes.set_title('')
        if(config['plot']['title'] != ''):
            self.axes.set_title(config['plot']['title'])
        self.axes.set_xlabel(self.x_title)
        self.axes.set_ylabel(self.y_title)
        return

    def set_condition_range(self):
        condition_ymin = self.condition_axes.get_ybound()[0]
        if(config['plot']['condition_axis']['min'] != -1):
            condition_ymin = config['plot']['condition_axis']['min']
        condition_ymax = self.condition_axes.get_ybound()[1]
        if(config['plot']['condition_axis']['max'] != -1):
            condition_ymax = config['plot']['condition_axis']['max']
        self.condition_axes.set_ylim([condition_ymin, condition_ymax])
        return

    def set_axes_ranges(self):
        # Set the axis range
        xmin = self.axes.get_xbound()[0]
        if(config['plot']['x_axis']['min'] != -1):
            xmin = config['plot']['x_axis']['min']
        xmax = self.axes.get_xbound()[1]
        if(config['plot']['x_axis']['max'] != -1):
            xmax = config['plot']['x_axis']['max']
        ymin = self.axes.get_ybound()[0]
        if(config['plot']['y_axis']['min'] != -1):
            ymin = config['plot']['y_axis']['min']
        ymax = self.axes.get_ybound()[1]
        if(config['plot']['y_axis']['max'] != -1):
            ymax = config['plot']['y_axis']['max']
        self.axes.set_xlim([xmin, xmax])
        self.axes.set_ylim([ymin, ymax])
        return

    def set_cursor(self):
        # Control mouse clicking behaviour
        # Create a special cursor that snaps to growth curves
        self.cursor = SnapToCursor(self.axes, self.xdata_list, self.ydata_list,
                                   useblit=False, color='red', linewidth=1)

        # Configure the measurement cursor
        if(config['plot']['cursor']):
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
                closest_i = self.find_closest(
                    self.plot_list, event.xdata, event.ydata, 5)
                if closest_i is not None:
                    self.linewindow = LineStyleWindow(self.plot_list[closest_i].data, self)
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

            if config['data']['show_events']:
                self.mpl_connect('motion_notify_event', onhover)
        return

    def set_plot_styles(self):
        # Apply any saved changes from the line style configuration
        for i, _ in enumerate(self.plot_list):
            self.plot_list[i].set_style()

    def save_plot_styles(self):
        for i, _ in enumerate(self.plot_list):
            self.plot_list[i].save_style()

    def set_legends(self):
        # Switch legend on/off
        if(config['legend']['show']):
            self.legend_on = True
            self.legend_title = config['legend']['title']
            leg = self.axes.legend(title=config['legend']['title'],
                                   loc='upper left')
            leg.set_draggable(True)

        # Toggle condition legend on
        if(config['condition_legend']['show'] and not data_manager.condition_data.empty):
            self.condition_legend_on = True
            self.condition_legend_title = config['condition_legend']['title']
            handles, labels = self.condition_axes.get_legend_handles_labels()
            cond_leg = self.axes.legend(
                handles, labels,
                title=config['condition_legend']['title'], loc='lower right'
            )
            cond_leg.set_draggable(True)
            if(config['legend']['show']):
                self.axes.add_artist(leg)
        return

    # Function to find the closest curve to an x,y point
    def find_closest(self, plots, x, y, limit):
        min_dist = 99999
        # Transform to display coordinates
        x_display, y_display = self.axes.transData.transform_point((x, y))
        closest_i = None
        for i, plot in enumerate(plots):
            xdata_display = np.array([])
            ydata_display = np.array([])
            # Transform all points to display coordinates
            for j, xold in enumerate(plot.plots[0].get_xdata()):
                xnew, ynew = plot.plots[0].axes.transData.transform_point(
                    (xold, plot.plots[0].get_ydata()[j])
                )
                xdata_display = np.append(xdata_display, xnew)
                ydata_display = np.append(ydata_display, ynew)
            dist = np.sqrt(np.power(xdata_display - x_display, 2)
                           + np.power(ydata_display - y_display, 2))
            dist_i = np.argmin(dist)
            distance = dist[dist_i]
            if(distance < min_dist):
                min_dist = distance
                closest_i = i
        if (min_dist > limit):
            return None
        return closest_i

    # Function to save figure through file handler gui
    def save(self):
        save_file(self.fig)
