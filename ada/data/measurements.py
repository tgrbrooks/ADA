import numpy as np
from scipy.optimize import curve_fit

from ada.data.processor import (process_data, average_data,
                                   time_average)
from ada.data.models import get_model

import ada.configuration as config
import ada.styles as styles
from ada.logger import logger


def get_headings(self):
    logger.debug('Getting the table row headings')
    headings = ['File']
    for data in self.parent.data.data_files:
        headings.append(data.label)
    return headings

def get_profiles(self):
    logger.debug('Getting the data profile names')
    profiles = []
    for data in self.parent.data.data_files:
        profiles.append(data.profile)
    return profiles

def get_reactors(self):
    logger.debug('Getting the reactor names')
    reactors = []
    for data in self.parent.data.data_files:
        reactors.append(data.reactor)
    return reactors

def get_gradients(self, data_name, grad_from, grad_to):
    logger.debug('Getting gradient of %s from %.2f to %.2f' %
                 (data_name, grad_from, grad_to))
    gradients = []
    for i, _ in enumerate(self.parent.data.data_files):
        xdata, ydata, _ = self.get_xy_data(i, data_name)
        # Calculate the gradient
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        for i, ydat in enumerate(ydata):
            if ydat >= grad_from and x1 is None:
                x1 = xdata[i]
                y1 = ydat
            if ydat >= grad_to and x2 is None:
                x2 = xdata[i]
                y2 = ydat
            if x1 is not None and x2 is not None:
                break
        if x1 is None or x2 is None:
            gradients.append(None)
        else:
            gradients.append((y2-y1)/(x2-x1))
    return gradients

def get_time_to(self, data_name, time_to):
    logger.debug('Getting the time to reach %s of %.2f' %
                 (data_name, time_to))
    times = []
    for i, _ in enumerate(self.parent.data.data_files):
        found = False
        xdata, ydata, _ = self.get_xy_data(i, data_name)
        for i, ydat in enumerate(ydata):
            if ydat >= time_to:
                times.append(xdata[i])
                found = True
                break
        if not found:
            times.append(None)
    return times

def get_xy_data(self, i, data_name):
    xdatas = []
    ydatas = []
    for rep in self.parent.data.replicate_files[i]:
        xdata = rep.get_xdata(config.xvar)
        ydata = rep.get_ydata(data_name, self.parent.calibration)
        xdata, ydata = process_data(xdata, ydata)
        xdatas.append(xdata)
        ydatas.append(ydata)
    if len(xdatas) > 1:
        xdata, ydata, yerr = average_data(xdatas, ydatas, config.std_err)
        if config.ynormlog:
            yerr = yerr/ydata
            ydata = np.log(ydata/ydata[0])
        return xdata, ydata, yerr
    elif len(xdatas) == 1:
        return xdatas[0], ydatas[0], None
    else:
        raise RuntimeError('No data found')

def get_averages(self, cond_name, start_t, end_t):
    logger.debug('Getting average of %s between time %.2f and %.2f' %
                 (cond_name, start_t, end_t))
    averages = []
    for i, _ in enumerate(self.parent.data.data_files):
        xdata, ydata = self.get_condition_xy_data(i, cond_name)
        dat = np.array([])
        for i, x in enumerate(xdata):
            if x >= start_t and x <= end_t:
                dat = np.append(dat, ydata[i])
        mean = np.mean(dat)
        averages.append(mean)
    return averages

def get_condition_at(self, cond_name, time):
    logger.debug('Getting condition %s at time %.2f' % (cond_name, time))
    values = []
    for i, _ in enumerate(self.parent.data.data_files):
        xdata, ydata = self.get_condition_xy_data(i, cond_name)
        values.append(np.interp(time, xdata, ydata))
    return values

def get_condition_xy_data(self, i, cond_name):
    for cond in self.parent.condition_data.data_files:
        if self.parent.data.data_files[i].reactor != cond.reactor:
            continue
        if self.parent.data.data_files[i].date != cond.date:
            continue
        if self.parent.data.data_files[i].time != cond.time:
            continue
        xdata = cond.get_xdata(config.xvar)
        ydata = cond.get_signal(cond_name)
        if config.condition_average != -1:
            xdata, ydata, _ = time_average(
                xdata, ydata, config.condition_average)
        return xdata, ydata
    raise RuntimeError('No condition data found for %s'
                       % (self.parent.data.data_files[i].name))

def get_fit(self, data_name, fit_name, fit_param, fit_from, fit_to):
    logger.debug('Fitting %s with %s from %.2f to %.2f and recording %s' % (
        data_name, fit_name, fit_from, fit_to, fit_param))
    values = []
    for i, _ in enumerate(self.parent.data.data_files):
        fit_x, fit_y, fit_sigma = self.get_xy_data(i, data_name)

        # Only fit the data in the given range
        if fit_from != fit_to:
            from_index = np.abs(fit_x - fit_from).argmin()
            to_index = np.abs(fit_x - fit_to).argmin()
            fit_x = fit_x[from_index:to_index]
            fit_y = fit_y[from_index:to_index]

        model = get_model(fit_name, '', '')
        func = model.func()

        # If there are replicate files then average the data
        if fit_sigma is not None:
            fit_sigma = fit_sigma[from_index:to_index]
            fit_result, _ = curve_fit(func, fit_x, fit_y, sigma=fit_sigma)
        else:
            fit_result, _ = curve_fit(func, fit_x, fit_y)

        for i, param in enumerate(model.params):
            if param == fit_param:
                values.append(fit_result[i])
    return values
