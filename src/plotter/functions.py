import numpy as np
import random
from math import factorial


# Function to apply alignment, outlier removal and smoothing
def process_data(xdata, ydata, config):
    # Remove any values <= 0
    xdata, ydata = remove_zeros(xdata, ydata)

    # Align at time 0 if option selected
    if config.align and config.y_alignment == -1:
        xdata = xdata - xdata[0]

    if config.y_alignment != -1:
        xdata = align_to_y(xdata, ydata, config)

    # remove outliers
    if (config.remove_above >= 0 or
            config.remove_below >= 0 or
            config.auto_remove):
        xdata, ydata = remove_outliers(xdata, ydata, config)

    # Smooth the data
    if(config.smooth):
        ydata = savitzky_golay(ydata, 61, 0)
    return xdata, ydata


# Function to remove any values <= 0
def remove_zeros(xdata, ydata):
    data_index = 0
    while data_index < len(ydata):
        if (ydata[data_index] <= 0):
            ydata = np.delete(ydata, data_index)
            xdata = np.delete(xdata, data_index)
            data_index = data_index - 1
        data_index = data_index + 1
    return xdata, ydata

# Function to align all plots to the same y value
def align_to_y(xdata, ydata, config):
    # Find the first y index greater than the alignment point
    index = 0
    for i, y in enumerate(ydata):
        if y >= config.y_alignment:
            index = i
            break
    xdata = xdata - xdata[index]
    return xdata


# Function to remove outliers in the data
def remove_outliers(xdata, ydata, config):
    data_index = 0
    while data_index < len(ydata):
        if (config.remove_above >= 0 and
                ydata[data_index] > config.remove_above):
            ydata = np.delete(ydata, data_index)
            xdata = np.delete(xdata, data_index)
            data_index = data_index - 1
        if (config.remove_below >= 0 and
                ydata[data_index] < config.remove_below):
            ydata = np.delete(ydata, data_index)
            xdata = np.delete(xdata, data_index)
            data_index = data_index - 1
        data_index = data_index + 1
    # Apply automatic outlier detection
    if(config.auto_remove):
        # get the average difference between data points
        mean_diff = 0
        for i in range(0, len(ydata)-1, 1):
            mean_diff = mean_diff + abs(ydata[i]-ydata[i+1])
        mean_diff = mean_diff / (len(ydata)-1)
        data_index = 0
        # If the difference to the next point is over 20x the mean,
        # delete the next point
        while data_index < len(ydata)-1:
            if abs(ydata[data_index] - ydata[data_index+1]) > 20.*mean_diff:
                ydata = np.delete(ydata, data_index+1)
                xdata = np.delete(xdata, data_index+1)
            data_index = data_index + 1
    return xdata, ydata


# Function to apply savitsky golay smoothing to data from SciPy cookbook
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
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window,
                                                           half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


# Function to average replicate data sets
def average_data(xdatas, ydatas, show_err=False):
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
        if(show_err):
            std_dev = std_dev/np.sqrt(ys.size)
        new_xdata = np.append(new_xdata, x_i)
        new_ydata = np.append(new_ydata, mean)
        new_yerr = np.append(new_yerr, std_dev)
    return new_xdata, new_ydata, new_yerr


# Function to average data over time period
def time_average(xdata, ydata, window, show_err=False):
    new_xdata = np.array([])
    new_ydata = np.array([])
    new_yerr = np.array([])
    w_i = 1
    i = 0
    while(i < len(xdata)):
        data = np.array([])
        while(i < len(xdata) and xdata[i] < w_i*window):
            data = np.append(data, ydata[i])
            i = i + 1
        mean = np.mean(data)
        std_dev = np.std(data, ddof=1)
        if(show_err):
            std_dev = std_dev/np.sqrt(data.size)
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


# Function to find nearest index in numpy array
def exponent_text(value):
    exponent = np.floor(np.log10(np.abs(value))).astype(int)
    if exponent >= 0 and exponent <= 2:
        text = '%1.2f' % (value)
        return text
    value = value/(1.*10.**exponent)
    text = r'%1.2f$\times10^{%i}$' % (value, exponent)
    return text
