import numpy as np
from scipy.optimize import curve_fit

# Local includes
from ada.data.data_holder import DataHolder
from ada.data.processor import (process_data, time_average, time_average_arrays,
                                average_data, calculate_gradient, calculate_time_to, get_fit_data_range)
from ada.data.models import get_model
from ada.configuration import config
import ada.options as opt
from ada.logger import logger


# Class to store data files in
class DataManager():

    def __init__(self):
        self.growth_data = DataHolder()
        self.condition_data = DataHolder()
        self.calibration = None

    def clear(self):
        self.growth_data.clear()
        self.condition_data.clear()
        self.calibration = None

    def get_growth_data_files(self):
        return self.growth_data.data_files

    def get_growth_data_labels(self):
        labels = []
        for data in self.growth_data.data_files:
            labels.append(data.label)
        return labels

    def num_growth_files(self):
        return len(self.get_growth_data_files())

    def get_growth_file(self, i):
        return self.growth_data.data_files[i]

    def get_condition_data_files(self):
        return self.condition_data.data_files

    def num_condition_files(self):
        return len(self.get_condition_data_files())

    def get_condition_file(self, i):
        return self.condition_data.data_files[i]

    def get_growth_variables(self):
        variables = []
        if len(self.growth_data.data_files) == 0:
            return variables
        for sig in self.growth_data.data_files[0].signals:
            variables.append(sig.name)
        if self.calibration is not None and 'CD' not in variables:
            variables.append('CD')
        return variables

    def get_condition_variables(self):
        variables = []
        if len(self.condition_data.data_files) == 0:
            return variables
        for sig in self.condition_data.data_files[0].signals:
            variables.append(sig.name)
        return variables

    def get_growth_unit(self, name):
        if len(self.growth_data.data_files) <= 0:
            return ''
        return self.growth_data.data_files[0].get_signal_unit(name)

    def get_condition_unit(self, name):
        if len(self.condition_data.data_files) <= 0:
            return ''
        return self.condition_data.data_files[0].get_signal_unit(name)

    def has_replicates(self, index):
        if len(self.growth_data.replicate_files[index]) > 1:
            return True
        return False

    def num_replicates(self, index):
        return len(self.growth_data.replicate_files[index])

    def get_replicates(self, index):
        return self.growth_data.replicate_files[index]

    def num_condition_replicates(self, index):
        return len(self.condition_data.replicate_files[index])

    def get_replicate_data(self, i, j, xvar, yvar):
        xdata = self.growth_data.replicate_files[i][j].get_xdata(xvar)
        ydata = self.growth_data.replicate_files[i][j].get_ydata(
            yvar, self.calibration)
        return xdata, ydata

    def get_averaged_data(self, xdatas, ydatas, time_window=None, std_err=False):
        xdata = None
        ydata = None
        yerr = None
        # Average replicate data sets over time
        if len(xdatas) > 1 and time_window is not None:
            xdata, ydata, yerr = \
                time_average_arrays(xdatas, ydatas, time_window, std_err)
        # Average replicate data sets for each point
        elif len(xdatas) > 1:
            xdata, ydata, yerr = average_data(xdatas, ydatas, std_err)
        # Average a single data set over time
        elif len(xdatas) == 1 and time_window is not None:
            xdata, ydata, yerr = \
                time_average(xdatas[0], ydatas[0], time_window, std_err)
        # Return the original data set
        elif len(xdatas) == 1:
            xdata = xdatas[0]
            ydata = ydatas[0]
        else:
            raise RuntimeError('No data found')
        return xdata, ydata, yerr

    def get_replicate_xy_data(self, i, signal_name, xvar=None):
        if xvar is None:
            xvar = config['plot']['x_axis']['variable']

        xdatas = []
        ydatas = []
        for rep in self.growth_data.replicate_files[i]:
            xdata = rep.get_xdata(xvar)
            ydata = rep.get_ydata(signal_name, self.calibration)
            xdata, ydata = process_data(xdata, ydata)
            xdatas.append(xdata)
            ydatas.append(ydata)

        return xdatas, ydatas

    def get_xy_data(self, i, signal_name, xvar=None, growth_average=None, std_err=False, ynormlog=False):
        if config['stats']['std_err']:
            std_err = True
        if config['plot']['y_axis']['normlog']:
            ynormlog = True
        if growth_average is None:
            growth_average = config['data']['growth_average']

        xdatas, ydatas = self.get_replicate_xy_data(i, signal_name, xvar)
        xdata, ydata, yerr = self.get_averaged_data(xdatas, ydatas, growth_average, std_err)
        if ynormlog:
            if yerr is not None:
                yerr = yerr/ydata
            ydata = np.log(ydata/ydata[0])

        return xdata, ydata, yerr

    def get_xtitle(self, i, xvar=None, xname=None, xunit=None):
        x_config = config['plot']['x_axis']
        if xvar is None:
            xvar = x_config['variable']
        if xname is None:
            xname = x_config['name']
        if xunit is None:
            xunit = x_config['unit']

        return self.growth_data.data_files[i].get_xtitle(xvar, xname, xunit)

    def get_ytitle(self, i, yvar=None, yname=None, yunit=None, ynormlog=False):
        y_config = config['plot']['y_axis']
        if yvar is None:
            yvar = y_config['variable']
        if yname is None:
            yname = y_config['name']
        if yunit is None:
            yunit = y_config['unit']
        if y_config['normlog']:
            ynormlog = True

        return self.growth_data.data_files[i].get_ytitle(
            yvar, yname, yunit, self.calibration, ynormlog)

    def get_titles(self, i):
        return self.get_xtitle(i), self.get_ytitle(i)

    def get_units(self, i):
        xtitle, ytitle = self.get_titles(i)
        x_unit = ''
        if(len(xtitle.split('[')) > 1):
            x_unit = (xtitle.split('[')[1]).split(']')[0]
        y_unit = ''
        if(len(ytitle.split('[')) > 1):
            y_unit = (ytitle.split('[')[1]).split(']')[0]
        return x_unit, y_unit

    def get_growth_legend(self, i, label_names=None, extra_info=None, only_extra=False):
        if label_names is None:
            label_names = config['legend']['label_names']
        if extra_info is None:
            extra_info = config['legend']['extra_info']
        if config['legend']['only_extra']:
            only_extra = True

        legend_label = label_names[i]
        if(extra_info != 'none' and not only_extra):
            legend_label = (legend_label + ' ('
                            + self.growth_data.data_files[i].get_header_info(extra_info) + ')')
        elif(extra_info != 'none' and only_extra):
            legend_label = self.growth_data.data_files[i].get_header_info(extra_info)
        return legend_label

    def get_condition_xy_data(self, i, cond_name, xvar=None, condition_average=None, std_err=False):
        if xvar is None:
            xvar = config['plot']['x_axis']['variable']
        if condition_average is None:
            condition_average = config['data']['condition_average']
        if config['stats']['std_err']:
            std_err = True

        for j, cond in enumerate(self.condition_data.data_files):
            if self.growth_data.data_files[i].reactor != cond.reactor:
                continue
            if self.growth_data.data_files[i].sub_reactor != cond.sub_reactor:
                continue
            if self.growth_data.data_files[i].date != cond.date:
                continue
            if self.growth_data.data_files[i].time != cond.time:
                continue
            return self.get_condition_data(j, xvar, cond_name, condition_average, std_err)
        raise RuntimeError('No condition data found for %s'
                           % (self.growth_data.data_files[i].name))

    def get_condition_data(self, i, xvar=None, yvar=None, condition_average=None, std_err=False):
        if xvar is None:
            xvar = config['plot']['x_axis']['variable']
        if yvar is None:
            yvar = config['plot']['condition_axis']['variable']
        if condition_average is None:
            condition_average = config['data']['condition_average']
        if config['stats']['std_err']:
            std_err = config['stats']['std_err']

        xdatas = []
        ydatas = []
        for rep in self.condition_data.replicate_files[i]:
            xdata = rep.get_xdata(xvar)
            ydata = rep.get_ydata(yvar)
            xdatas.append(xdata)
            ydatas.append(ydata)
        
        return self.get_averaged_data(xdatas, ydatas, condition_average, std_err)

    def get_condition_ytitle(self, i, yvar=None, yname=None, yunit=None):
        cond_config = config['plot']['condition_axis']
        if yvar is None:
            yvar = cond_config['variable']
        if yname is None:
            yname = cond_config['name']
        if yunit is None:
            yunit = cond_config['unit']

        return self.condition_data.data_files[i].get_ytitle(yvar, yname, yunit)

    def get_condition_legend(self, i, label_names=None, extra_info=None, only_extra=False):
        if label_names is None:
            label_names = config['condition_legend']['label_names']
        if extra_info is None:
            extra_info = config['condition_legend']['extra_info']
        if config['condition_legend']['only_extra']:
            only_extra = True

        # Get the legend label with any extra info specified in
        # the configuration
        legend_label = label_names[i]
        if (extra_info != 'none' and not only_extra):
            legend_label = \
                (legend_label + ' ('
                 + self.condition_data.data_files[i].get_header_info(extra_info)
                 + ')')
        elif (extra_info != 'none' and only_extra):
            legend_label = \
                self.condition_data.data_files[i].get_header_info(extra_info)
        return legend_label

    def get_replicate_gradients(self, i, signal_name, grad_from, grad_to):
        logger.debug('Getting gradient of %s from %.2f to %.2f' %
                     (signal_name, grad_from, grad_to))
        gradients = []
        xdatas, ydatas = self.get_replicate_xy_data(i, signal_name)
        for rep_i, xdata in enumerate(xdatas):
            gradients.append(calculate_gradient(xdata, ydatas[rep_i], grad_from, grad_to))
        return gradients

    def get_gradients(self, signal_name, grad_from, grad_to):
        logger.debug('Getting gradient of %s from %.2f to %.2f' %
                     (signal_name, grad_from, grad_to))
        gradients = []
        for i, _ in enumerate(self.growth_data.data_files):
            xdata, ydata, _ = self.get_xy_data(i, signal_name)
            gradients.append(calculate_gradient(xdata, ydata, grad_from, grad_to))
        return gradients

    def get_replicate_time_to(self, i, signal_name, time_to):
        logger.debug('Getting the time to reach %s of %.2f' %
                     (signal_name, time_to))
        times = []
        xdatas, ydatas = self.get_replicate_xy_data(i, signal_name)
        for rep_i, xdata in enumerate(xdatas):
            times.append(calculate_time_to(xdata, ydatas[rep_i], time_to))
        return times

    def get_time_to(self, signal_name, time_to):
        logger.debug('Getting the time to reach %s of %.2f' %
                     (signal_name, time_to))
        times = []
        for i, _ in enumerate(self.growth_data.data_files):
            xdata, ydata, _ = self.get_xy_data(i, signal_name)
            times.append(calculate_time_to(xdata, ydata, time_to))
            
        return times

    def get_averages(self, cond_name, start_t, end_t):
        logger.debug('Getting average of %s between time %.2f and %.2f' %
                     (cond_name, start_t, end_t))
        averages = []
        errors = []
        for i, _ in enumerate(self.growth_data.data_files):
            xdata, ydata, _ = self.get_condition_xy_data(i, cond_name)
            dat = np.array([])
            for i, x in enumerate(xdata):
                if x >= start_t and x <= end_t:
                    dat = np.append(dat, ydata[i])
            if dat.size == 0:
                averages.append(None)
                errors.append(None)
                continue
            mean = np.mean(dat)
            averages.append(mean)
            if config['stats']['std_err']:
                errors.append(np.std(dat, ddof=1)/np.sqrt(dat.size))
            else:
                errors.append(np.std(dat, ddof=1))
        return averages, errors

    def get_condition_at(self, cond_name, time):
        logger.debug('Getting condition %s at time %.2f' % (cond_name, time))
        values = []
        for i, _ in enumerate(self.growth_data.data_files):
            xdata, ydata, _ = self.get_condition_xy_data(i, cond_name)
            values.append(np.interp(time, xdata, ydata))
        return values

    def get_all_fit_params(self, signal_name, fit_name, fit_from, fit_to, fit_param):
        logger.debug('Fitting %s with %s from %.2f to %.2f and recording %s' % (
            signal_name, fit_name, fit_from, fit_to, fit_param))
        values = []
        errors = []
        for i, _ in enumerate(self.growth_data.data_files):
            fit_result, covm = self.get_fit(
                i, signal_name, fit_name, fit_from, fit_to)
            param_errors = np.sqrt(np.diag(covm))

            model = get_model(fit_name)

            for i, param in enumerate(model.params):
                if param == fit_param:
                    values.append(fit_result[i])
                    errors.append(param_errors[i])
        return values, errors

    def get_fit_data(self, index, signal_name=None, fit_from=None, fit_to=None):
        if signal_name is None:
            signal_name = config['plot']['y_axis']['variable']
        if fit_from is None:
            fit_from = config['fit']['from']
        if fit_to is None:
            fit_to = config['fit']['to']

        fit_x, fit_y, fit_sigma = self.get_xy_data(index, signal_name)
        return get_fit_data_range(fit_x, fit_y, fit_sigma, fit_from, fit_to)

    def get_replicate_fits(self, index, signal_name, fit_name, fit_from, fit_to, fit_param):
        fit_start = None
        if fit_name == 'exponential':
            fit_start = [1, 1./opt.unit_map[config['plot']['x_axis']['variable']]]
        model = get_model(fit_name)
        func = model.func()
        xdatas, ydatas = self.get_replicate_xy_data(index, signal_name)
        values = []
        for rep_i, xdata in enumerate(xdatas):
            fit_x, fit_y, _ = get_fit_data_range(xdata, ydatas[rep_i], None, fit_from, fit_to)
            fit_result, _ = curve_fit(func, fit_x, fit_y, p0=fit_start)
            for i, param in enumerate(model.params):
                if param == fit_param:
                    values.append(fit_result[i])
        return values

    def get_fit(self, index, signal_name=None, fit_name=None, fit_from=None, fit_to=None, fit_start=None, fit_min=None, fit_max=None):
        if signal_name is None:
            signal_name = config['plot']['y_axis']['variable']
        if fit_name is None:
            fit_name = config['fit']['type']
        if fit_from is None:
            fit_from = config['fit']['from']
        if fit_to is None:
            fit_to = config['fit']['to']
        if fit_start is None:
            fit_start = config['fit']['start']
        if fit_min is None:
            fit_min = config['fit']['min']
        if fit_max is None:
            fit_max = config['fit']['max']
            
        bounds = (-np.inf, np.inf)
        if fit_min is not None and fit_min != [] and fit_max is not None and fit_max != []:
            bounds = (fit_min, fit_max)
        if fit_start == []:
            fit_start = None
        if fit_start is None and fit_name == 'exponential':
            fit_start = [1, 1./opt.unit_map[config['plot']['x_axis']['variable']]]

        fit_x, fit_y, fit_sigma = self.get_fit_data(
            index, signal_name, fit_from, fit_to)

        model = get_model(fit_name)
        func = model.func()

        # If there are replicate files then average the data
        if fit_sigma is not None:
            fit_result, covm = curve_fit(func, fit_x, fit_y, sigma=fit_sigma, p0=fit_start, bounds=bounds)
        else:
            fit_result, covm = curve_fit(func, fit_x, fit_y, p0=fit_start, bounds=bounds)

        return fit_result, covm


data_manager = DataManager()
