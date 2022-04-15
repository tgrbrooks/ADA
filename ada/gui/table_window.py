import csv

from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QWidget,
                             QVBoxLayout, QTabWidget, QTableWidget,
                             QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import QPoint

from ada.gui.error_window import error_wrapper
from ada.gui.file_handler import get_save_file_name
from ada.components.table_list_item import TableListItem
from ada.components.button import Button
from ada.components.list import List
from ada.components.user_input import DropDown
from ada.data.data_manager import data_manager
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
    @error_wrapper
    def add_row(self):
        logger.debug('Adding %s row to table' %
                     self.row_option.currentText())
        table_list_item = TableListItem(
            self.row_option.currentText(), self)
        self.row_list.addItem(table_list_item.item)
        self.row_list.setItemWidget(table_list_item.item,
                                    table_list_item.widget)
        self.rows.append(table_list_item)

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

    def get_row_title(self, row):
        tunit = 's'
        if config.xvar == 'minutes':
            tunit = 'min'
        if config.xvar == 'hours':
            tunit = 'hr'
        if config.xvar == 'days':
            tunit = 'day'
        row_title = ''
        # Determine the type of data
        if row.type == 'profile':
            row_title = 'Profile'
        if row.type == 'reactor':
            row_title = 'Reactor'
        if row.type == 'gradient':
            row_title = ('Gradient of %s at between %s and %s'
                         % (row.data.currentText(),
                            row.grad_from.text(),
                            row.grad_to.text()))
        if row.type == 'time to':
            row_title = ('Time (%s) to %s of %s'
                         % (tunit,
                            row.data.currentText(),
                            row.time_to.text()))
        if row.type == 'average of condition':
            row_title = ('Average of %s between %s and %s %s'
                         % (row.condition.currentText(),
                            row.start_t.text(),
                            row.end_t.text(),
                            tunit))
        if row.type == 'condition at time':
            row_title = ('%s at time %s %s'
                         % (row.condition.currentText(),
                            row.time.text(),
                            tunit))
        if row.type == 'fit parameter':
            row_title = ('%s fit of %s between %s and %s %s, parameter %s'
                         % (row.fit.currentText(),
                            row.data.currentText(),
                            row.fit_from.text(),
                            row.fit_to.text(),
                            tunit,
                            row.param.currentText()))
        return row_title

    def get_row_data(self, row):
        row_data = []
        if row.type == 'profile':
            row_data = [data_manager.growth_data.get_profiles()]
        if row.type == 'reactor':
            row_data = [data_manager.growth_data.get_reactors()]
        if row.type == 'gradient':
            gradients = data_manager.get_gradients(
                row.data.currentText(),
                row.grad_from.get_float(),
                row.grad_to.get_float())
            row_data = [gradients]
        if row.type == 'time to':
            time_to = data_manager.get_time_to(row.data.currentText(),
                                               row.time_to.get_float())
            row_data = [time_to]
        if row.type == 'average of condition':
            average, _ = data_manager.get_averages(
                row.condition.currentText(),
                row.start_t.get_float(),
                row.end_t.get_float())
            row_data = [average]
        if row.type == 'condition at time':
            condition = data_manager.get_condition_at(
                row.condition.currentText(),
                row.time.get_float())
            row_data = [condition]
        if row.type == 'fit parameter':
            fit_result, fit_error = data_manager.get_all_fit_params(row.data.currentText(),
                                                                    row.fit.currentText(),
                                                                    row.fit_from.get_float(),
                                                                    row.fit_to.get_float(),
                                                                    row.param.currentText())
            if row.show_error.isChecked():
                row_data = [fit_result, fit_error]
            else:
                row_data = [fit_result]
        return row_data

    # Create table and write to file
    @error_wrapper
    def make_table(self):
        logger.debug('Creating the table')
        # Get the column headings from the data file names
        column_headings = self.get_headings()
        # Record the titles and data for each row
        row_titles = []
        row_data = []
        # Loop over the rows
        for row in self.rows:
            row_titles.append(self.get_row_title(row))
            row_data.append(self.get_row_data(row))
        self.header = column_headings
        self.titles = row_titles
        self.data = row_data
        self.show_table()

    def get_headings(self):
        logger.debug('Getting the table row headings')
        headings = ['File']
        for data in data_manager.growth_data.data_files:
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
            for col, dat in enumerate(self.data[row][0]):
                if dat is not None:
                    logger.debug(dat)
                    if len(self.data[row]) == 2:
                        self.table.setItem(
                            row+1, col+1, QTableWidgetItem('%.*f (%.*f)' % (config.sig_figs, dat, config.sig_figs, self.data[row][1][col])))
                    elif isfloat(dat) and title != 'Reactor':
                        self.table.setItem(
                            row+1, col+1, QTableWidgetItem('%.*f' % (config.sig_figs, dat)))
                    else:
                        self.table.setItem(
                            row+1, col+1, QTableWidgetItem(dat))
                else:
                    self.table.setItem(row+1, col+1, QTableWidgetItem('none'))

    @error_wrapper
    def save_table(self):
        file_name = get_save_file_name()
        if not file_name.endswith('.csv'):
            file_name = file_name + '.csv'
        logger.info('Saving the table as %s' % file_name)
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in range(self.table.rowCount()):
                    rowdata = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('none')
                    writer.writerow(rowdata)
        self.close()
