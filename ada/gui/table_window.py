import csv
import numpy as np
from scipy.optimize import curve_fit

from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QLabel, QWidget,
                             QPushButton, QComboBox, QScrollArea, QListWidget,
                             QVBoxLayout, QTabWidget, QTableWidget,
                             QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import QPoint

from ada.gui.error_window import ErrorWindow
from ada.gui.file_handler import get_save_file_name
from ada.components.table_list_item import TableListItem
from ada.components.button import Button
from ada.components.list import List
from ada.components.user_input import DropDown
from ada.data.processor import (process_data, average_data,
                                time_average)
from ada.data.measurements import (
    get_gradients, get_time_to, get_averages, get_condition_at, get_fit)
from ada.data.models import get_model
from ada.type_functions import isfloat

import ada.configuration as config
import ada.styles as styles
from ada.logger import logger


# Class for a table constructor window
class TableWindow(QMainWindow):

    def __init__(self, parent=None):
        super(TableWindow, self).__init__(parent)
        self.title = 'Create Table'
        self.width = 500*config.wr
        self.height = 330*config.hr
        logger.debug('Creating table window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        self.parent = parent
        self.rows = []
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        tabs = QTabWidget()

        create_layout = QGridLayout()
        create_layout.setContentsMargins(
            5*config.wr, 5*config.hr, 5*config.wr, 5*config.hr)
        create_layout.setSpacing(5*config.wr)

        # List of row options
        self.row_option = DropDown('Row:', config.table_row_options, self)
        create_layout.addWidget(self.row_option, 0, 0)

        # Button to add a new row
        add_button = Button("Add Row", self)
        add_button.clicked.connect(self.add_row)
        add_button.setFixedWidth(100*config.wr)
        add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        create_layout.addWidget(add_button, 0, 1)

        # List of all the added rows
        self.row_list = List(self)
        # self.row_list.setStyleSheet(config.scroll_style)
        self.row_list.setSpacing(-12*config.wr)
        create_layout.addWidget(self.row_list, 1, 0, 2, 2)

        # Button to produce the table
        make_button = Button("Create Table", self)
        make_button.clicked.connect(self.make_table)
        create_layout.addWidget(make_button, 3, 0, 1, 2)

        create_widget = QWidget()
        create_widget.setLayout(create_layout)

        tabs.addTab(create_widget, "Create")

        table_layout = QVBoxLayout()
        self.table = QTableWidget()
        table_layout.addWidget(self.table)

        save_button = Button("Save Table", self)
        save_button.clicked.connect(self.save_table)
        table_layout.addWidget(save_button)

        table_widget = QWidget()
        table_widget.setLayout(table_layout)

        tabs.addTab(table_widget, "Table")
        tabs.setStyleSheet(styles.tab_style)

        self.setCentralWidget(tabs)

    # Add a new row to the table
    def add_row(self):
        try:
            logger.debug('Adding %s row to table' %
                         self.row_option.currentText())
            table_list_item = TableListItem(
                self.row_option.currentText(), self)
            self.row_list.addItem(table_list_item.item)
            self.row_list.setItemWidget(table_list_item.item,
                                        table_list_item.widget)
            self.rows.append(table_list_item)
        except Exception as e:
            logger.error(str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    # Remove a row from the table
    def remove_item(self):
        # Horrible stuff to get list item
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = self.row_list.viewport().mapFromGlobal(gp)
        row = self.row_list.row(self.row_list.itemAt(lp))
        logger.debug('Removing row %i from table' % row)
        self.row_list.takeItem(row)
        self.rows.pop(row)

    # Create table and write to file
    def make_table(self):
        logger.debug('Creating the table')
        try:
            # Get the column headings from the data file names
            column_headings = self.get_headings()
            # Record the titles and data for each row
            row_titles = []
            row_data = []
            tunit = 's'
            if config.xvar == 'minutes':
                tunit = 'min'
            if config.xvar == 'hours':
                tunit = 'hr'
            if config.xvar == 'days':
                tunit = 'day'
            # Loop over the rows
            for row in self.rows:
                # Determine the type of data
                if row.type == 'profile':
                    row_titles.append('Profile')
                    row_data.append(self.parent.data.get_profiles())
                if row.type == 'reactor':
                    row_titles.append('Reactor')
                    row_data.append(self.parent.data.get_reactors())
                if row.type == 'gradient':
                    row_titles.append('Gradient of %s at between %s and %s'
                                      % (row.data.currentText(),
                                         row.grad_from.text(),
                                         row.grad_to.text()))
                    row_data.append(get_gradients(self.parent.data,
                                                  row.data.currentText(),
                                                  row.grad_from.get_float(),
                                                  row.grad_to.get_float()))
                if row.type == 'time to':
                    row_titles.append('Time (%s) to %s of %s'
                                      % (tunit,
                                         row.data.currentText(),
                                         row.time_to.text()))
                    row_data.append(get_time_to(self.parent.data, row.data.currentText(),
                                                row.time_to.get_float()))
                if row.type == 'average of condition':
                    row_titles.append('Average of %s between %s and %s %s'
                                      % (row.condition.currentText(),
                                         row.start_t.text(),
                                         row.end_t.text(),
                                         tunit))
                    row_data.append(get_averages(self.parent.condition_data, self.parent.data,
                                                 row.condition.currentText(),
                                                 row.start_t.get_float(),
                                                 row.end_t.get_float()))
                if row.type == 'condition at time':
                    row_titles.append('%s at time %s %s'
                                      % (row.condition.currentText(),
                                         row.time.text(),
                                         tunit))
                    row_data.append(get_condition_at(self.parent.condition_data, self.parent.data,
                                                     row.condition.currentText(),
                                                     row.time.get_float()))
                if row.type == 'fit parameter':
                    row_titles.append('%s fit of %s between %s and %s %s, parameter %s'
                                      % (row.fit.currentText(),
                                         row.data.currentText(),
                                         row.fit_from.text(),
                                         row.fit_to.text(),
                                         tunit,
                                         row.param.currentText()))
                    row_data.append(get_fit(self.parent.data, row.data.currentText(),
                                            row.fit.currentText(),
                                            row.param.currentText(),
                                            row.fit_from.get_float(),
                                            row.fit_to.get_float()))
            self.header = column_headings
            self.titles = row_titles
            self.data = row_data
            self.show_table()
        except Exception as e:
            logger.error(str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def get_headings(self):
        logger.debug('Getting the table row headings')
        headings = ['File']
        for data in self.parent.data.data_files:
            headings.append(data.label)
        return headings

    def show_table(self):
        logger.debug('Displaying the table')
        self.table.setRowCount(len(self.titles)+1)
        self.table.setColumnCount(len(self.header))
        for col, head in enumerate(self.header):
            self.table.setItem(0, col, QTableWidgetItem(str(head)))
        for row, title in enumerate(self.titles):
            self.table.setItem(row+1, 0, QTableWidgetItem(str(title)))
            for col, dat in enumerate(self.data[row]):
                if dat is not None:
                    if isfloat(dat):
                        self.table.setItem(
                            row+1, col+1, QTableWidgetItem('%.*f' % (config.sig_figs, dat)))
                    else:
                        self.table.setItem(
                            row+1, col+1, QTableWidgetItem(dat))
                else:
                    self.table.setItem(row+1, col+1, QTableWidgetItem('none'))

    def save_table(self):
        try:
            file_name = get_save_file_name()
            if not file_name.endswith('.csv'):
                file_name = file_name + '.csv'
            logger.info('Saving the table as %s' % file_name)
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.header)
                for i, title in enumerate(self.titles):
                    row = [title]
                    for dat in self.data[i]:
                        if dat is not None:
                            row.append(str(dat))
                        else:
                            row.append('none')
                    writer.writerow(row)
            self.close()
        except Exception as e:
            logger.error(str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()
