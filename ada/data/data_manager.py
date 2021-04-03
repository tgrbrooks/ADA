import numpy as np
from scipy.optimize import curve_fit

# Local includes
from ada.data.algae_data import AlgaeData
from ada.data.data_holder import DataHolder
from ada.data.processor import process_data, time_average, average_data
from ada.data.models import get_model
import ada.configuration as config
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

    def num_growth_files(self):
        return len(self.get_growth_data_files())

    def get_condition_data_files(self):
        return self.condition_data.data_files

    def num_condition_files(self):
        return len(self.get_condition_data_files())

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

    def get_replicate_data(self, i, j, xvar, yvar):
        xdata = self.growth_data.replicate_files[i][j].get_xdata(xvar)
        ydata = self.growth_data.replicate_files[i][j].get_ydata(
            yvar, self.calibration)
        return xdata, ydata

    def get_xy_data(self, i, signal_name, xvar=None, std_err=False, ynormlog=False):
        if xvar is None:
            xvar = config.xvar
        if config.std_err:
            std_err = True
        if config.ynormlog:
            ynormlog = True

        xdatas = []
        ydatas = []
        for rep in self.growth_data.replicate_files[i]:
            xdata = rep.get_xdata(xvar)
            ydata = rep.get_ydata(signal_name, self.calibration)
            xdata, ydata = process_data(xdata, ydata)
            xdatas.append(xdata)
            ydatas.append(ydata)
        if len(xdatas) > 1:
            xdata, ydata, yerr = average_data(xdatas, ydatas, std_err)
            if ynormlog:
                yerr = yerr/ydata
                ydata = np.log(ydata/ydata[0])
            return xdata, ydata, yerr
        elif len(xdatas) == 1:
            return xdatas[0], ydatas[0], None
        else:
            raise RuntimeError('No data found')

    def get_xtitle(self, i, xvar=None, xname=None, xunit=None):
        if xvar is None:
            xvar = config.xvar
        if xname is None:
            xname = config.xname
        if xunit is None:
            xunit = config.xunit

        return self.growth_data.data_files[i].get_xtitle(xvar, xname, xunit)

    def get_ytitle(self, i, yvar=None, yname=None, yunit=None, ynormlog=False):
        if yvar is None:
            yvar = config.yvar
        if yname is None:
            yname = config.yname
        if yunit is None:
            yunit = config.yunit
        if config.ynormlog:
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
            label_names = config.label_names
        if extra_info is None:
            extra_info = config.extra_info
        if config.only_extra:
            only_extra = True

        legend_label = label_names[i]
        if(extra_info != 'none' and not only_extra):
            legend_label = (legend_label + ' ('
                            + self.growth_data.data_files[i].get_header_info(extra_info) + ')')
        elif(extra_info != 'none' and only_extra):
            legend_label = self.growth_data.data_files[i].get_header_info(extra_info)
        return legend_label

    def get_condition_xy_data(self, i, cond_name, xvar=None, condition_average=None):
        if xvar is None:
            xvar = config.xvar
        if condition_average is None:
            condition_average = config.condition_average

        for cond in self.condition_data.data_files:
            if self.growth_data.data_files[i].reactor != cond.reactor:
                continue
            if self.growth_data.data_files[i].sub_reactor != cond.sub_reactor:
                continue
            if self.growth_data.data_files[i].date != cond.date:
                continue
            if self.growth_data.data_files[i].time != cond.time:
                continue
            xdata = cond.get_xdata(xvar)
            ydata = cond.get_signal(cond_name)
            if condition_average != -1:
                xdata, ydata, _ = time_average(
                    xdata, ydata, condition_average)
            return xdata, ydata
        raise RuntimeError('No condition data found for %s'
                           % (self.growth_data.data_files[i].name))

    def get_condition_data(self, i, xvar=None, yvar=None, condition_average=None, std_err=False):
        if xvar is None:
            xvar = config.xvar
        if yvar is None:
            yvar = config.condition_yvar
        if condition_average is None:
            condition_average = config.condition_average
        if config.std_err:
            std_err = True

        xdata = self.condition_data.data_files[i].get_xdata(xvar)
        ydata = self.condition_data.data_files[i].get_signal(yvar)
        yerr = None
        # Average condition data over time
        if(condition_average != -1):
            # Do something
            xdata, ydata, yerr = \
                time_average(xdata, ydata, condition_average, std_err)
        return xdata, ydata, yerr

    def get_condition_ytitle(self, i, yvar=None, yname=None, yunit=None):
        if yvar is None:
            yvar = config.condition_yvar
        if yname is None:
            yname = config.condition_yname
        if yunit is None:
            yunit = config.condition_yunit

        return self.condition_data.data_files[i].get_ytitle(yvar, yname, yunit)

    def get_condition_legend(self, i, label_names=None, extra_info=None, only_extra=False):
        if label_names is None:
            label_names = config.condition_label_names
        if extra_info is None:
            extra_info = config.condition_extra_info
        if config.condition_only_extra:
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

    def get_gradients(self, signal_name, grad_from, grad_to):
        logger.debug('Getting gradient of %s from %.2f to %.2f' %
                     (signal_name, grad_from, grad_to))
        gradients = []
        for i, _ in enumerate(self.growth_data.data_files):
            xdata, ydata, _ = self.get_xy_data(i, signal_name)
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

    def get_time_to(self, signal_name, time_to):
        logger.debug('Getting the time to reach %s of %.2f' %
                     (signal_name, time_to))
        times = []
        for i, _ in enumerate(self.growth_data.data_files):
            found = False
            xdata, ydata, _ = self.get_xy_data(i, signal_name)
            for i, ydat in enumerate(ydata):
                if ydat >= time_to:
                    times.append(xdata[i])
                    found = True
                    break
            if not found:
                times.append(None)
        return times

    def get_averages(self, cond_name, start_t, end_t):
        logger.debug('Getting average of %s between time %.2f and %.2f' %
                     (cond_name, start_t, end_t))
        averages = []
        errors = []
        for i, _ in enumerate(self.growth_data.data_files):
            xdata, ydata = self.get_condition_xy_data(i, cond_name)
            dat = np.array([])
            for i, x in enumerate(xdata):
                if x >= start_t and x <= end_t:
                    dat = np.append(dat, ydata[i])
            mean = np.mean(dat)
            averages.append(mean)
            if config.std_err:
                errors.append(np.std(dat, ddof=1)/np.sqrt(dat.size))
            else:
                errors.append(np.std(dat, ddof=1))
        return averages, errors

    def get_condition_at(self, cond_name, time):
        logger.debug('Getting condition %s at time %.2f' % (cond_name, time))
        values = []
        for i, _ in enumerate(self.growth_data.data_files):
            xdata, ydata = self.get_condition_xy_data(i, cond_name)
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
            signal_name = config.yvar
        if fit_from is None:
            fit_from = config.fit_from
        if fit_to is None:
            fit_to = config.fit_to

        fit_x, fit_y, fit_sigma = self.get_xy_data(index, signal_name)

        # Only fit the data in the given range
        if fit_from != fit_to:
            from_index = np.abs(fit_x - fit_from).argmin()
            to_index = np.abs(fit_x - fit_to).argmin()
            fit_x = fit_x[from_index:to_index]
            fit_y = fit_y[from_index:to_index]

        if fit_sigma is not None:
            fit_sigma = fit_sigma[from_index:to_index]

        return fit_x, fit_y, fit_sigma

    def get_fit(self, index, signal_name=None, fit_name=None, fit_from=None, fit_to=None):
        if signal_name is None:
            signal_name = config.yvar
        if fit_name is None:
            fit_name = config.fit_type
        if fit_from is None:
            fit_from = config.fit_from
        if fit_to is None:
            fit_to = config.fit_to

        fit_x, fit_y, fit_sigma = self.get_fit_data(
            index, signal_name, fit_from, fit_to)

        model = get_model(fit_name)
        func = model.func()

        # If there are replicate files then average the data
        if fit_sigma is not None:
            fit_result, covm = curve_fit(func, fit_x, fit_y, sigma=fit_sigma)
        else:
            fit_result, covm = curve_fit(func, fit_x, fit_y)

        return fit_result, covm


data_manager = DataManager()
