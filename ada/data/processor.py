import numpy as np
import random
from math import factorial

import ada.configuration as config
from ada.logger import logger


# Function to apply alignment, outlier removal and smoothing
def process_data(xdata, ydata):
    logger.debug('Processing data')
    # Remove any values <= 0
    if config.remove_zeros:
        xdata, ydata = remove_zeros(xdata, ydata)

    # Align at time 0 if option selected
    if config.align and config.y_alignment == -1:
        xdata = xdata - xdata[0]

    if config.y_alignment != -1:
        xdata = align_to_y(xdata, ydata, config.y_alignment)

    # remove outliers
    if (config.remove_above is not None or
        config.remove_below is not None or
            config.auto_remove):
        xdata, ydata = remove_outliers(xdata, ydata, config.remove_below,
                                       config.remove_above, config.auto_remove, config.outlier_threshold)

    # Smooth the data
    if(config.smooth):
        ydata = savitzky_golay(ydata, config.sg_window_size,
                               config.sg_order, config.sg_deriv, config.sg_rate)
    return xdata, ydata


# Function to remove any zero values
def remove_zeros(xdata, ydata):
    logger.debug('Removing any y=0 points in data')
    data_index = 0
    while data_index < len(ydata):
        if (ydata[data_index] == 0):
            ydata = np.delete(ydata, data_index)
            xdata = np.delete(xdata, data_index)
            data_index = data_index - 1
        data_index = data_index + 1
    return xdata, ydata


# Function to align all plots to the same y value
def align_to_y(xdata, ydata, y_alignment):
    logger.debug('Aligning data to y = %.2f' % y_alignment)
    # Find the first y index greater than the alignment point
    index = 0
    for i, y in enumerate(ydata):
        if y >= y_alignment:
            index = i
            break
    xdata = xdata - xdata[index]
    return xdata


# Function to remove outliers in the data
def remove_outliers(xdata, ydata, min, max, auto, threshold):
    data_index = 0
    while data_index < len(ydata):
        if (max is not None and ydata[data_index] > max):
            ydata = np.delete(ydata, data_index)
            xdata = np.delete(xdata, data_index)
            data_index = data_index - 1
        if (min is not None and ydata[data_index] < min):
            ydata = np.delete(ydata, data_index)
            xdata = np.delete(xdata, data_index)
            data_index = data_index - 1
        data_index = data_index + 1
    # Apply automatic outlier detection
    if(auto):
        logger.debug('Auto-removing outliers')
        # Do this iteratively until no points are removed
        removed_points = 1
        iteration = 0
        while (removed_points != 0):
            logger.debug('')
            removed_points = 0
            # get the average difference between data points
            mean_diff = 0
            for i in range(0, len(ydata)-1, 1):
                mean_diff = mean_diff + abs(ydata[i]-ydata[i+1])
            mean_diff = mean_diff / (len(ydata)-1)
            data_index = 0
            # If the difference to the next point is over 20x the mean,
            # delete the next point
            while data_index < len(ydata)-1:
                if abs(ydata[data_index] - ydata[data_index+1]) > threshold * mean_diff:
                    removed_points += 1
                    ydata = np.delete(ydata, data_index+1)
                    xdata = np.delete(xdata, data_index+1)
                data_index = data_index + 1
            logger.debug('Data %i, iteration %i, removed points = %i' %
                         (data_index, iteration, removed_points))
    return xdata, ydata


# Function to apply savitsky golay smoothing to data from SciPy cookbook
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    logger.debug('Smoothing data')
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window,
                                                           half_window+1)])
    # On windows the first call to linalg gives nans for some reason
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    if np.isnan(m).any():
        m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    y = np.convolve(m[::-1], y, mode='valid')
    return y


