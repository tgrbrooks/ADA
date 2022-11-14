# pyqt5 imports
from PyQt5.QtWidgets import QSizePolicy

# maplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Local imports
from gui.file_handler import save_file

import configuration as config
from logger import logger


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

    def plot(self, plot_config=None):
        logger.debug('Creating correlation plot')

        self.axes.clear()
        if plot_config is None:
            return

        self.scatter = self.axes.scatter(
            plot_config.x_data, plot_config.y_data, alpha=0)
        self.errbar = self.axes.errorbar(
            plot_config.x_data, plot_config.y_data, plot_config.y_error, plot_config.x_error, '.')
        if plot_config is not None:
            self.axes.set_title(plot_config.title)
            self.axes.set_xlabel(plot_config.x_title)
            self.axes.set_ylabel(plot_config.y_title)

            bounding_box = dict(boxstyle="round", ec=(
                1., 0.5, 0.5), fc=(1., 0.8, 0.8))
            if plot_config.correlation_coeff is not None:
                text = ('$\\rho$ = %.*f' %
                        (config.sig_figs, plot_config.correlation_coeff))
                self.axes.text(0.25, 0.95, text,
                               transform=self.axes.transAxes,
                               bbox=bounding_box, picker=True)

            self.label_annotation = self.axes.annotate('',
                                                       xy=(0, 0),
                                                       xytext=(0.2, 0.2),
                                                       textcoords='axes fraction',
                                                       bbox=dict(
                                                           boxstyle="round", fc="w"),
                                                       arrowprops=dict(arrowstyle="->"))
            self.label_annotation.set_visible(False)

            def update_annotation(ind):
                label_pos = self.scatter.get_offsets()[ind["ind"][0]]
                self.label_annotation.xy = label_pos
                label_text = plot_config.labels[ind["ind"][0]]
                self.label_annotation.set_text(label_text)

            def onhover(event):
                vis = self.label_annotation.get_visible()
                cont = None
                if event.inaxes == self.axes:
                    cont, ind = self.scatter.contains(event)
                if cont:
                    update_annotation(ind)
                    self.label_annotation.set_visible(True)
                    self.draw_idle()
                else:
                    if vis:
                        self.label_annotation.set_visible(False)
                        self.draw_idle()

            if len(plot_config.labels) > 0:
                self.mpl_connect('motion_notify_event', onhover)

        self.draw()
        return

    # Function to save figure through file handler gui
    def save(self):
        save_file(self.fig)
