# Standard library imports
import csv

# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QSizePolicy,
    QGridLayout, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QComboBox,
    QCheckBox, QLabel, QLineEdit, QGraphicsDropShadowEffect, QSizePolicy,
    QFormLayout, QHBoxLayout, QMenu, QAction)
from PyQt5.QtCore import QPoint, Qt

# Local application imports
from ada.plotter.main_plot import PlotCanvas
from ada.reader.data_holder import DataHolder
from ada.reader.read_calibration import read_calibration
from ada.components.label import Label, TopLabel, LeftLabel, DelLabel
from ada.components.user_input import TextEntry, SpinBox, DropDown, CheckBox
from ada.components.list import List
from ada.components.spacer import Spacer
from ada.components.button import Button, BigButton
from ada.components.collapsible_box import CollapsibleBox
from ada.components.data_list_item import (DataListItem, ConditionListItem,
    DelListItem)
from ada.gui.error_window import ErrorWindow
from ada.gui.export_window import ExportWindow
from ada.gui.table_window import TableWindow
from ada.gui.fit_window import FitWindow
from ada.gui.load_window import LoadWindow
from ada.gui.file_handler import get_file_names, get_save_file_name
from ada.type_functions import isfloat, isint
import ada.configuration as config


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Algal Data Analyser'
        # Default dimensions
        self.left = 10
        self.top = 10
        self.width = 960
        self.height = 600
        # Container for data
        self.data = DataHolder()
        # Container for condition data
        self.condition_data = DataHolder()
        self.calibration = None
        self.setStyleSheet(config.main_background)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()
        tabs.setStyleSheet(config.tab_style)

        # ---------------------------------------------------------------------
        #                           PLOTTING TAB
        # ---------------------------------------------------------------------

        # Main plotting window
        plot_layout = QGridLayout()
        plot_layout.setContentsMargins(5, 5, 5, 5)
        plot_layout.setSpacing(10)

        # Main plot window (row, column, row extent, column extent)
        self.plot = PlotCanvas(self, width=10, height=4)
        shadow = QGraphicsDropShadowEffect(blurRadius=10, xOffset=3, yOffset=3)
        self.plot.setGraphicsEffect(shadow)
        self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        plot_layout.addWidget(self.plot, 0, 0, 5, 5)

        # Saving options
        save_button = Button('Save', self, 'Save the figure')
        save_button.clicked.connect(self.update_config)
        save_button.clicked.connect(self.save_plot)
        plot_layout.addWidget(save_button, 5, 0)

        # Export options
        export_button = Button('Export', self,
                               'Export the data to CSV')
        export_button.clicked.connect(self.export_files)
        plot_layout.addWidget(export_button, 5, 1)

        # Measure gradient
        measure_button = Button('Measure', self, 'Measure the growth rate')
        measure_button.clicked.connect(self.toggle_cursor)
        measure_button.clicked.connect(self.update_plot)
        plot_layout.addWidget(measure_button, 5, 2)

        # Fit curves
        fit_button = Button('Fit', self, 'Fit the growth curves')
        fit_button.clicked.connect(self.fit_curve)
        plot_layout.addWidget(fit_button, 5, 3)

        # Table output button
        table_button = Button('To Table', self, 
                              'Create a table of growth rates for all curves'
                              '\nConfigure in options tab')
        table_button.clicked.connect(self.update_config)
        table_button.clicked.connect(self.create_table)
        plot_layout.addWidget(table_button, 5, 4)

        data_entry_layout = QVBoxLayout()
        data_entry_layout.setSpacing(5)
        data_entry_layout.setContentsMargins(5,0,5,0)
        # Add data button
        self.data_button = Button('Add Data', self,
                             'Import data for plotting')
        self.data_button.clicked.connect(self.update_config)
        self.data_button.clicked.connect(self.open_data_files)
        self.data_button.clicked.connect(self.update_data_list)
        data_entry_layout.addWidget(self.data_button)
        self.data_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_button.customContextMenuRequested.connect(self.on_context_menu)

        self.clear_menu = QMenu(self)
        self.clear_action = QAction('Clear all', self)
        self.clear_menu.addAction(self.clear_action)

        # List of data in a scrollable area
        self.data_list = List(self)
        self.data_list.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Expanding)
        data_entry_layout.addWidget(self.data_list)

        # Add condition data text
        condition_data_text = TopLabel('Condition Data:', True)
        data_entry_layout.addWidget(condition_data_text)
        # List of condition data
        self.condition_data_list = List(self)
        self.condition_data_list.setSizePolicy(QSizePolicy.Expanding,
                                               QSizePolicy.Expanding)
        data_entry_layout.addWidget(self.condition_data_list)

        calibration_button = Button('Add Calibration Curve', self,
                                    'Set OD to CD conversion from file')
        calibration_button.clicked.connect(self.open_calibration_file)
        data_entry_layout.addWidget(calibration_button)
        self.calibration_file = DelLabel(self)
        self.calibration_file.button.clicked.connect(self.remove_calibration_file)
        self.calibration_file.setFixedHeight(40)
        data_entry_layout.addWidget(self.calibration_file)

        # Plot button
        plot_button = BigButton('Plot!', self, 'Plot the data!')
        plot_button.clicked.connect(self.update_config)
        plot_button.clicked.connect(self.update_plot)
        data_entry_layout.addWidget(plot_button)

        data_entry_widget = QWidget()
        data_entry_widget.setLayout(data_entry_layout)
        plot_layout.addWidget(data_entry_widget, 0, 5, 6, 1)

        plot_widget = QWidget()
        plot_widget.setStyleSheet(config.white_background)
        plot_widget.setLayout(plot_layout)
        tabs.addTab(plot_widget, 'Plotting')

        # ---------------------------------------------------------------------
        #                           OPTIONS TABS
        # ---------------------------------------------------------------------
        
        # --------------- AXIS CONFIGURATION

        # Axis configuration
        axis_v_layout = QVBoxLayout()
        axis_h_layout = QHBoxLayout()
        x_v_layout = QVBoxLayout()
        x_form_layout = QFormLayout()
        y_v_layout = QVBoxLayout()
        y_form_layout = QFormLayout()
        z_v_layout = QVBoxLayout()
        z_form_layout = QFormLayout()

        self.figure_title = TextEntry('Figure title:', self)
        axis_v_layout.addWidget(self.figure_title)

        x_v_layout.addWidget(TopLabel('X (time):'))
        # X axis drop down menu
        self.xaxis_dropdown = DropDown('Variable:', config.xaxis_units, self)
        self.xaxis_dropdown.setCurrentIndex(2)
        x_form_layout.addRow(self.xaxis_dropdown)

        # X axis titles
        self.xaxis_name = TextEntry('Label:', self)
        x_form_layout.addRow(self.xaxis_name)
        self.xaxis_unit = TextEntry('Unit name:', self)
        self.xaxis_unit.setToolTip('Enter "none" for no units')
        x_form_layout.addRow(self.xaxis_unit)

        # X axis range
        self.xaxis_min = TextEntry('Range min:', self)
        x_form_layout.addRow(self.xaxis_min)
        self.xaxis_max = TextEntry('Range max:', self)
        x_form_layout.addRow(self.xaxis_max)

        x_form_widget = QWidget()
        x_form_widget.setLayout(x_form_layout)
        x_v_layout.addWidget(x_form_widget)
        x_v_widget = QWidget()
        x_v_widget.setLayout(x_v_layout)
        axis_h_layout.addWidget(x_v_widget)

        y_v_layout.addWidget(TopLabel('Y (growth):'))
        # Y axis drop down menu
        self.yaxis_dropdown = DropDown('Variable:', [], self)
        y_form_layout.addRow(self.yaxis_dropdown)

        # Y axis titles
        self.yaxis_name = TextEntry('Label:', self)
        y_form_layout.addRow(self.yaxis_name)
        self.yaxis_unit = TextEntry('Unit name:', self)
        self.yaxis_unit.setToolTip('Enter "none" for no units')
        y_form_layout.addRow(self.yaxis_unit)

        # Y axis range
        self.yaxis_min = TextEntry('Range min:', self)
        y_form_layout.addRow(self.yaxis_min)
        self.yaxis_max = TextEntry('Range max:', self)
        y_form_layout.addRow(self.yaxis_max)

        y_form_widget = QWidget()
        y_form_widget.setLayout(y_form_layout)
        y_v_layout.addWidget(y_form_widget)
        y_v_widget = QWidget()
        y_v_widget.setLayout(y_v_layout)
        axis_h_layout.addWidget(Spacer())
        axis_h_layout.addWidget(y_v_widget)

        z_v_layout.addWidget(TopLabel('Y2 (conditions):'))
        # Condition Y axis drop down menu
        self.condition_yaxis_dropdown = DropDown('Variable:', [], self)
        z_form_layout.addRow(self.condition_yaxis_dropdown)

        # Condition Y axis titles
        self.condition_yaxis_name = TextEntry('Label:', self)
        z_form_layout.addRow(self.condition_yaxis_name)
        self.condition_yaxis_unit = TextEntry('Unit name:', self)
        self.xaxis_unit.setToolTip('Enter "none" for no units')
        z_form_layout.addRow(self.condition_yaxis_unit)

        # Condition Y axis range
        self.condition_yaxis_min = TextEntry('Range min:', self)
        z_form_layout.addRow(self.condition_yaxis_min)
        self.condition_yaxis_max = TextEntry('Range max:', self)
        z_form_layout.addRow(self.condition_yaxis_max)

        z_form_widget = QWidget()
        z_form_widget.setLayout(z_form_layout)
        z_v_layout.addWidget(z_form_widget)
        z_v_widget = QWidget()
        z_v_widget.setLayout(z_v_layout)
        axis_h_layout.addWidget(Spacer())
        axis_h_layout.addWidget(z_v_widget)
        axis_h_widget = QWidget()
        axis_h_widget.setLayout(axis_h_layout)
        axis_v_layout.addWidget(axis_h_widget)
        axis_v_layout.addWidget(Spacer())

        axis_box_widget = QWidget()
        axis_box_widget.setStyleSheet(config.white_background)
        axis_box_widget.setLayout(axis_v_layout)
        tabs.addTab(axis_box_widget, 'Axes')

        # --------------- DATA CONFIGURATION

        # Data configuration options
        data_h_layout = QHBoxLayout()
        data_box_layout = QFormLayout()

        # Smooth noisy data button
        self.smooth_data = CheckBox('Data smoothing off/on', self)
        self.smooth_data.setToolTip('Apply Savitzky-Golay to noisy data')
        data_box_layout.addRow(' ', self.smooth_data)

        # Align all data with 0 checkbox
        self.align_data = CheckBox('Alignment at time = 0 on/off', self)
        self.align_data.setToolTip('Start growth curves at 0 time')
        data_box_layout.addRow(' ', self.align_data)

        # Align all data at Y position
        self.y_alignment = TextEntry('Align at Y:', self)
        self.y_alignment.setToolTip('Align all growth curves at given Y value')
        data_box_layout.addRow(self.y_alignment)

        # Condition data downsampling and averaging
        self.condition_average = TextEntry('Condition data time average:', self)
        self.condition_average.setToolTip('Average over a given time window')
        data_box_layout.addRow(self.condition_average)

        self.show_events = CheckBox('Show events off/on', self)
        data_box_layout.addRow(' ', self.show_events)

        download_button = Button(' Download ADA data template ', self)
        download_button.clicked.connect(self.download_template)
        data_box_layout.addRow(' ', download_button)

        data_form_widget = QWidget()
        data_form_widget.setLayout(data_box_layout)
        data_h_layout.addWidget(data_form_widget)

        data_v_layout = QVBoxLayout()
        # Remove any obvious outliers from the growth data
        data_v_layout.addWidget(TopLabel('Data outliers:'))
        data_v_form_layout = QFormLayout()
        self.auto_remove = CheckBox('Auto-remove outliers off/on', self)
        data_v_form_layout.addRow(' ', self.auto_remove)
        self.remove_above = TextEntry('Remove above:', self)
        data_v_form_layout.addRow(self.remove_above)
        self.remove_below = TextEntry('Remove below:', self)
        data_v_form_layout.addRow(self.remove_below)
        data_v_form_widget = QWidget()
        data_v_form_widget.setLayout(data_v_form_layout)
        data_v_layout.addWidget(data_v_form_widget)
        data_v_layout.addWidget(Spacer())

        data_v_widget = QWidget()
        data_v_widget.setLayout(data_v_layout)
        data_h_layout.addWidget(data_v_widget)
        data_h_layout.addWidget(Spacer())

        data_box_widget = QWidget()
        data_box_widget.setStyleSheet(config.white_background)
        data_box_widget.setLayout(data_h_layout)
        tabs.addTab(data_box_widget, 'Data')

        # --------------- LEGEND CONFIGURATION

        # Legend configuration options
        legend_h_layout = QHBoxLayout()
        growth_form_layout = QFormLayout()
        growth_v_layout = QVBoxLayout()
        condition_form_layout = QFormLayout()
        condition_v_layout = QVBoxLayout()

        # Legend on/off checkbox
        growth_v_layout.addWidget(TopLabel('Growth Legend:'))
        self.legend_toggle = CheckBox('Legend on', self)
        growth_form_layout.addRow(' ', self.legend_toggle)

        # Legend options dropdown menu (editable)
        self.legend_names = DropDown('Labels:', [], self)
        self.legend_names.entry.setEditable(True)
        self.legend_names.entry.setInsertPolicy(2)
        self.legend_names.setToolTip('Edit names by changing text '
                                     'and pressing return')
        growth_form_layout.addRow(self.legend_names)

        # Heading for legend
        self.legend_title = TextEntry('Heading:', self)
        growth_form_layout.addRow(self.legend_title)

        # Extra information from header dropdown
        self.extra_info = DropDown('Extra text:', config.info_options, self)
        self.extra_info.setToolTip('Show extra information from '
                                   'the file in the legend')
        growth_form_layout.addRow(self.extra_info)

        # Checkbox to only show extra info
        self.only_extra = CheckBox('Remove labels', self)
        growth_form_layout.addRow(' ', self.only_extra)

        growth_form_widget = QWidget()
        growth_form_widget.setLayout(growth_form_layout)
        growth_v_layout.addWidget(growth_form_widget)
        growth_v_layout.addWidget(Spacer())
        growth_v_widget = QWidget()
        growth_v_widget.setLayout(growth_v_layout)
        legend_h_layout.addWidget(growth_v_widget)

        # Condition legend configuration
        condition_v_layout.addWidget(TopLabel('Condition legend:'))
        self.condition_legend_toggle = CheckBox('Legend on', self)
        condition_form_layout.addRow(' ', self.condition_legend_toggle)

        # Condition legend options dropdown menu
        self.condition_legend_names = DropDown('Labels:', [], self)
        self.condition_legend_names.entry.setEditable(True)
        self.condition_legend_names.entry.setInsertPolicy(2)
        self.condition_legend_names.setToolTip('Edit names by changing text '
                                               'and pressing return')
        condition_form_layout.addRow(self.condition_legend_names)

        # Heading for condition legend
        self.condition_legend_title = TextEntry('Heading:', self)
        condition_form_layout.addRow(self.condition_legend_title)

        self.condition_extra_info = DropDown('Extra text:', config.info_options, self)
        self.condition_extra_info.setToolTip('Show extra information from '
                                             'the file in the legend')
        condition_form_layout.addRow(self.condition_extra_info)

        # Checkbox to only show extra info
        self.condition_only_extra = CheckBox('Remove labels', self)
        condition_form_layout.addRow(' ', self.condition_only_extra)

        condition_form_widget = QWidget()
        condition_form_widget.setLayout(condition_form_layout)
        condition_v_layout.addWidget(condition_form_widget)
        condition_v_layout.addWidget(Spacer())
        condition_v_widget = QWidget()
        condition_v_widget.setLayout(condition_v_layout)
        legend_h_layout.addWidget(condition_v_widget)
        legend_h_layout.addWidget(Spacer())

        legend_box_widget = QWidget()
        legend_box_widget.setStyleSheet(config.white_background)
        legend_box_widget.setLayout(legend_h_layout)
        tabs.addTab(legend_box_widget, 'Legend')

        # --------------- STYLE CONFIGURATION

        # Style configuration
        style_h_layout = QHBoxLayout()
        style_box_layout = QFormLayout()

        # Plot style dropdown menu
        self.style_dropdown = DropDown('Style:', config.style_options, self)
        style_box_layout.addRow(self.style_dropdown)

        # Font style dropdown menu
        self.font_dropdown = DropDown('Font style:', config.font_options, self)
        style_box_layout.addRow(self.font_dropdown)

        # Font size textbox
        self.title_size = SpinBox('Title font size:', 14, 0, 100, self)
        style_box_layout.addRow(self.title_size)

        self.legend_size = SpinBox('Legend font size:', 12, 0, 100, self)
        style_box_layout.addRow(self.legend_size)

        self.label_size = SpinBox('Label font size:', 12, 0, 100, self)
        style_box_layout.addRow(self.label_size)

        # Line width textbox
        self.line_width = SpinBox('Line width:', 2, 0, 20, self)
        style_box_layout.addRow(self.line_width)

        # Condition axis colour
        self.axis_colour = TextEntry('Condition axis color:', self)
        style_box_layout.addRow(self.axis_colour)

        self.grid_toggle = CheckBox('Grid on/off', self)
        style_box_layout.addRow(' ',self.grid_toggle)

        style_box_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        style_box_layout.setLabelAlignment(Qt.AlignCenter)

        style_box_widget = QWidget()
        style_box_widget.setLayout(style_box_layout)

        style_h_layout.addWidget(style_box_widget)
        style_h_layout.addWidget(Spacer())
        style_h_widget = QWidget()
        style_h_widget.setLayout(style_h_layout)
        style_h_widget.setStyleSheet(config.white_background)
        tabs.addTab(style_h_widget, 'Style')

        # --------------- STATS CONFIGURATION

        # Stats configuration
        stats_box_layout = QFormLayout()

        self.std_err = CheckBox('Standard error/deviation', self)
        self.std_err.setToolTip('Checked = show standard error on mean\n'
                                'Unchecked = show standard deviation')
        stats_box_layout.addRow(' ', self.std_err)

        stats_box_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        stats_box_layout.setLabelAlignment(Qt.AlignCenter)

        stats_box_widget = QWidget()
        stats_box_widget.setStyleSheet(config.white_background)
        stats_box_widget.setLayout(stats_box_layout)
        tabs.addTab(stats_box_widget, 'Stats')

        # ----------------------------------
        self.setCentralWidget(tabs)
        self.show()

    # -------------------------------------------------------------------------
    #                           MEMBER FUNCTIONS
    # -------------------------------------------------------------------------

    # Function: Open and read in data files
    def open_data_files(self):
        try:
            self.load = LoadWindow(self, self.data, self.condition_data)
            self.load.show()
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    # Function: Open and read in calibration
    def open_calibration_file(self):
        try:
            self.calibration_file.clear()
            calib_file_name = get_file_names()
            self.calibration_file.setText(calib_file_name[0])
            self.calibration = read_calibration(calib_file_name[0])
            self.update_data_list()
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def remove_calibration_file(self):
        self.calibration_file.clear()
        self.calibration = None

    def on_context_menu(self, point):
        # show context menu
        action = self.clear_menu.exec_(self.data_button.mapToGlobal(point))
        if action == self.clear_action:
            self.data.clear()
            self.update_data_list()
            self.condition_data.clear()
            self.update_condition_data_list()

    # Function: Update the main plot
    def update_plot(self):
        try:
            self.plot.plot(self.data, self.condition_data)
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    # Function: Save the main plot
    def save_plot(self):
        try:
            self.plot.save()
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    # Function: Update the list of data files and associated options
    def update_data_list(self):
        self.data_list.clear()
        self.yaxis_dropdown.clear()
        self.legend_names.clear()
        for i, data in enumerate(self.data.data_files):
            data_list_item = DataListItem(data.name.split('/')[-1], i, self)
            self.data_list.addItem(data_list_item.item)
            self.data_list.setItemWidget(data_list_item.item,
                                         data_list_item.widget)
            self.legend_names.addItem(data.label)
            if i > 0:
                continue
            contains_od = False
            contains_cd = False
            for sig in reversed(data.signals):
                self.yaxis_dropdown.addItem(sig.name)
                if sig.name == 'OD':
                    self.yaxis_dropdown.addItem('ln(OD/OD0)')
                    contains_od = True
                if sig.name == 'CD':
                    contains_cd = True
            if contains_od and not contains_cd and self.calibration is not None:
                self.yaxis_dropdown.addItem('CD')

    # Function: Update the list of condition data and associated options
    def update_condition_data_list(self):
        self.condition_data_list.clear()
        self.condition_yaxis_dropdown.clear()
        self.condition_legend_names.clear()
        for i, data in enumerate(self.condition_data.data_files):
            data_list_item = ConditionListItem(data.name.split('/')[-1], self)
            self.condition_data_list.addItem(data_list_item.item)
            self.condition_data_list.setItemWidget(data_list_item.item,
                                         data_list_item.widget)
            self.condition_legend_names.addItem(data.label)
            if i > 0:
                continue
            for sig in data.signals:
                self.condition_yaxis_dropdown.addItem(sig.name)

    def get_data_row(self):
        # Horrible stuff to get list item
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = self.data_list.viewport().mapFromGlobal(gp)
        row = self.data_list.row(self.data_list.itemAt(lp))
        return row

    def get_condition_row(self):
        # Horrible stuff to get list item
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = self.condition_data_list.viewport().mapFromGlobal(gp)
        row = self.condition_data_list.row(self.condition_data_list.itemAt(lp))
        return row

    # Function: Remove file from list of data
    def remove_item(self):
        row = self.get_data_row()
        for i, data in enumerate(self.data.data_files):
            if i != row:
                continue
            self.data.delete_data(i)
        self.update_data_list()

    # Function: Remove file from list of data
    def remove_replicate(self, index):
        row = self.get_data_row()
        for i, data in enumerate(self.data.data_files):
            if i != row:
                continue
            self.data.delete_replicate(i, index)
        self.update_data_list()

    # Function: Remove file from list of condition data
    def remove_condition_item(self):
        row = self.get_condition_row()
        for i, data in enumerate(self.condition_data.data_files):
            if i != row:
                continue
            self.condition_data.delete_data(i)
        self.update_condition_data_list()

    def add_to_item(self):
        row = self.get_data_row()
        # Open file with file handler
        self.load = LoadWindow(self, self.data, self.condition_data, row)
        self.load.show()

    def download_template(self):
        template = ['Name,,Title,,Reactor,,Profile,\n',
                    'Date,2020-01-15,Time,18:18:18\n',
                    'Time [hr],OD [],Conditions\n']
        file_name = get_save_file_name()
        file_name = file_name.split('.')[0] + '.csv'
        with open(file_name, 'w', newline='') as csvfile:
            for row in template:
                csvfile.write(row)

    # Function: Toggle cursor on and off
    def toggle_cursor(self):
        config.do_fit = False
        config.cursor = not config.cursor

    def fit_curve(self):
        self.fit = FitWindow(self)
        self.fit.show()

    # Function: Toggle grid on and off
    def create_table(self):
        self.table = TableWindow(self)
        self.table.show()

    # Function: Export data to csv format
    def export_files(self):
        self.export = ExportWindow(self)
        self.export.show()

    # Function: Update the global configuration
    def update_config(self):
        config.title = self.figure_title.text()

        # x axis config
        config.xvar = self.xaxis_dropdown.currentText()
        config.xname = self.xaxis_name.text()
        config.xunit = self.xaxis_unit.text()
        if(isfloat(self.xaxis_min.text())):
            config.xmin = float(self.xaxis_min.text())
        else:
            config.xmin = -1
        if(isfloat(self.xaxis_max.text())):
            config.xmax = float(self.xaxis_max.text())
        else:
            config.xmax = -1

        # y axis config
        config.yvar = self.yaxis_dropdown.currentText()
        config.yname = self.yaxis_name.text()
        config.yunit = self.yaxis_unit.text()
        if(isfloat(self.yaxis_min.text())):
            config.ymin = float(self.yaxis_min.text())
        else:
            config.ymin = -1
        if(isfloat(self.yaxis_max.text())):
            config.ymax = float(self.yaxis_max.text())
        else:
            config.ymax = -1

        # Condition y axis config
        config.condition_yvar = \
            self.condition_yaxis_dropdown.currentText()
        config.condition_yname = self.condition_yaxis_name.text()
        config.condition_yunit = self.condition_yaxis_unit.text()
        if(isfloat(self.condition_yaxis_min.text())):
            config.condition_ymin = \
                float(self.condition_yaxis_min.text())
        else:
            config.condition_ymin = -1
        if(isfloat(self.condition_yaxis_max.text())):
            config.condition_ymax = float(self.condition_yaxis_max.text())
        else:
            config.condition_ymax = -1

        # Data config
        config.smooth = self.smooth_data.isChecked()
        config.align = self.align_data.isChecked()
        if(isfloat(self.y_alignment.text())):
            config.y_alignment = float(self.y_alignment.text())
        else:
            config.y_alignment = -1
        config.auto_remove = self.auto_remove.isChecked()
        if(isfloat(self.remove_above.text())):
            config.remove_above = float(self.remove_above.text())
        else:
            config.remove_above = -1
        if(isfloat(self.remove_below.text())):
            config.remove_below = float(self.remove_below.text())
        else:
            config.remove_below = -1
        if(isfloat(self.condition_average.text())):
            config.condition_average = \
                float(self.condition_average.text())
        else:
            config.condition_average = -1
        config.show_events = self.show_events.isChecked()

        # Legend config
        config.legend = self.legend_toggle.isChecked()
        config.condition_legend = \
            self.condition_legend_toggle.isChecked()
        config.legend_title = self.legend_title.text()
        if(config.legend_title.lower() == 'none'):
            config.legend_title = ''
        config.condition_legend_title = self.condition_legend_title.text()
        if(config.condition_legend_title.lower() == 'none'):
            config.condition_legend_title = ''
        config.label_names.clear()
        for i in range(self.legend_names.count()):
            config.label_names.append(self.legend_names.itemText(i))
        config.condition_label_names.clear()
        for i in range(self.condition_legend_names.count()):
            config.condition_label_names.append(
                self.condition_legend_names.itemText(i)
            )
        config.extra_info = self.extra_info.currentText()
        config.condition_extra_info = \
            self.condition_extra_info.currentText()
        config.only_extra = self.only_extra.isChecked()
        config.condition_only_extra = \
            self.condition_only_extra.isChecked()

        # Style config
        config.style = self.style_dropdown.currentText()
        config.font_style = self.font_dropdown.currentText()
        if(isfloat(self.title_size.text())):
            config.title_size = float(self.title_size.text())
        else:
            config.title_size = -1
        if(isfloat(self.legend_size.text())):
            config.legend_size = float(self.legend_size.text())
        else:
            config.legend_size = -1
        if(isfloat(self.label_size.text())):
            config.label_size = float(self.label_size.text())
        else:
            config.label_size = -1
        if(isfloat(self.line_width.text())):
            config.line_width = float(self.line_width.text())
        else:
            config.line_width = -1
        config.axis_colour = self.axis_colour.text()
        config.grid = self.grid_toggle.isChecked()

        # Stats config
        config.std_err = self.std_err.isChecked()

        config.do_fit = False
