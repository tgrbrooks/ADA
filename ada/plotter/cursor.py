from matplotlib.widgets import AxesWidget
import matplotlib.pyplot as plt
import numpy as np

import ada.configuration as config


class Cursor(AxesWidget):

    def __init__(self, ax, horizOn=True, vertOn=True, useblit=False,
                 **lineprops):
        AxesWidget.__init__(self, ax)

        self.connect_event('motion_notify_event', self.onmove)
        self.connect_event('draw_event', self.clear)

        self.visible = True
        self.horizOn = horizOn
        self.vertOn = vertOn
        self.useblit = useblit and self.canvas.supports_blit

        if self.useblit:
            lineprops['animated'] = True
        self.lineh = ax.axhline(ax.get_ybound()[0], visible=False, **lineprops)
        self.linev = ax.axvline(ax.get_xbound()[0], visible=False, **lineprops)

        self.background = None
        self.needclear = False

    def clear(self, event):
        """Internal event handler to clear the cursor."""
        if self.ignore(event):
            return
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.linev.set_visible(False)
        self.lineh.set_visible(False)

    def onmove(self, event):
        """Internal event handler to draw the cursor when the mouse moves."""
        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            return
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True
        if not self.visible:
            return
        self.linev.set_xdata((event.xdata, event.xdata))

        self.lineh.set_ydata((event.ydata, event.ydata))
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        self._update()

    def _update(self):
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.linev)
            self.ax.draw_artist(self.lineh)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
        return False


class SnapToCursor(AxesWidget):
    """
    Like Cursor but the crosshair snaps to the nearest x, y point.
    For simplicity, this assumes that *x* is sorted.
    """

    def __init__(self, ax, x, y, horizOn=True, vertOn=True, useblit=False,
                 **lineprops):
        AxesWidget.__init__(self, ax)

        self.connect_event('motion_notify_event', self.onmove)
        self.connect_event('button_press_event', self.onclick)
        self.connect_event('draw_event', self.clear)

        self.visible = True
        self.horizOn = horizOn
        self.vertOn = vertOn
        self.useblit = useblit and self.canvas.supports_blit

        if self.useblit:
            lineprops['animated'] = True
        self.lineh = ax.axhline(ax.get_ybound()[0], visible=False, **lineprops)
        self.linev = ax.axvline(ax.get_xbound()[0], visible=False, **lineprops)

        self.marker, = ax.plot(0, 0, marker='o', visible=False,
                               color='red', markersize=4)

        self.background = None
        self.needclear = False

        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.25, 0.95, '', transform=ax.transAxes,
                           bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5),
                                     fc=(1., 0.8, 0.8)))
        self.gradtxt = ax.text(0.25, 0.8, '', transform=ax.transAxes,
                               bbox=dict(boxstyle="round", ec=(1., 0.5, 0.5),
                                         fc=(1., 0.8, 0.8)))
        self.positions = []
        self.lines = []

    def clear(self, event):
        """Internal event handler to clear the cursor."""
        if self.ignore(event):
            return
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.linev.set_visible(False)
        self.lineh.set_visible(False)

    def onmove(self, event):
        """Internal event handler to draw the cursor when the mouse moves."""
        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            return
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True
        if not self.visible:
            return

        x, y = event.xdata, event.ydata
        indx = min(np.searchsorted(self.x[0], x), len(self.x[0]) - 1)
        min_dist = np.sqrt((self.x[0][indx] - x)**2.
                           + (self.y[0][indx] - y)**2.)
        min_ind = 0
        for ind, _ in enumerate(self.x):
            index_x = min(np.searchsorted(self.x[ind], x),
                          len(self.x[ind]) - 1)
            dist = np.sqrt((self.x[ind][index_x] - x)**2.
                           + (self.y[ind][index_x] - y)**2.)
            if(dist < min_dist):
                indx = index_x
                min_ind = ind
        x = self.x[min_ind][indx]
        y = self.y[min_ind][indx]

        self.linev.set_xdata((x, x))
        self.lineh.set_ydata((y, y))
        self.marker.set_xdata(x)
        self.marker.set_ydata(y)
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)
        self.marker.set_visible(self.visible)

        self.txt.set_text('x: %1.2f | y: %1.2f' % (x, y))

        self._update()

    def onclick(self, event):
        x, y = event.xdata, event.ydata
        indx = min(np.searchsorted(self.x[0], x), len(self.x[0]) - 1)
        min_dist = np.sqrt((self.x[0][indx] - x)**2.
                           + (self.y[0][indx] - y)**2.)
        min_ind = 0
        for ind, _ in enumerate(self.x):
            index_x = min(np.searchsorted(self.x[ind], x),
                          len(self.x[ind]) - 1)
            dist = np.sqrt((self.x[ind][index_x] - x)**2.
                           + (self.y[ind][index_x] - y)**2.)
            if(dist < min_dist):
                indx = index_x
                min_ind = ind
        x = self.x[min_ind][indx]
        y = self.y[min_ind][indx]
        position = self.ax.plot(x, y, marker='o', visible=True,
                                color='red', markersize=4)

        # Delete old measurement
        if(len(self.positions) >= 2):
            for pos in self.positions:
                p = pos.pop(0)
                p.remove()
                del p
            self.positions.clear()
            for line in self.lines:
                L = line.pop(0)
                L.remove()
                del L
            self.lines.clear()
        # Draw line between points
        elif(len(self.positions) == 1):
            pos1 = self.positions[0]
            x_points = np.array([pos1[0].get_xdata()[0], x])
            y_points = np.array([pos1[0].get_ydata()[0], y])
            line = self.ax.plot(x_points, y_points, 'r-')
            self.lines.append(line)
            gradient = (y_points[1] - y_points[0])/(x_points[1] - x_points[0])
            exponent = np.floor(np.log10(np.abs(gradient))).astype(int)
            gradient = gradient/(1.*10.**exponent)

            x_label = self.ax.xaxis.get_label().get_text()
            x_unit = ''
            if(len(x_label.split('[')) > 1):
                x_unit = (x_label.split('[')[1]).split(']')[0]
            y_label = self.ax.yaxis.get_label().get_text()
            y_unit = ''
            if(len(y_label.split('[')) > 1):
                y_unit = (y_label.split('[')[1]).split(']')[0]
            grad_unit = y_unit + "/" + x_unit
            self.gradtxt.set_text(r'grad = %.*f$\times10^{%i}$ %s'
                                  % (config.sig_figs, gradient, exponent, grad_unit))

        self.positions.append(position)

    def _update(self):
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.linev)
            self.ax.draw_artist(self.lineh)
            self.ax.draw_artist(self.marker)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
        return False
