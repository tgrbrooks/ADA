import unittest
import sys
import os
from datetime import datetime, date, time

from ada.reader.read_algem_pro import read_algem_pro
from ada.reader.read_ada import read_ada
from ada.reader.read_algem_ht24 import read_algem_ht24, read_algem_ht24_details
from ada.reader.read_algem_ht24_txt import read_algem_ht24_txt
from ada.reader.read_ip import read_ip
from ada.reader.read_psi import read_psi
from ada.reader.read_calibration import read_calibration


class ReaderTest(unittest.TestCase):
    # ====== reader/read_algem_pro.py ========
    def test_read_algem_pro(self):
        data = read_algem_pro('test/files/Algem-Pro/150.txt')
        # Header information
        self.assertEqual(data.label, '150', 'Incorrect label read')
        self.assertEqual(data.date, date(2018, 1, 16), 'Incorrect date read')
        self.assertEqual(data.time, time(18, 51, 12), 'Incorrect time read')
        self.assertEqual(data.reactor, '13134B', 'Incorrect reactor read')
        self.assertEqual(data.profile, '20_150_light_c1',
                         'Incorrect profile read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 426, 'Incorrect x data read')
        self.assertEqual(len(data.signals), 1, 'Incorrect y data read')

    # ====== reader/read_ada.py ========
    def test_read_ada(self):
        data, conditions = read_ada('test/files/ADA/IP_T-Iso.csv')
        # Header information
        self.assertEqual(data.label, 'IP_T-Iso', 'Incorrect label read')
        self.assertEqual(data.date, date(2020, 10, 28), 'Incorrect date read')
        self.assertEqual(data.time, time(13, 39, 0), 'Incorrect time read')
        self.assertEqual(data.reactor, 'IP-1250-0046',
                         'Incorrect reactor read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 18640, 'Incorrect x data read')
        self.assertEqual(len(data.signals), 1, 'Incorrect y data read')
        self.assertEqual(len(conditions.signals), 6,
                         'Incorrect condition data read')

    # ====== reader/read_algem_ht24.py ========
    def test_read_algem_ht24(self):
        data_list = read_algem_ht24('test/files/Algem-HT24/19775 OD.csv')
        self.assertEqual(len(data_list), 24,
                         'Incorrect number of data sets processed')
        data = data_list[0]
        # Header information
        self.assertEqual(data.label, '(A1) 19775 OD', 'Incorrect label read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 1147, 'Incorrect x data read')
        self.assertEqual(len(data.signals), 1, 'Incorrect y data read')

    def test_read_algem_ht24_details(self):
        data_list, replicate_list = read_algem_ht24_details('test/files/Algem-HT24/19775 OD.csv',
                                                            'test/files/Algem-HT24/19775 Details.csv')
        self.assertEqual(len(data_list), 8,
                         'Incorrect number of data sets processed')
        data = data_list[0]
        # Header information
        self.assertEqual(data.label, '(A1) 19775 OD', 'Incorrect label read')
        self.assertEqual(data.date, date(2020, 2, 13), 'Incorrect date read')
        self.assertEqual(data.time, time(14, 51, 25), 'Incorrect time read')
        self.assertEqual(data.reactor, '19775', 'Incorrect reactor read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 1147, 'Incorrect x data read')
        self.assertEqual(len(data.signals), 1, 'Incorrect y data read')
        # Replicate information
        self.assertEqual(len(replicate_list), 16,
                         'Incorrect number of replicate data sets processed')
        replicate = replicate_list[0]
        self.assertEqual(len(replicate), 2, 'Incorrect size of replicate list')
        self.assertEqual(replicate[1], 0, 'Incorrect replicate index')

    # ====== reader/read_algem_ht24_txt.py ========
    def test_read_algem_ht24_txt(self):
        data_list, replicate_list, condition_list, rep_condition_list = read_algem_ht24_txt(
            'test/files/Algem-HT24/ht24.txt')
        self.assertEqual(len(data_list), 6,
                         'Incorrect number of data sets processed')
        data = data_list[0]
        # Header information
        self.assertEqual(data.label, '(0) ht24', 'Incorrect label read')
        self.assertEqual(data.date, date(2021, 1, 12), 'Incorrect date read')
        self.assertEqual(data.time, time(17, 19, 37), 'Incorrect time read')
        self.assertEqual(data.reactor, '19775', 'Incorrect reactor read')
        self.assertEqual(data.sub_reactor, '0', 'Incorrect sub_reactor read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 10, 'Incorrect x data read')
        self.assertEqual(len(data.signals), 1, 'Incorrect y data read')
        # Replicate information
        self.assertEqual(len(replicate_list), 12,
                         'Incorrect number of replicate data sets processed')
        replicate = replicate_list[0]
        self.assertEqual(len(replicate), 2, 'Incorrect size of replicate list')
        self.assertEqual(replicate[1], 0, 'Incorrect replicate index')
        # Condition information
        self.assertEqual(len(condition_list), 6,
                         'Incorrect number of condition data sets processed')
        condition = condition_list[0]
        self.assertEqual(condition.xaxis.data.size, 105,
                         'Incorrect condition x data read')
        self.assertEqual(len(rep_condition_list), 12,
                         'Incorrect number of replicate condition data sets processed')

    # ====== reader/read_ip.py ========
    def test_read_ip(self):
        data, conditions = read_ip('test/files/IP/IP_T-Iso.csv')
        # Header information
        self.assertEqual(data.label, 'IP_T-Iso', 'Incorrect label read')
        self.assertEqual(data.date, date(2020, 10, 28), 'Incorrect date read')
        self.assertEqual(data.time, time(13, 39, 00), 'Incorrect time read')
        self.assertEqual(data.reactor, 'IP-1250-0046', 'Incorrect reactor read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 18640, 'Incorrect x data read')
        self.assertEqual(len(data.events), 200, 'Incorrect data events read')
        self.assertEqual(len(data.signals), 1, 'Incorrect y data read')
        # Condition information
        self.assertEqual(conditions.xaxis.data.size, 18640, 'Incorrect condition x data read')
        self.assertEqual(len(conditions.signals), 6, 'Incorrect condition y data read')

    # ====== reader/read_psi.py ========
    def test_read_psi(self):
        data, conditions = read_psi('test/files/PSI/PSI_bioreactor.ods')
        # Header information
        self.assertEqual(data.label, 'PSI_bioreactor', 'Incorrect label read')
        self.assertEqual(data.date, date(2020, 8, 1), 'Incorrect date read')
        self.assertEqual(data.time, time(10, 16, 57), 'Incorrect time read')
        self.assertEqual(data.reactor, 'Photobioreactor-041', 'Incorrect reactor read')
        self.assertEqual(data.profile, 'BG11 Synechocystis WT', 'Incorrect profile read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 1200, 'Incorrect x data read')
        self.assertEqual(len(data.events), 1, 'Incorrect data events read')
        self.assertEqual(len(data.signals), 2, 'Incorrect y data read')
        # Condition information
        self.assertEqual(conditions.xaxis.data.size, 6003, 'Incorrect condition x data read')
        self.assertEqual(len(conditions.signals), 6, 'Incorrect condition y data read')

    # ====== reader/read_calibration.py ========
    def test_read_calibration(self):
        calibration = read_calibration('test/files/calibration.csv')
        self.assertEqual(calibration.label, 'calibration', 'Incorrect label read')
        self.assertEqual(len(calibration.true), 7, 'Incorrect true measurements')
        self.assertEqual(len(calibration.measured), 7, 'Incorrect measured measurements')

if __name__ == '__main__':
    print(sys.path)
    unittest.main()
