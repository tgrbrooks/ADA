import csv

from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QLabel, QWidget,
                             QCheckBox, QPushButton, QComboBox, QListWidget, QLineEdit, QVBoxLayout)
from PyQt5.QtCore import QPoint, Qt

from ada.gui.error_window import ErrorWindow
from ada.gui.file_handler import get_file_names
from ada.type_functions import isint
from ada.components.label import Label
from ada.components.list import List
from ada.components.button import Button, BigButton
from ada.components.user_input import TextEntry, SpinBox, DropDown, CheckBox
from ada.components.spacer import Spacer
from ada.components.data_list_item import DelListItem

from ada.reader.read_algem_ht24 import (read_algem_ht24,
                                        read_algem_ht24_details)
from ada.reader.read_algem_pro import read_algem_pro
from ada.reader.read_ip import read_ip
from ada.reader.read_psi import read_psi
from ada.reader.read_csv import read_csv

import ada.configuration as config


class LoadWindow(QMainWindow):

    def __init__(self, parent, data, condition, row=-1):
        super(LoadWindow, self).__init__(parent)
        self.title = 'Load Files'
        self.width = 350*config.wr
        self.height = 150*config.hr
        self.parent = parent
        self.data = data
        self.condition = condition
        self.details = []
        self.condition_files = []
        self.files = []
        self.row = row
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QVBoxLayout()
        layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        layout.setSpacing(5*config.wr)

        # Dropdown list of available file types
        self.file_type = DropDown('File type:', [], self)
        self.file_type.addItem('Algem Pro')
        # Can't add HT24 data as replicate
        if self.row == -1:
            self.file_type.addItem('Algem HT24')
        self.file_type.addItem('IP')
        self.file_type.addItem('PSI')
        self.file_type.addItem('ADA')
        layout.addWidget(self.file_type)

        # Button for selecting files to import
        select_file_button = Button("Select data file(s)", self)
        select_file_button.clicked.connect(self.select_data)
        select_file_button.clicked.connect(self.update_options)
        layout.addWidget(select_file_button)

        # List of files to import
        self.file_list = List(self)
        self.file_list.setSpacing(-5*config.wr)
        self.file_list.setStyleSheet(config.default_font)
        layout.addWidget(self.file_list)

        # Button and list for Algem conditions files
        self.select_conditions_button = Button("Select conditions file(s)",
                                               self)
        self.select_conditions_button.clicked.connect(self.select_conditions)
        layout.addWidget(self.select_conditions_button)
        self.select_conditions_button.hide()

        self.conditions_file_list = List(self)
        self.conditions_file_list.setSpacing(-5*config.wr)
        self.conditions_file_list.setStyleSheet(config.default_font)
        layout.addWidget(self.conditions_file_list)
        self.conditions_file_list.hide()

        # Button and list for HT24 details file
        self.select_details_button = Button("Select details file", self)
        self.select_details_button.clicked.connect(self.select_details)
        layout.addWidget(self.select_details_button)
        self.select_details_button.hide()

        self.details_file_list = List(self)
        self.details_file_list.setSpacing(-5*config.wr)
        self.details_file_list.setStyleSheet(config.default_font)
        layout.addWidget(self.details_file_list)
        self.details_file_list.hide()

        # Option to downsample conditions data
        self.downsample = TextEntry('Downsample conditions:', self)
        self.downsample.setToolTip('Only read in every X data points')
        layout.addWidget(self.downsample)
        self.downsample.hide()

        # Checkbox for merging replicates in HT24 data
        self.merge_replicates = CheckBox('Merge replicates', self)
        layout.addWidget(self.merge_replicates)
        self.merge_replicates.hide()

        # Button to load the data
        load_button = Button("Load", self)
        load_button.clicked.connect(self.load_handler)
        layout.addWidget(load_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_options(self):
        file_type = self.file_type.currentText()
        self.select_conditions_button.hide()
        self.conditions_file_list.hide()
        self.downsample.hide()
        self.select_details_button.hide()
        self.details_file_list.hide()
        self.merge_replicates.hide()
        # Show details file options for the Algem HT24
        if file_type == 'Algem HT24':
            self.select_details_button.show()
            self.details_file_list.show()
            self.merge_replicates.show()
        # Allow condition files to be added if not dealing with replicates
        if (file_type == 'Algem HT24' or file_type == 'Algem Pro') and self.row == -1:
            self.select_conditions_button.show()
            self.conditions_file_list.show()
            self.downsample.show()

    # Function: Remove file from list of data
    def remove_item(self, file_list, display_list):
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = display_list.viewport().mapFromGlobal(gp)
        row = display_list.row(display_list.itemAt(lp))
        for i, file_name in enumerate(file_list):
            if i != row:
                continue
            del file_list[i]
        self.fill_list(file_list, display_list)

    def fill_list(self, file_list, display_list):
        display_list.clear()
        for i, file_name in enumerate(file_list):
            list_item = DelListItem(file_name.split('/')[-1])
            list_item.button.clicked.connect(
                lambda: self.remove_item(file_list, display_list)
            )
            display_list.addItem(list_item.item)
            display_list.setItemWidget(list_item.item, list_item.widget)

    def select_data(self):
        try:
            self.files = self.files + get_file_names()
            self.fill_list(self.files, self.file_list)
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def select_details(self):
        try:
            self.details = get_file_names()
            self.fill_list(self.details, self.details_file_list)
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def select_conditions(self):
        try:
            self.condition_files = get_file_names()
            self.fill_list(self.condition_files, self.conditions_file_list)
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def load_handler(self):
        try:
            self.load()
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
                raise RuntimeError(
                    "File %s has the wrong extension" % (file_name))

            # Read in files from Algem Pro
            if file_type == 'Algem Pro':
                algem_data = read_algem_pro(file_name)
                if self.row == -1:
                    self.data.add_data(algem_data)
                else:
                    self.data.add_replicate(algem_data, self.row)

            # Read in files from Algem HT24 if details file is provided
            elif file_type == 'Algem HT24' and len(self.details) == 0:
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

            # Read in files from Industrial Plankton
            elif file_type == 'IP':
                try:
                    ip_data, condition_data = read_ip(file_name)
                except Exception as e:
                    raise RuntimeError(
                        'Error reading file '+file_name+'\n'+str(e))
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
                    raise RuntimeError(
                        'Error reading file '+file_name+'\n'+str(e))
                if self.row == -1:
                    self.data.add_data(psi_data)
                    self.condition.add_data(condition_data)
                else:
                    self.data.add_replicate(psi_data, self.row)

            elif file_type == 'ADA':
                csv_data, condition_data = read_csv(file_name)
                if self.row == -1:
                    self.data.add_data(csv_data)
                    self.condition.add_data(condition_data)
                else:
                    self.data.add_replicate(csv_data, self.row)

        if len(self.condition_files) > 0:
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
                elif file_type == 'Algem HT24' and len(self.details) == 0:
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
