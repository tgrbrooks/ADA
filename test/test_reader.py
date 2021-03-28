import unittest, sys, os
from datetime import datetime, date, time

from ada.reader.read_algem_pro import read_algem_pro
from ada.reader.read_ada import read_ada
from ada.reader.read_algem_ht24 import read_algem_ht24, read_algem_ht24_details, read_details
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
        self.assertEqual(data.profile, '20_150_light_c1', 'Incorrect profile read')
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
        self.assertEqual(data.reactor, 'IP-1250-0046', 'Incorrect reactor read')
        # Data information
        self.assertEqual(data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(data.xaxis.data.size, 18640, 'Incorrect x data read')
        self.assertEqual(len(data.signals), 1, 'Incorrect y data read')
        self.assertEqual(len(conditions.signals), 6, 'Incorrect condition data read')


if __name__ == '__main__':
    print(sys.path)
    unittest.main()
