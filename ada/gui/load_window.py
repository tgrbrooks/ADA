from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QPoint

from ada.data.data_manager import data_manager
from ada.gui.error_window import error_wrapper
from ada.gui.file_handler import get_file_names
from ada.type_functions import isint
from ada.components.list import List
from ada.components.window import Window
from ada.components.button import Button
from ada.components.user_input import TextEntry, DropDown, CheckBox
from ada.components.data_list_item import DelListItem

from ada.reader.read_algem_ht24 import (read_algem_ht24,
                                        read_algem_ht24_details)
from ada.reader.read_algem_pro import read_algem_pro
from ada.reader.read_algem_ht24_txt import read_algem_ht24_txt
from ada.reader.read_ip import read_ip
from ada.reader.read_psi import read_psi
from ada.reader.read_ada import read_ada
from ada.reader.read_microbemeter import read_microbemeter

import ada.configuration as config
import ada.styles as styles
from ada.logger import logger


class LoadWindow(Window):

    def __init__(self, parent, row=-1):
        super(LoadWindow, self).__init__(
            'Load Files', 350, 150, QVBoxLayout, parent)
        self.details = []
        self.condition_files = []
        self.files = []
        self.row = row
        self.initUI()

    def initUI(self):
        # Dropdown list of available file types
        file_types = config.replicate_types
        if self.row == -1:
            file_types = config.file_types
        self.file_type = self.window.addWidget(
            DropDown('File type:', file_types, change_action=self.update_options))

        # Button for selecting files to import
        self.window.addWidget(
            Button("Select data file(s)", clicked=self.select_data))

        # List of files to import
        self.file_list = self.window.addWidget(List())
        self.file_list.setSpacing(-5*config.wr)
        self.file_list.setStyleSheet(styles.default_font)

        # Button and list for Algem conditions files
        self.select_conditions_button = self.window.addWidget(
            Button("Select conditions file(s)", clicked=self.select_conditions))
        self.select_conditions_button.hide()

        self.conditions_file_list = self.window.addWidget(List(spacing=-5*config.wr, style=styles.default_font))
        self.conditions_file_list.hide()

        # Button and list for HT24 details file
        self.select_details_button = self.window.addWidget(
            Button("Select details file", clicked=self.select_details))
        self.select_details_button.hide()

        self.details_file_list = self.window.addWidget(List(spacing=-5*config.wr, style=styles.default_font))
        self.details_file_list.hide()

        # Option to downsample conditions data
        self.downsample = self.window.addWidget(
            TextEntry('Downsample conditions:', default=config.downsample, tooltip='Only read in every X data points'))
        self.downsample.hide()

        # Checkbox for merging replicates in HT24 data
        self.merge_replicates = self.window.addWidget(
            CheckBox('Merge replicates'))
        self.merge_replicates.hide()

        # Button to load the data
        self.window.addWidget(Button("Load", clicked=self.load))

        self.update_options()

    def update_options(self):
        logger.debug('Updating the load options based on file type')
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
        if file_type == 'Algem HT24' or file_type == 'Algem Pro':
            self.select_conditions_button.show()
            self.conditions_file_list.show()
            self.downsample.show()
        if file_type == 'MicrobeMeter' and self.row == -1:
            self.merge_replicates.show()

    # Function: Remove file from list of data
    def remove_item(self, file_list, display_list):
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = display_list.viewport().mapFromGlobal(gp)
        row = display_list.row(display_list.itemAt(lp))
        logger.debug('Removing item %i from data list' % row)
        for i, _ in enumerate(file_list):
            if i != row:
                continue
            del file_list[i]
        self.fill_list(file_list, display_list)

    def fill_list(self, file_list, display_list):
        logger.debug('Creating list of files to be loaded')
        display_list.clear()
        for file_name in file_list:
            list_item = DelListItem(file_name.split('/')[-1])
            list_item.button.clicked.connect(
                lambda: self.remove_item(file_list, display_list)
            )
            display_list.addItem(list_item.item)
            display_list.setItemWidget(list_item.item, list_item.widget)

    @error_wrapper
    def select_data(self):
        logger.debug('Selecting data files')
        self.files = self.files + get_file_names()
        self.fill_list(self.files, self.file_list)

    @error_wrapper
    def select_details(self):
        logger.debug('Selecting details files')
        self.details = get_file_names()
        self.fill_list(self.details, self.details_file_list)

    @error_wrapper
    def select_conditions(self):
        logger.debug('Selecting conditions files')
        self.condition_files = get_file_names()
        self.fill_list(self.condition_files, self.conditions_file_list)

    def load_algem_pro(self, file_name):
        logger.info('Loading an Algem-Pro file %s' % file_name)
        # Read in files from Algem Pro
        algem_data = read_algem_pro(file_name)
        if self.row == -1:
            data_manager.growth_data.add_data(algem_data)
        else:
            data_manager.growth_data.add_replicate(algem_data, self.row)

    def load_algem_pro_conditions(self, file_name, downsample):
        logger.info('Loading Algem-Pro condition file %s, downsample %i' %
                    (file_name, downsample))
        # Read in conditions files from Algem Pro
        algem_conditions = read_algem_pro(file_name, downsample)
        if self.row == -1:
            data_manager.condition_data.add_data(algem_conditions)
        else:
            data_manager.condition_data.add_replicate(
                algem_conditions, self.row)

    def load_algem_ht24_txt(self, file_name):
        downsample = self.downsample.get_int()

        logger.info('Loading a partial HT-24 file %s, downsample: %i' %
                    (file_name, downsample))
        algem_data_list, rep_algem_data_list, cond_data_list,\
            rep_cond_data_list = read_algem_ht24_txt(file_name, downsample)
        for algem_data in algem_data_list:
            data_manager.growth_data.add_data(algem_data)
        for replicate in rep_algem_data_list:
            if self.merge_replicates.isChecked():
                data_manager.growth_data.add_replicate(
                    replicate[0], replicate[1])
            else:
                data_manager.growth_data.add_data(replicate[0])
        for condition_data in cond_data_list:
            data_manager.condition_data.add_data(condition_data)
        for replicate in rep_cond_data_list:
            if self.merge_replicates.isChecked():
                data_manager.condition_data.add_replicate(
                    replicate[0], replicate[1])
            else:
                data_manager.condition_data.add_data(replicate[0])

    def load_algem_ht24(self, file_name):
        logger.info('Loading HT-24 file %s' % file_name)
        # Read in files from Algem HT24 if no details file is provided
        if len(self.details) == 0:
            algem_data_list = read_algem_ht24(file_name)
            for algem_data in algem_data_list:
                data_manager.growth_data.add_data(algem_data)

        # Read in files from Algem HT24 with details file
        else:
            algem_data_list, replicate_data_list = read_algem_ht24_details(
                file_name, self.details[0])
            for algem_data in algem_data_list:
                data_manager.growth_data.add_data(algem_data)
            for replicate in replicate_data_list:
                if self.merge_replicates.isChecked():
                    data_manager.growth_data.add_replicate(
                        replicate[0], replicate[1])
                else:
                    data_manager.growth_data.add_data(replicate[0])

    def load_algem_ht24_conditions(self, file_name, downsample):
        logger.info('Loading HT-24 condition file %s, downsample %i' %
                    (file_name, downsample))
        # Read in files from Algem HT24 if details file is provided
        if len(self.details) == 0:
            algem_conditions_list = read_algem_ht24(file_name,
                                                    downsample)
            for algem_conditions in algem_conditions_list:
                data_manager.condition_data.add_data(algem_conditions)

        # Read in files from Algem HT24 without details file
        else:
            algem_conditions_list, replicate_conditions_list = \
                read_algem_ht24_details(file_name, self.details[0],
                                        downsample)
            for algem_conditions in algem_conditions_list:
                data_manager.condition_data.add_data(algem_conditions)
            for replicate in replicate_conditions_list:
                if self.merge_replicates.isChecked():
                    data_manager.condition_data.add_replicate(replicate[0],
                                                              replicate[1])
                else:
                    data_manager.condition_data.add_data(replicate[0])

    def load_ip(self, file_name):
        logger.info('Loading IP file %s' % file_name)
        # Read in files from Industrial Plankton
        try:
            ip_data, condition_data = read_ip(file_name)
        except Exception as e:
            raise RuntimeError(
                'Error reading file '+file_name+'\n'+str(e))
        if self.row == -1:
            data_manager.growth_data.add_data(ip_data)
            data_manager.condition_data.add_data(condition_data)
        else:
            data_manager.growth_data.add_replicate(ip_data, self.row)
            data_manager.condition_data.add_replicate(condition_data, self.row)

    def load_psi(self, file_name):
        logger.info('Loading PSI file %s' % file_name)
        # Read in files from Photon System Instruments photobioreactor
        try:
            psi_data, condition_data = read_psi(file_name)
        except Exception as e:
            raise RuntimeError(
                'Error reading file '+file_name+'\n'+str(e))
        if self.row == -1:
            data_manager.growth_data.add_data(psi_data)
            data_manager.condition_data.add_data(condition_data)
        else:
            data_manager.growth_data.add_replicate(psi_data, self.row)
            data_manager.condition_data.add_replicate(condition_data, self.row)

    def load_ada(self, file_name):
        logger.info('Loading ADA file %s' % file_name)
        ada_data, condition_data = read_ada(file_name)
        if self.row == -1:
            data_manager.growth_data.add_data(ada_data)
            if condition_data is not None:
                data_manager.condition_data.add_data(condition_data)
        else:
            data_manager.growth_data.add_replicate(ada_data, self.row)
            if condition_data is not None:
                data_manager.condition_data.add_replicate(
                    condition_data, self.row)

    def load_microbemeter(self, file_name):
        logger.info('Loading MicrobeMeter file %s' % file_name)
        data_list, condition_data = read_microbemeter(file_name)
        if self.row == -1:
            data_manager.growth_data.add_data(data_list[0])
            n_files = len(data_manager.growth_data.data_files)
            for data in data_list[1:]:
                if self.merge_replicates.isChecked():
                    data_manager.growth_data.add_replicate(data, n_files - 1)
                else:
                    data_manager.growth_data.add_data(data)
            if condition_data is not None:
                data_manager.condition_data.add_data(condition_data)
        else:
            for data in data_list:
                data_manager.growth_data.add_replicate(data, self.row)

    @error_wrapper
    def load(self):
        logger.debug('Loading files into ADA')
        file_type = self.file_type.currentText()
        for file_name in self.files:
            if file_type == 'Algem Pro' and file_name.endswith('.txt'):
                self.load_algem_pro(file_name)
            elif file_type == 'Algem HT24' and file_name.endswith('.txt'):
                self.load_algem_ht24_txt(file_name)
            elif file_type == 'Algem HT24' and file_name.endswith('.csv'):
                self.load_algem_ht24(file_name)
            elif file_type == 'IP' and file_name.endswith('.csv'):
                self.load_ip(file_name)
            elif file_type == 'PSI' and file_name.endswith('.ods'):
                self.load_psi(file_name)
            elif file_type == 'ADA' and file_name.endswith('.csv'):
                self.load_ada(file_name)
            elif file_type == 'MicrobeMeter' and file_name.endswith('.tsv'):
                self.load_microbemeter(file_name)
            else:
                raise RuntimeError(
                    "File %s has the wrong extension" % (file_name))

        if len(self.condition_files) > 0:
            # Set downsampling if option selected
            downsample = -1
            if isint(self.downsample.text()):
                downsample = int(self.downsample.text())

            # Load in optional conditions data for algem machines
            for file_name in self.condition_files:
                if file_type == 'Algem Pro' and file_name.endswith('.txt'):
                    self.load_algem_pro_conditions(file_name, downsample)
                elif file_type == 'Algem HT24' and file_name.endswith('.csv'):
                    self.load_algem_ht24_conditions(file_name, downsample)
                else:
                    raise RuntimeError("File %s has the wrong extension" %
                                       (file_name))

        # Update the data lists in the main window
        self.parent.update_data_list()
        self.parent.update_condition_data_list()
        self.close()
