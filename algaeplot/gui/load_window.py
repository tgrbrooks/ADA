import csv

from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QLabel, QWidget,
    QCheckBox, QPushButton, QComboBox, QListWidget, QLineEdit)

from algaeplot.gui.error_window import ErrorWindow
from algaeplot.gui.file_handler import get_file_names
from algaeplot.gui.type_functions import isint
from algaeplot.gui.label import Label

from algaeplot.reader.read_algem_ht24 import (read_algem_ht24,
    read_algem_ht24_details)
from algaeplot.reader.read_algem_pro import read_algem_pro
from algaeplot.reader.read_ip_t_iso import read_ip_t_iso
from algaeplot.reader.read_psi import read_psi
from algaeplot.reader.read_csv import read_csv

import algaeplot.configuration as config

class LoadWindow(QMainWindow):

    def __init__(self, parent, data, condition, row=-1):
        super(LoadWindow, self).__init__(parent)
        self.title = 'Load Files'
        self.width = 250
        self.height = 150
        self.parent = parent
        self.data = data
        self.condition = condition
        self.details = None
        self.condition_files = None
        self.row = row
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QGridLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Dropdown list of available file types
        file_text = Label('File type:', True)
        layout.addWidget(file_text, 0, 0)
        self.file_type = QComboBox(self)
        self.file_type.addItem('Algem Pro')
        # Can't add HT24 data as replicate
        if self.row == -1:
            self.file_type.addItem('Algem HT24')
        self.file_type.addItem('IP T-Iso')
        self.file_type.addItem('PSI')
        self.file_type.addItem('AlgaePlotter')
        layout.addWidget(self.file_type, 0, 1)

        # Button for selecting files to import
        select_file_button = QPushButton("Select data file(s)", self)
        select_file_button.clicked.connect(self.select_data)
        select_file_button.clicked.connect(self.update_options)
        select_file_button.setStyleSheet(config.default_font_bold)
        layout.addWidget(select_file_button, 1, 0)

        # List of files to import
        self.file_list = QListWidget(self)
        self.file_list.setStyleSheet(config.default_font_bold)
        layout.addWidget(self.file_list, 1, 1)

        # Button and list for Algem conditions files
        self.select_conditions_button = QPushButton(
            "Select conditions file(s)", self)
        self.select_conditions_button.clicked.connect(self.select_conditions)
        self.select_conditions_button.setStyleSheet(config.default_font_bold)
        layout.addWidget(self.select_conditions_button, 2, 0)
        self.select_conditions_button.hide()

        self.conditions_file_list = QListWidget(self)
        self.conditions_file_list.setStyleSheet(config.default_font_bold)
        layout.addWidget(self.conditions_file_list, 2, 1)
        self.conditions_file_list.hide()

        # Option to downsample conditions data
        self.downsample_text = Label('Downsample conditions:', True)
        layout.addWidget(self.downsample_text, 3, 0)
        self.downsample_text.hide()

        self.downsample = QLineEdit(self)
        self.downsample.setToolTip('Only read in every X data points')
        layout.addWidget(self.downsample, 3, 1)
        self.downsample.hide()

        # Button and list for HT24 details file
        self.select_details_button = QPushButton("Select details file", self)
        self.select_details_button.clicked.connect(self.select_details)
        self.select_details_button.setStyleSheet(config.default_font_bold)
        layout.addWidget(self.select_details_button, 4, 0)
        self.select_details_button.hide()

        self.details_file_list = QListWidget(self)
        self.details_file_list.setStyleSheet(config.default_font_bold)
        layout.addWidget(self.details_file_list, 4, 1)
        self.details_file_list.hide()

        # Checkbox for merging replicates in HT24 data
        self.merge_replicates_text = Label('Merge replicates')
        layout.addWidget(self.merge_replicates_text, 5, 0)
        self.merge_replicates_text.hide()

        self.merge_replicates = QCheckBox(self)
        layout.addWidget(self.merge_replicates, 5, 1)
        self.merge_replicates.hide()

        # Button to load the data
        load_button = QPushButton("Load", self)
        load_button.clicked.connect(self.load)
        load_button.setStyleSheet(config.default_font_bold)
        layout.addWidget(load_button, 6, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_options(self):
        file_type = self.file_type.currentText()
        self.select_conditions_button.hide()
        self.conditions_file_list.hide()
        self.downsample_text.hide()
        self.downsample.hide()
        self.select_details_button.hide()
        self.details_file_list.hide()
        self.merge_replicates_text.hide()
        self.merge_replicates.hide()
        # Show details file options for the Algem HT24
        if file_type == 'Algem HT24':
            self.select_details_button.show()
            self.details_file_list.show()
            self.merge_replicates_text.show()
            self.merge_replicates.show()
        # Allow condition files to be added if not dealing with replicates
        if (file_type == 'Algem HT24' or file_type == 'Algem Pro') and self.row == -1:
            self.select_conditions_button.show()
            self.conditions_file_list.show()
            self.downsample_text.show()
            self.downsample.show()

    def select_data(self):
        try:
            self.files = get_file_names()
            for file_name in self.files:
                self.file_list.addItem(file_name.split('/')[-1])
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def select_details(self):
        try:
            self.details = get_file_names()
            for file_name in self.details:
                self.details_file_list.addItem(file_name.split('/')[-1])
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def select_conditions(self):
        try:
            self.condition_files = get_file_names()
            for file_name in self.condition_files:
                self.conditions_file_list.addItem(file_name.split('/')[-1])
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()


    def load(self):
        file_type = self.file_type.currentText()
        extension = '.csv'
        if file_type == 'Algem Pro':
            extension = '.txt'
        if file_type == 'PSI':
            extension = '.ods'

        for file_name in self.files:
            if not file_name.endswith(extension):
                raise RuntimeError("File %s has the wrong extension" % (file_name))

            # Read in files from Algem Pro
            if file_type == 'Algem Pro':
                algem_data = read_algem_pro(file_name)
                if self.row == -1:
                    self.data.add_data(algem_data)
                else:
                    self.data.add_replicate(algem_data, self.row)

            # Read in files from Algem HT24 if details file is provided
            elif file_type == 'Algem HT24' and not self.details:
                algem_data_list = read_algem_ht24(file_name)
                for algem_data in algem_data_list:
                    if self.row == -1:
                        self.data.add_data(algem_data)
                    else:
                        self.data.add_replicate(algem_data, self.row)

            # Read in files from Algem HT24 without details file
            elif file_type == 'Algem HT24':
                algem_data_list, replicate_data_list = read_algem_ht24_details(
                    file_name, self.details[0])
                for algem_data in algem_data_list:
                    self.data.add_data(algem_data)
                for replicate in replicate_data_list:
                    if self.merge_replicates.isChecked():
                        self.data.add_replicate(replicate[0], replicate[1])
                    else:
                        self.data.add_data(replicate[0])

            # Read in files from Industrial Plankton T-Iso
            elif file_type == 'IP T-Iso':
                try:
                    ip_data, condition_data = read_ip_t_iso(file_name)
                except Exception as e:
                    raise RuntimeError('Error reading file '+file_name+'\n'+str(e))
                if self.row == -1:
                    self.data.add_data(ip_data)
                    self.condition.add_data(condition_data)
                else:
                    self.data.add_replicate(ip_data, self.row)

            # Read in files from Photon System Instruments photobioreactor
            elif file_type == 'PSI':
                try:
                    psi_data, condition_data = read_psi(file_name)
                except Exception as e:
                    raise RuntimeError('Error reading file '+file_name+'\n'+str(e))
                if self.row == -1:
                    self.data.add_data(psi_data)
                    self.condition.add_data(condition_data)
                else:
                    self.data.add_replicate(psi_data, self.row)

            elif file_type == 'AlgaePlotter':
                csv_data, condition_data = read_csv(file_name)
                if self.row == -1:
                    self.data.add_data(csv_data)
                    self.condition.add_data(condition_data)
                else:
                    self.data.add_replicate(csv_data, self.row)
        
        if self.condition_files is not None:
            # Set downsampling if option selected
            downsample = -1
            if isint(self.downsample.text()):
                downsample = int(self.downsample.text())

            # Load in optional conditions data for algem machines
            for file_name in self.condition_files:
                if not file_name.endswith(extension):
                    raise RuntimeError("File %s has the wrong extension" %
                                       (file_name))

                # Read in conditions files from Algem Pro
                if file_type == 'Algem Pro':
                    algem_conditions = read_algem_pro(file_name, downsample)
                    self.condition.add_data(algem_conditions)

                # Read in files from Algem HT24 if details file is provided
                elif file_type == 'Algem HT24' and not self.details:
                    algem_conditions_list = read_algem_ht24(file_name,
                                                            downsample)
                    for algem_conditions in algem_conditions_list:
                        self.condition.add_data(algem_conditions)

                # Read in files from Algem HT24 without details file
                elif file_type == 'Algem HT24':
                    algem_conditions_list, replicate_conditions_list = \
                        read_algem_ht24_details(file_name, self.details[0],
                                                downsample)
                    for algem_conditions in algem_conditions_list:
                        self.condition.add_data(algem_conditions)
                    for replicate in replicate_conditions_list:
                        if self.merge_replicates.isChecked():
                            self.condition.add_replicate(replicate[0],
                                                         replicate[1])
                        else:
                            self.condition.add_data(replicate[0])

        # Update the data lists in the main window
        self.parent.update_data_list()
        self.parent.update_condition_data_list()
        self.close()
