import unittest, sys, os
import tempfile, shutil
from datetime import datetime, date, time

from algaeplot.reader.read_algem_pro import read_algem_pro
from algaeplot.gui.main_window import App
from algaeplot.gui.export_window import ExportWindow

from PyQt5.QtWidgets import QApplication

class AlgaePlotterTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        app = QApplication(sys.argv)
        self.window = App()
        self.data = read_algem_pro('test/files/Algem-Pro/150.txt')
        self.window.data.add_data(self.data)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    # ====== gui/mainwindow.py ========

    def test_main_window_size(self):
        self.assertEqual(self.window.width, 960, 'Incorrect default width')

    # ====== reader/readtextfile.py ========

    def test_algem_pro_read(self):
        # Header information
        self.assertEqual(self.data.label, '150', 'Incorrect label read')
        self.assertEqual(self.data.date, date(2018, 1, 16), 'Incorrect date read')
        self.assertEqual(self.data.time, time(18, 51, 12), 'Incorrect time read')
        self.assertEqual(self.data.reactor, '13134B', 'Incorrect reactor read')
        self.assertEqual(self.data.profile, '20_150_light_c1', 'Incorrect profile read')
        # Data information
        self.assertEqual(self.data.xaxis.name, 'Time', 'Incorrect x name read')
        self.assertEqual(self.data.xaxis.unit, 's', 'Incorrect x unit read')
        self.assertEqual(self.data.xaxis.data.size, 426, 'Incorrect x data read')
        self.assertEqual(len(self.data.signals), 1, 'Incorrect y data read')

    def test_algem_pro_read_downsample(self):
        algem_data = read_algem_pro('test/files/Algem-Pro/150.txt', 10)
        self.assertEqual(algem_data.xaxis.data.size, 42, 'Incorrect x data read')

    # ====== reader/dataholder.py ========

    def test_data_holder(self):
        self.assertEqual(len(self.window.data.data_files), 1, 'Wrong number of data files')
        self.assertEqual(len(self.window.data.replicate_files), 1, 'Wrong number of replicate files')
        self.assertEqual(len(self.window.data.replicate_files[0]), 1, 'Wrong number of replicate files')

    def test_add_delete_data(self):
        algem_data = read_algem_pro('test/files/Algem-Pro/150.txt')
        self.window.data.add_data(algem_data)
        self.assertEqual(len(self.window.data.data_files), 2, 'Wrong number of data files')
        self.window.data.delete_data(1)
        self.assertEqual(len(self.window.data.data_files), 1, 'Wrong number of data files')

    def test_add_delete_replicate(self):
        algem_data = read_algem_pro('test/files/Algem-Pro/150.txt')
        self.window.data.add_replicate(algem_data, 0)
        self.assertEqual(len(self.window.data.replicate_files[0]), 2, 'Wrong number of replicate files')
        self.window.data.delete_replicate(0, 1)
        self.assertEqual(len(self.window.data.replicate_files[0]), 1, 'Wrong number of replicate files')

    '''
    # ====== gui/exportwindow.py ========
    
    def test_export_txt_to_csv(self):
        export_window = ExportWindow(self.window)
        export_window.test_path = self.test_dir
        export_window.export()
        self.assertEqual(os.listdir(self.test_dir), '150.csv', 'Exporting to csv failed')
    '''
    


if __name__ == '__main__':
    print(sys.path)
    unittest.main()