# Function to average replicate data sets
def average_data(xdatas, ydatas, show_err=False):
    logger.debug('Averaging data')
    new_xdata = np.array([])
    new_ydata = np.array([])
    new_yerr = np.array([])
    if len(xdatas) <= 1:
        return xdatas[0], ydatas[0], new_yerr
    for i, x_i in enumerate(xdatas[0]):
        ys = np.array([ydatas[0][i]])
        for j in range(1, len(xdatas), 1):
            # Interpolate between points to do average
            ys = np.append(ys, np.interp(x_i, xdatas[j], ydatas[j]))
        mean = np.mean(ys)
        std_dev = np.std(ys, ddof=1)
        if(show_err):
            std_dev = std_dev/np.sqrt(ys.size)
        new_xdata = np.append(new_xdata, x_i)
        new_ydata = np.append(new_ydata, mean)
        new_yerr = np.append(new_yerr, std_dev)
    return new_xdata, new_ydata, new_yerr


# Function to average data over time period
def time_average(xdata, ydata, window, show_err=False):
    logger.debug('Averaging data over time window of %i' % window)
    new_xdata = np.array([])
    new_ydata = np.array([])
    new_yerr = np.array([])
    w_i = 1
    i = 0
    while(i < len(xdata)):
        data_x = np.array([])
        data_y = np.array([])
        while(i < len(xdata) and xdata[i] < w_i * window):
            data_x = np.append(data_x, xdata[i])
            data_y = np.append(data_y, ydata[i])
            i = i + 1
        if(data_y.size == 0):
            w_i = w_i + 1
            continue
        mean_x = np.mean(data_x)
        mean_y = np.mean(data_y)
        std_dev = np.std(data_y, ddof=1)
        if(show_err):
            std_dev = std_dev/np.sqrt(data_y.size)
        new_xdata = np.append(new_xdata, mean_x)
        new_ydata = np.append(new_ydata, mean_y)
        if(data_y.size == 1):
            new_yerr = np.append(new_yerr, 0)
        else:
            new_yerr = np.append(new_yerr, std_dev)
        w_i = w_i + 1
    return new_xdata, new_ydata, new_yerr

# Function to average arrays of data over time period
def time_average_arrays(xdatas, ydatas, window, show_err=False):
    logger.debug('Averaging data over time window of %i' % window)
    new_xdata = np.array([])
    new_ydata = np.array([])
    new_yerr = np.array([])
    w_i = 1
    data_remaining = True
    while data_remaining:
        window_x = np.array([])
        window_y = np.array([])
        finished = True
        for i, xdata in enumerate(xdatas):
            # Check if there's any data in the next window
            if len(xdata[xdata >= (w_i) * window]) > 0:
                finished = False
            mask = ((xdata >= (w_i - 1) * window) & (xdata < w_i * window))
            window_x = np.append(window_x, xdata[mask])
            window_y = np.append(window_y, ydatas[i][mask])
        if finished:
            data_remaining = False
        if(window_y.size == 0):
            w_i = w_i + 1
            continue
        mean_x = np.mean(window_x)
        mean_y = np.mean(window_y)
        std_dev = np.std(window_y, ddof=1)
        if(show_err):
            std_dev = std_dev/np.sqrt(window_y.size)
        new_xdata = np.append(new_xdata, mean_x)
        new_ydata = np.append(new_ydata, mean_y)
        if(window_y.size == 1):
            new_yerr = np.append(new_yerr, 0)
        else:
            new_yerr = np.append(new_yerr, std_dev)
        w_i = w_i + 1
    return new_xdata, new_ydata, new_yerr


def get_exponent(value):
    return np.floor(np.log10(np.abs(value))).astype(int)


# Function to write big numbers prettily
def exponent_text(value):
    exponent = get_exponent(value)
    if exponent >= 0 and exponent <= 2:
        text = '%.*f' % (config.sig_figs, value)
        return text
    value = value/(1.*10.**exponent)
    text = r'%.*f$\times10^{%i}$' % (config.sig_figs, value, exponent)
    return text


# Function to write big numbers prettily (with errors!)
def exponent_text_errors(value, error):
    exponent = get_exponent(value)
    if exponent >= 0 and exponent <= 2:
        text = '%.*f ($\pm$%.*f)' % (config.sig_figs,
                                     value, config.sig_figs, error)
        return text
    value = value/(1.*10.**exponent)
    error = error/(1.*10.**exponent)
    text = r'%.*f ($\pm$%.*f)$\times10^{%i}$' % (config.sig_figs,
                                                 value, config.sig_figs, error, exponent)
    return text
