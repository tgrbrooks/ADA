import unittest
import sys
import os
from datetime import datetime, date, time
import math
import numpy as np

from ada.reader.read_algem_pro import read_algem_pro
from ada.reader.read_calibration import read_calibration
from ada.data.algae_data import AlgaeData
from ada.data.data_holder import DataHolder
from ada.data.models import get_model
from ada.data.processor import (
    align_to_y, remove_outliers, savitzky_golay, average_data,
    time_average, time_average_arrays, get_exponent, exponent_text, exponent_text_errors)
from ada.data.data_manager import DataManager


class DataTest(unittest.TestCase):

    def setUp(self):
        self.data = read_algem_pro('test/files/Algem-Pro/500.txt')
        self.calib = read_calibration('test/files/calibration.csv')
        data_holder = DataHolder()
        data_holder.add_data(self.data)
        self.manager = DataManager()
        self.manager.growth_data = data_holder
        self.manager.condition_data = data_holder

    # ====== data/algae_data.py ========
    def test_algae_data_constructor(self):
        empty = AlgaeData('name.txt')
        self.assertEqual(empty.label, 'name', 'Incorrect label')
        self.assertEqual(empty.date, date(1994, 3, 16),
                         'Incorrect initial date')
        self.assertEqual(empty.time, time(0, 0, 0), 'Incorrect initial time')

    def test_algae_data_header_info(self):
        self.assertEqual(self.data.get_header_info('date'),
                         '16/01/2018', 'Incorrect date string')
        self.assertEqual(self.data.get_header_info('time'),
                         '18:51:24', 'Incorrect time string')
        self.assertEqual(self.data.get_header_info('date+time'),
                         '16/01/2018, 18:51:24', 'Incorrect date+time string')
        self.assertEqual(self.data.get_header_info(
            'title'), 'testing_c1', 'Incorrect title')
        self.assertEqual(self.data.get_header_info(
            'reactor'), '12982A', 'Incorrect reactor')
        self.assertEqual(self.data.get_header_info('profile'),
                         '30_500_nm', 'Incorrect profile')
        self.assertEqual(self.data.get_header_info(''),
                         None, 'Incorrect empty value')

    def test_algae_data_getters(self):
        # Signal
        self.assertEqual(len(self.data.get_signal('OD')),
                         427, 'Incorrect signal')
        with self.assertRaises(RuntimeError):
            self.data.get_signal('none')
        self.assertEqual(self.data.get_signal_unit(
            'OD'), 'Numeric', 'Incorrect signal unit')
        # X data
        self.assertEqual(len(self.data.get_xdata('seconds')),
                         427, 'Incorrect xdata')
        self.assertEqual(self.data.get_xdata('none'), None, 'Incorrect xdata')
        self.assertEqual(self.data.get_xtitle(
            'seconds', '', ''), 'Time [sec]', 'Incorrect xtitle')
        self.assertEqual(self.data.get_xtitle(
            'hour', '', 'none'), 'Time', 'Incorrect xtitle')
        self.assertEqual(self.data.get_xtitle(
            'minutes', 'name', 'unit'), 'name [unit]', 'Incorrect xtitle')
        # Y data
        self.assertEqual(len(self.data.get_ydata('OD')),
                         427, 'Incorrect ydata')
        with self.assertRaises(RuntimeError):
            self.data.get_ydata('none')
        self.assertEqual(len(self.data.get_ydata('CD', self.calib)),
                         427, 'Incorrect ydata with calibration')
        self.assertEqual(self.data.get_ytitle('OD', '', ''),
                         'OD [Numeric]', 'Incorrect ytitle')
        self.assertEqual(self.data.get_ytitle(
            'OD', '', 'none'), 'OD', 'Incorrect ytitle')
        self.assertEqual(self.data.get_ytitle(
            'OD', 'name', 'unit'), 'name [unit]', 'Incorrect ytitle')
        self.assertEqual(self.data.get_ytitle(
            'CD', '', '', self.calib), 'CD', 'Incorrect ytitle')
        self.assertEqual(self.data.get_ytitle(
            'CD', 'name', 'unit', self.calib), 'name [unit]', 'Incorrect ytitle')
        self.assertEqual(self.data.get_ytitle(
            'OD', '', '', None, True), 'ln(OD/OD$_{0}$)', 'Incorrect ytitle')
        self.assertEqual(self.data.get_ytitle(
            'OD', 'name', 'unit', None, True), 'name [unit]', 'Incorrect ytitle')

    # ====== data/calibration_data.py ========
    def test_calibration_data(self):
        self.assertEqual(len(self.calib.calibrate_od(
            self.data.get_signal('OD'))), 427)

    # ====== data/data_holder.py ========
    def test_data_holder(self):
        data_holder = DataHolder()
        self.assertEqual(len(data_holder.data_files), 0)
        self.assertEqual(len(data_holder.replicate_files), 0)
        self.assertEqual(data_holder.empty, True)
        data_holder.add_data(self.data)
        self.assertEqual(len(data_holder.data_files), 1)
        self.assertEqual(len(data_holder.replicate_files), 1)
        self.assertEqual(len(data_holder.replicate_files[0]), 1)
        data_holder.add_replicate(self.data, 0)
        self.assertEqual(len(data_holder.replicate_files), 1)
        self.assertEqual(len(data_holder.replicate_files[0]), 2)
        self.assertEqual(data_holder.empty, False)
        self.assertEqual(data_holder.get_profiles(), ['30_500_nm'])
        self.assertEqual(data_holder.get_reactors(), ['12982A'])
        data_holder.delete_replicate(0, 1)
        self.assertEqual(len(data_holder.replicate_files[0]), 1)
        data_holder.delete_data(0)
        self.assertEqual(len(data_holder.data_files), 0)
        self.assertEqual(len(data_holder.replicate_files), 0)
        self.assertEqual(data_holder.empty, True)
        data_holder.add_data(self.data)
        data_holder.clear()
        self.assertEqual(len(data_holder.data_files), 0)
        self.assertEqual(len(data_holder.replicate_files), 0)
        self.assertEqual(data_holder.empty, True)

    # ====== data/models.py ========
    def test_models(self):
        with self.assertRaises(RuntimeError):
            get_model('none')
        model = get_model('flat line', 'xunit', 'yunit')
        func = model.func()
        self.assertEqual(func([2], 4), 4)
        self.assertEqual(model.param_text([4]), '$p$ = 4.00 yunit')
        self.assertEqual(model.param_text_error(
            [4], [1]), '$p$ = 4.00 ($\pm$1.00) yunit')
        self.assertEqual(model.get_latex_param('Y intercept (p)'), '$p$')
        self.assertEqual(model.get_units('Y intercept (p)'), 'yunit')
        model = get_model('linear')
        func = model.func()
        self.assertEqual(func([2], 4, 4), 12)
        model = get_model('quadratic')
        func = model.func()
        self.assertEqual(func([2], 4, 4, 4), 28)
        model = get_model('exponential')
        func = model.func()
        self.assertEqual(math.floor(func([2], 4, 2)), 218)
        model = get_model('zweitering')
        func = model.func()
        self.assertEqual(math.floor(func([2], 0, 40, 0.4, 4)), 4)

    # ====== data/processor.py ========
    def test_align_to_y(self):
        xdata = np.array([0, 1, 2, 3, 4, 5, 6])
        ydata = np.array([0, 1, 2, 3, 4, 5, 6])
        newx = align_to_y(xdata, ydata, 2)
        self.assertEqual(newx[0], -2)

    def test_remove_outliers(self):
        xdata = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ydata = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 30])
        newx, newy = remove_outliers(xdata, ydata, 2, 6, False, 0)
        self.assertEqual(len(newx), 5)
        self.assertEqual(len(newy), 5)
        newx, newy = remove_outliers(xdata, ydata, None, None, True, 5)
        self.assertEqual(len(newx), 9)
        self.assertEqual(len(newy), 9)

    def test_average_data(self):
        xdata = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ydata_1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ydata_2 = np.array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
        newx, newy, err = average_data([xdata, xdata], [ydata_1, ydata_2])
        self.assertEqual(newx[0], 0)
        self.assertEqual(newy[0], 4.5)
        self.assertAlmostEqual(err[0], 6.36, 2)
        self.assertEqual(newx[4], 4)
        self.assertEqual(newy[4], 4.5)
        self.assertAlmostEqual(err[4], 0.71, 2)
        newx, newy, err = average_data(
            [xdata, xdata], [ydata_1, ydata_2], True)
        self.assertAlmostEqual(err[0], 4.50, 2)
        self.assertAlmostEqual(err[4], 0.50, 2)

    def test_time_average(self):
        xdata = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ydata = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        newx, newy, err = time_average(xdata, ydata, 2)
        self.assertEqual(newx[0], 0.5)
        self.assertEqual(newy[0], 0.5)
        self.assertAlmostEqual(err[0], 0.71, 2)
        self.assertEqual(newx[4], 8.5)
        self.assertEqual(newy[4], 8.5)
        self.assertAlmostEqual(err[4], 0.71, 2)
        newx, newy, err = time_average(xdata, ydata, 2, True)
        self.assertAlmostEqual(err[0], 0.50, 2)
        self.assertAlmostEqual(err[4], 0.50, 2)

    def test_time_average_array(self):
        xdata1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ydata1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        xdata2 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        ydata2 = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        xdatas = [xdata1, xdata2]
        ydatas = [ydata1, ydata2]
        newx, newy, err = time_average_arrays(xdatas, ydatas, 2)
        self.assertEqual(newx[0], 0.5)
        self.assertEqual(newy[0], 5.5)
        self.assertAlmostEqual(err[0], 5.80, 2)
        self.assertEqual(newx[4], 8.5)
        self.assertEqual(newy[4], 13.5)
        self.assertAlmostEqual(err[4], 5.80, 2)
        newx, newy, err = time_average_arrays(xdatas, ydatas, 2, True)
        self.assertAlmostEqual(err[0], 2.90, 2)
        self.assertAlmostEqual(err[4], 2.90, 2)

    def test_get_exponent(self):
        self.assertEqual(get_exponent(100), 2)

    def test_exponent_text(self):
        self.assertEqual(exponent_text(2000), r'2.00$\times10^{3}$')

    def test_exponent_text_errors(self):
        self.assertEqual(exponent_text_errors(2000, 100),
                         r'2.00 ($\pm$0.10)$\times10^{3}$')

    # ====== data/data_manager.py ========
    def test_get_growth_variables(self):
        self.assertEqual(self.manager.get_growth_variables(), ['OD'])

    def test_get_growth_unit(self):
        self.assertEqual(self.manager.get_growth_unit('OD'), 'Numeric')

    def test_has_replicates(self):
        self.assertEqual(self.manager.has_replicates(0), False)

    def test_num_replicates(self):
        self.assertEqual(self.manager.num_replicates(0), 1)

    def test_get_replicate_data(self):
        xdata, ydata = self.manager.get_replicate_data(0, 0, 'seconds', 'OD')
        self.assertEqual(xdata[4], 5401)
        self.assertEqual(ydata[4], 0.106)

    def test_get_xy_data(self):
        xdata, ydata, err = self.manager.get_xy_data(0, 'OD')
        self.assertEqual(xdata[4], 5401)
        self.assertEqual(ydata[4], 0.106)
        self.assertEqual(err, None)

    def test_get_titles(self):
        self.assertEqual(self.manager.get_titles(0), ('Time [s]', ''))

    def test_get_units(self):
        self.assertEqual(self.manager.get_units(0), ('s', ''))

    def test_get_growth_legend(self):
        self.assertEqual(self.manager.get_growth_legend(0, ['500']), '500')

    def test_get_condition_xy_data(self):
        xdata, ydata, _ = self.manager.get_condition_xy_data(0, 'OD')
        self.assertEqual(xdata[4], 5401)
        self.assertEqual(ydata[4], 0.106)

    def test_get_condition_data(self):
        xdata, ydata, err = self.manager.get_condition_data(0, yvar='OD')
        self.assertEqual(xdata[4], 5401)
        self.assertEqual(ydata[4], 0.106)
        self.assertEqual(err, None)

    def test_get_condition_ytitle(self):
        self.assertEqual(self.manager.get_condition_ytitle(
            0, 'OD'), 'OD [Numeric]')

    def test_get_condition_legend(self):
        self.assertEqual(self.manager.get_condition_legend(0, ['500']), '500')

    def test_get_gradients(self):
        gradients = self.manager.get_gradients('OD', 0.1, 0.2)
        self.assertAlmostEqual(gradients[0], 6.85E-7, 2)
        self.assertEqual(self.manager.get_gradients('OD', 8, 9), [None])

    def test_get_time_to(self):
        time_to = self.manager.get_time_to('OD', 0.2)
        self.assertEqual(time_to[0], 138601)
        self.assertEqual(self.manager.get_time_to('OD', 8), [None])

    def test_get_averages(self):
        averages, error = self.manager.get_averages('OD', 100000, 200000)
        self.assertAlmostEqual(averages[0], 0.22, 2)
        self.assertAlmostEqual(error[0], 0.04, 2)
        self.assertEqual(self.manager.get_averages(
            'OD', 10000000, 20000000), ([None], [None]))

    def test_get_condition_at(self):
        condition_at = self.manager.get_condition_at('OD', 200000)
        self.assertAlmostEqual(condition_at[0], 0.31, 2)

    def test_get_all_fit_params(self):
        fit_params, error = self.manager.get_all_fit_params(
            'OD', 'linear', 100000, 200000, 'Gradient (p1)')
        self.assertAlmostEqual(fit_params[0], 1.41E-6, 2)
        self.assertAlmostEqual(error[0], 3.39E-8, 2)

    def test_get_fit_data(self):
        fit_x, fit_y, fit_sigma = self.manager.get_fit_data(
            0, 'OD', 100000, 200000)
        self.assertEqual(len(fit_x), 55)
        self.assertEqual(len(fit_y), 55)
        self.assertEqual(fit_sigma, None)

    def test_get_fit(self):
        fit_result, _ = self.manager.get_fit(
            0, 'OD', 'flat line', 100000, 200000)
        self.assertAlmostEqual(fit_result[0], 0.22, 2)
        fit_result, _ = self.manager.get_fit(0, 'OD', 'linear', 100000, 200000)
        self.assertAlmostEqual(fit_result[0], 6.95E-3, 2)
        self.assertAlmostEqual(fit_result[1], 1.41E-6, 2)
        fit_result, _ = self.manager.get_fit(
            0, 'OD', 'quadratic', 100000, 200000)
        self.assertAlmostEqual(fit_result[0], 0.13, 2)
        self.assertAlmostEqual(fit_result[1], -2.78E-7, 2)
        self.assertAlmostEqual(fit_result[2], 5.64E-12, 2)
        fit_result, _ = self.manager.get_fit(
            0, 'OD', 'exponential', 0, 200000, fit_start=[1, 0.00001])
        self.assertAlmostEqual(fit_result[0], 0.09, 2)
        self.assertAlmostEqual(fit_result[1], 1.00E-3, 2)
        fit_result, _ = self.manager.get_fit(0, 'OD', 'zweitering')
        self.assertAlmostEqual(fit_result[0], 0.11, 2)
        self.assertAlmostEqual(fit_result[1], 1.61, 2)
        self.assertAlmostEqual(fit_result[2], 1.27, 2)
        self.assertAlmostEqual(fit_result[3], 2.42, 2)


if __name__ == '__main__':
    print(sys.path)
    unittest.main()
