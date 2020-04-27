from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget, QPushButton, QComboBox, QScrollArea, QListWidget, QVBoxLayout
from PyQt5.QtCore import QPoint

import numpy as np

from gui.errorwindow import ErrorWindow
from gui.tablelistitem import TableListItem
from plotter.functions import process_data, average_data, time_average
import csv

# Class for a table constructor window
class TableWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(TableWindow, self).__init__(parent)
        self.title = 'Create Table'
        self.width = 400
        self.height = 220
        self.parent = parent
        self.rows = []
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        #self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(5)

        # List of row options
        self.row_option = QComboBox(self)
        self.row_option.addItem('profile')
        self.row_option.addItem('reactor')
        self.row_option.addItem('gradient')
        self.row_option.addItem('time to')
        self.row_option.addItem('average of condition')
        self.row_option.addItem('condition at time')
        layout.addWidget(self.row_option, 0, 0)

        # Button to add a new row
        add_button = QPushButton("Add Row", self)
        add_button.clicked.connect(self.add_row)
        add_button.setStyleSheet('font-size: 14pt; font-weight: bold; font-family: Courier;')
        layout.addWidget(add_button, 0, 1)

        # List of all the added rows
        table_layout = QVBoxLayout()
        self.table_list = QListWidget(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        table_widget = QWidget()
        table_widget.setLayout(table_layout)
        table_layout.addWidget(self.table_list)
        scroll_area.setWidget(table_widget)
        layout.addWidget(scroll_area, 1, 0, 2, 2)

        # Button to produce the table
        make_button = QPushButton("Create Table", self)
        make_button.clicked.connect(self.make_table)
        make_button.setStyleSheet('font-size: 14pt; font-weight: bold; font-family: Courier;')
        layout.addWidget(make_button, 3, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Add a new row to the table
    def add_row(self):
        table_list_item = TableListItem(self.row_option.currentText(), self)
        self.table_list.addItem(table_list_item.item)
        self.table_list.setItemWidget(table_list_item.item, table_list_item.widget)
        self.rows.append(table_list_item)

    # Remove a row from the table
    def remove_item(self):
        # Horrible stuff to get list item
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = self.table_list.viewport().mapFromGlobal(gp)
        row = self.table_list.row(self.table_list.itemAt(lp))
        self.table_list.takeItem(row)
        self.rows.pop(row)

    # Create table and write to file
    def make_table(self):
        try:
            # Get the column headings from the data file names
            column_headings = self.get_headings()
            # Record the titles and data for each row
            row_titles = []
            row_data = []
            tunit = 's'
            if self.parent.config.xvar == 'minutes':
                tunit = 'min'
            if self.parent.config.xvar == 'hours':
                tunit = 'hr'
            if self.parent.config.xvar == 'days':
                tunit = 'day'
            # Loop over the rows
            for row in self.rows:
                # Determine the type of data
                if row.type == 'profile':
                    row_titles.append('Profile')
                    row_data.append(self.get_profiles())
                if row.type == 'reactor':
                    row_titles.append('Reactor')
                    row_data.append(self.get_reactors())
                if row.type == 'gradient':
                    row_titles.append('Gradient of %s at between %s and %s' % (row.data.currentText(), row.grad_from.text(), row.grad_to.text()))
                    row_data.append(self.get_gradients(row.data.currentText(), float(row.grad_from.text()), float(row.grad_to.text())))
                if row.type == 'time to':
                    row_titles.append('Time (%s) to %s of %s' % (tunit, row.data.currentText(), row.time_to.text()))
                    row_data.append(self.get_time_to(row.data.currentText(), float(row.time_to.text())))
                if row.type == 'average of condition':
                    row_titles.append('Average of %s between %s and %s %s' % (row.condition.currentText(), row.start_t.text(), row.end_t.text(), tunit))
                    row_data.append(self.get_averages(row.condition.currentText(), float(row.start_t.text()), float(row.end_t.text())))
                if row.type == 'condition at time':
                    row_titles.append('%s at time %s %s' % (row.condition.currentText(), row.time.text(), tunit))
                    row_data.append(self.get_condition_at(row.condition.currentText(), float(row.time.text())))
            self.save_table(column_headings, row_titles, row_data)
            self.close()
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()
        
    def get_headings(self):
        headings = ['File']
        for data in self.parent.data.data_files:
            headings.append(data.label)
        return headings

    def get_profiles(self):
        profiles = []
        for data in self.parent.data.data_files:
            profiles.append(data.profile)
        return profiles

    def get_reactors(self):
        reactors = []
        for data in self.parent.data.data_files:
            reactors.append(data.reactor)
        return reactors

    def get_gradients(self, data_name, grad_from, grad_to):
        gradients = []
        for i, data in enumerate(self.parent.data.data_files):
            xdata, ydata = self.get_xy_data(i, data_name)
            # Calculate the gradient
            x1 = -1.
            y1 = -1.
            x2 = -1.
            y2 = -1.
            for i, ydat in enumerate(ydata):
                if ydat >= grad_from and x1 == -1:
                    x1 = xdata[i]
                    y1 = ydat
                if ydat >= grad_to and x2 == -1:
                    x2 = xdata[i]
                    y2 = ydat
                if x1 != -1 and x2 != -1:
                    break
            if x1 == -1. and x2 == -1.:
                gradients.append(-1.)
            else:
                gradients.append((y2-y1)/(x2-x1))
        return gradients

    def get_time_to(self, data_name, time_to):
        times = []
        for i, data in enumerate(self.parent.data.data_files):
            found = False
            xdata, ydata = self.get_xy_data(i, data_name)
            for i, ydat in enumerate(ydata):
                if ydat >= time_to:
                    times.append(xdata[i])
                    found = True
                    break
            if not found:
                times.append(-1)
        return times

    def get_xy_data(self, i, data_name):
        xdatas = []
        ydatas = []
        for rep in self.parent.data.replicate_files[i]:
            xdata = rep.get_xdata(self.parent.config.xvar)
            ydata = rep.get_signal(data_name)
            xdata, ydata = process_data(xdata, ydata, self.parent.config)
            xdatas.append(xdata)
            ydatas.append(ydata)
        if len(xdatas) > 1:
            xdata, ydata, yerr = average_data(xdatas, ydatas)
            return xdata, ydata
        elif len(xdatas) == 1: 
            return xdatas[0], ydatas[0]
        else:
            raise RuntimeError('No data found')

    def get_averages(self, cond_name, start_t, end_t):
        averages = []
        for i, data in enumerate(self.parent.data.data_files):
            found = False
            xdata, ydata = self.get_condition_xy_data(i, cond_name)
            dat = np.array([])
            #dat = np.append(dat, np.interp(start_t, ydata[i]))
            #dat = np.append(dat, np.interp(end_t, ydata[i]))
            for i, x in enumerate(xdata):
                if x >= start_t and x <= end_t:
                    dat = np.append(dat, ydata[i])
            mean = np.mean(dat)
            averages.append(mean)
        return averages

    def get_condition_at(self, cond_name, time):
        values = []
        for i, data in enumerate(self.parent.data.data_files):
            xdata, ydata = self.get_condition_xy_data(i, cond_name)
            values.append(np.interp(time, xdata, ydata))
        return values

    def get_condition_xy_data(self, i, cond_name):
        for cond in self.parent.condition_data.data_files:
            if self.parent.data.data_files[i].reactor != cond.reactor:
                continue
            if self.parent.data.data_files[i].date != cond.date:
                continue
            if self.parent.data.data_files[i].time != cond.time:
                continue
            xdata = cond.get_xdata(self.parent.config.xvar)
            ydata = cond.get_signal(cond_name)
            if self.parent.config.condition_average != -1:
                xdata, ydata, yerr = time_average(xdata, ydata, self.parent.config.condition_average)
            return xdata, ydata
        raise RuntimeError('No condition data found for %s' % (self.parent.data.data_files[i].name))

    def save_table(self, header, titles, data):
        with open('table.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for i, title in enumerate(titles):
                row = [title]
                for dat in data[i]:
                    row.append(str(dat))
                writer.writerow(row)
