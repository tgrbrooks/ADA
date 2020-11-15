import csv
import numpy as np

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget
from PyQt5.QtWidgets import QCheckBox, QPushButton, QComboBox

from algaeplot.gui.error_window import ErrorWindow
from algaeplot.gui.file_handler import get_save_directory_name


class ExportWindow(QMainWindow):

    def __init__(self, parent=None):
        super(ExportWindow, self).__init__(parent)
        self.title = 'Export Files'
        self.width = 150
        self.height = 100
        self.parent = parent
        self.test_path = 'none'
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QGridLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        rename_text = QLabel('Rename with profile:')
        rename_text.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(rename_text, 0, 0)
        self.rename = QCheckBox(self)
        layout.addWidget(self.rename, 0, 1)

        conditions_text = QLabel('Include conditions:')
        conditions_text.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(conditions_text, 1, 0)
        self.conditions = QCheckBox(self)
        layout.addWidget(self.conditions, 1, 1)

        export_button = QPushButton("Export", self)
        export_button.clicked.connect(self.export)
        export_button.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(export_button, 2, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def export(self):
        for data in self.parent.data.data_files:
            filename = data.name.split('.')[0] + '.csv'
            path = self.test_path
            if self.test_path == 'none':
                path = get_save_directory_name()
            if self.rename.isChecked():
                filename = path + '/' + data.profile + extension
            else:
                filename = path + '/' + filename.split('/')[-1]

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
                measurement_header = [data.xaxis.name + ' [' + data.xaxis.unit + ']']
                for sig in data.signals:
                    measurement_header.append(sig.name + ' [' + sig.unit + ']')
                if conditions is not None:
                    measurement_header.append('Conditions')
                    for sig in conditions.signals:
                        measurement_header.append(sig.name + ' [' + sig.unit + ']')
                writer.writerow(measurement_header)
                for i, xdat in enumerate(data.xaxis.data):
                    row = [xdat]
                    for sig in data.signals:
                        row.append(sig.data[i])
                    # Find closest signal time
                    if conditions is not None:
                        row.append('')
                        cond_ind = (np.abs(conditions.xaxis.data - xdat)).argmin()
                        for sig in conditions.signals:
                            row.append(sig.data[cond_ind])
                    writer.writerow(row)
        self.close()
