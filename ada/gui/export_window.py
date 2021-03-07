import csv
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtWidgets import QCheckBox, QPushButton, QComboBox

from ada.gui.error_window import ErrorWindow
from ada.gui.file_handler import get_save_directory_name
from ada.components.button import Button
from ada.components.user_input import CheckBox

import ada.configuration as config
from ada.logger import logger


class ExportWindow(QMainWindow):

    def __init__(self, parent=None):
        super(ExportWindow, self).__init__(parent)
        self.title = 'Export Files'
        self.width = 150*config.wr
        self.height = 100*config.hr
        logger.debug('Creating export window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        self.parent = parent
        self.test_path = 'none'
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QVBoxLayout()
        layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        layout.setSpacing(5*config.wr)

        self.rename = CheckBox('Rename with profile', self)
        layout.addWidget(self.rename)

        self.conditions = CheckBox('Include conditions', self)
        layout.addWidget(self.conditions)

        export_button = Button("Export", self)
        export_button.clicked.connect(self.export_handler)
        layout.addWidget(export_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def export_handler(self):
        try:
            self.export()
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def export(self):
        path = self.test_path
        if self.test_path == 'none':
            path = get_save_directory_name()
        logger.info('Exporting files to %s' % path)
        for data in self.parent.data.data_files:
            filename = data.label + '.csv'
            if self.rename.isChecked():
                filename = path + '/' + data.profile + '_ada.csv'
            else:
                filename = path + '/' + \
                    filename.split('/')[-1].split('.')[0] + '_ada.csv'
            logger.debug('Exporting file %s' % filename)

            # Get the condition data if that option is checked
            conditions = None
            if self.conditions.isChecked():
                for cond_data in self.parent.condition_data.data_files:
                    if data.reactor != cond_data.reactor:
                        continue
                    if data.date != cond_data.date:
                        continue
                    if data.time != cond_data.time:
                        continue
                    conditions = cond_data

            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                name_header = ['Name', data.label,
                               'Title', data.title,
                               'Reactor', data.reactor,
                               'Profile', data.profile]
                writer.writerow(name_header)
                date_header = ['Date', data.date, 'Time', data.time]
                writer.writerow(date_header)
                measurement_header = [
                    data.xaxis.name + ' [' + data.xaxis.unit + ']']
                for sig in data.signals:
                    measurement_header.append(sig.name + ' [' + sig.unit + ']')
                if conditions is not None:
                    measurement_header.append('Conditions')
                    for sig in conditions.signals:
                        measurement_header.append(
                            sig.name + ' [' + sig.unit + ']')
                writer.writerow(measurement_header)
                for i, xdat in enumerate(data.xaxis.data):
                    row = [xdat]
                    for sig in data.signals:
                        row.append(sig.data[i])
                    # Find closest signal time
                    if conditions is not None:
                        row.append('')
                        cond_ind = (
                            np.abs(conditions.xaxis.data - xdat)).argmin()
                        for sig in conditions.signals:
                            row.append(sig.data[cond_ind])
                    writer.writerow(row)
        self.close()
