# Standard library imports

# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QSizePolicy,
    QGridLayout, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QComboBox,
    QCheckBox, QLabel, QLineEdit, QGraphicsDropShadowEffect, QSizePolicy,
    QFormLayout, QHBoxLayout)
from PyQt5.QtCore import QPoint, Qt

# Local application imports
from algaeplot.plotter.main_plot import PlotCanvas
from algaeplot.reader.data_holder import DataHolder
from algaeplot.components.label import Label, TopLabel, LeftLabel
from algaeplot.components.user_input import TextEntry, SpinBox, DropDown, CheckBox
from algaeplot.components.list import List
from algaeplot.components.spacer import Spacer
from algaeplot.components.button import Button, BigButton
from algaeplot.components.collapsible_box import CollapsibleBox
from algaeplot.components.data_list_item import DataListItem, ConditionListItem
from algaeplot.gui.error_window import ErrorWindow
from algaeplot.gui.export_window import ExportWindow
from algaeplot.gui.table_window import TableWindow
from algaeplot.gui.fit_window import FitWindow
from algaeplot.gui.load_window import LoadWindow
from algaeplot.type_functions import isfloat, isint
import algaeplot.configuration as config


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Algae Plotter'
        # Default dimensions
        self.left = 10
        self.top = 10
        self.width = 1120
        self.height = 630
        # Container for data
        self.data = DataHolder()
        # Container for condition data
        self.condition_data = DataHolder()
        #self.setStyleSheet(config.main_background)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()

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
        plot_layout.addWidget(self.plot, 0, 0, 16, 25)

        # Saving options
        save_button = Button('Save', self, 'Save the figure')
        save_button.clicked.connect(self.update_config)
        save_button.clicked.connect(self.save_plot)
        plot_layout.addWidget(save_button, 16, 0, 2, 5)

        # Export options
        export_button = Button('Export', self,
                               'Export the data to CSV')
        export_button.clicked.connect(self.export_files)
        plot_layout.addWidget(export_button, 16, 5, 2, 5)

        # Measure gradient
        measure_button = Button('Measure', self, 'Measure the growth rate')
        measure_button.clicked.connect(self.toggle_cursor)
        measure_button.clicked.connect(self.update_plot)
        plot_layout.addWidget(measure_button, 16, 10, 2, 5)

        # Fit curves
        fit_button = Button('Fit', self, 'Fit the growth curves')
        fit_button.clicked.connect(self.fit_curve)
        plot_layout.addWidget(fit_button, 16, 15, 2, 5)

        # Table output button
        table_button = Button('To Table', self, 
                              'Create a table of growth rates for all curves'
                              '\nConfigure in options tab')
        table_button.clicked.connect(self.update_config)
        table_button.clicked.connect(self.create_table)
        plot_layout.addWidget(table_button, 16, 20, 2, 5)

        # Add data button
        data_button = Button('Add Data', self,
                             'Import data for plotting')
        data_button.clicked.connect(self.update_config)
        data_button.clicked.connect(self.open_data_files)
        data_button.clicked.connect(self.update_data_list)
        plot_layout.addWidget(data_button, 0, 25, 2, 7)

        # List of data in a scrollable area
        self.data_list = List(self)
        plot_layout.addWidget(self.data_list, 2, 25, 6, 7)

        # Add condition data text
        condition_data_text = TopLabel('Condition Data:', True)
        plot_layout.addWidget(condition_data_text, 8, 25, 1, 7)
        # List of condition data
        self.condition_data_list = List(self)
        plot_layout.addWidget(self.condition_data_list, 9, 25, 6, 7)

        # Plot button
        plot_button = BigButton('Plot!', self, 'Plot the data!')
        plot_button.clicked.connect(self.update_config)
        plot_button.clicked.connect(self.update_plot)
        plot_layout.addWidget(plot_button, 15, 25, 3, 7)

        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        tabs.addTab(plot_widget, 'Plotting')

        # ---------------------------------------------------------------------
        #                           OPTIONS TABS
        # ---------------------------------------------------------------------
        
        # --------------- AXIS CONFIGURATION

        # Axis configuration
        axis_box_layout = QGridLayout()
        axis_box_layout.setContentsMargins(5, 5, 5, 5)
        axis_box_layout.setSpacing(5)

        axis_box_layout.addWidget(LeftLabel('Figure title:', True), 0, 0)
        self.figure_title = QLineEdit(self)
        axis_box_layout.addWidget(self.figure_title, 0, 1, 1, 1)

        axis_box_layout.addWidget(TopLabel('Variable'), 1, 1)
        axis_box_layout.addWidget(TopLabel('Label name'), 1, 2)
        axis_box_layout.addWidget(TopLabel('Unit name'), 1, 3)
        axis_box_layout.addWidget(TopLabel('Range min'), 1, 4)
        axis_box_layout.addWidget(TopLabel('Range max'), 1, 5)
        axis_box_layout.addWidget(LeftLabel('X:'), 2, 0)
        axis_box_layout.addWidget(LeftLabel('Y:'), 3, 0)
        axis_box_layout.addWidget(LeftLabel('Y2 (conditions):'), 4, 0)

        # X axis drop down menu
        self.xaxis_dropdown = QComboBox(self)
        self.xaxis_dropdown.addItems(config.xaxis_units)
        axis_box_layout.addWidget(self.xaxis_dropdown, 2, 1)

        # X axis titles
        self.xaxis_name = QLineEdit(self)
        axis_box_layout.addWidget(self.xaxis_name, 2, 2)
        self.xaxis_unit = QLineEdit(self)
        self.xaxis_unit.setToolTip('Enter "none" for no units')
        axis_box_layout.addWidget(self.xaxis_unit, 2, 3)

        # X axis range
        self.xaxis_min = QLineEdit(self)
        axis_box_layout.addWidget(self.xaxis_min, 2, 4)
        self.xaxis_max = QLineEdit(self)
        axis_box_layout.addWidget(self.xaxis_max, 2, 5)

        # Y axis drop down menu
        self.yaxis_dropdown = QComboBox(self)
        axis_box_layout.addWidget(self.yaxis_dropdown, 3, 1)

        # Y axis titles
        self.yaxis_name = QLineEdit(self)
        axis_box_layout.addWidget(self.yaxis_name, 3, 2)
        self.yaxis_unit = QLineEdit(self)
        self.yaxis_unit.setToolTip('Enter "none" for no units')
        axis_box_layout.addWidget(self.yaxis_unit, 3, 3)

        # Y axis range
        self.yaxis_min = QLineEdit(self)
        axis_box_layout.addWidget(self.yaxis_min, 3, 4)
        self.yaxis_max = QLineEdit(self)
        axis_box_layout.addWidget(self.yaxis_max, 3, 5)

        # Condition Y axis drop down menu
        self.condition_yaxis_dropdown = QComboBox(self)
        axis_box_layout.addWidget(self.condition_yaxis_dropdown, 4, 1)

        # Condition Y axis titles
        self.condition_yaxis_name = QLineEdit(self)
        axis_box_layout.addWidget(self.condition_yaxis_name, 4, 2)
        self.condition_yaxis_unit = QLineEdit(self)
        self.xaxis_unit.setToolTip('Enter "none" for no units')
        axis_box_layout.addWidget(self.condition_yaxis_unit, 4, 3)

        # Condition Y axis range
        self.condition_yaxis_min = QLineEdit(self)
        axis_box_layout.addWidget(self.condition_yaxis_min, 4, 4)
        self.condition_yaxis_max = QLineEdit(self)
        axis_box_layout.addWidget(self.condition_yaxis_max, 4, 5)

        axis_box_layout.addWidget(Spacer(), 5, 6)

        axis_box_widget = QWidget()
        axis_box_widget.setLayout(axis_box_layout)
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
        data_box_widget.setLayout(data_h_layout)
        tabs.addTab(data_box_widget, 'Data')

        # --------------- LEGEND CONFIGURATION

        # Legend configuration options
        legend_box_layout = QGridLayout()
        legend_box_layout.setContentsMargins(5, 5, 5, 5)
        legend_box_layout.setSpacing(5)

        # Legend on/off checkbox
        legend_box_layout.addWidget(Label('Growth Legend:'), 1, 0)
        legend_box_layout.addWidget(Label('On:'), 0, 1)
        self.legend_toggle = QCheckBox(self)
        legend_box_layout.addWidget(self.legend_toggle, 1, 1)

        # Legend options dropdown menu (editable)
        legend_box_layout.addWidget(Label('Titles:'), 0, 2)
        self.legend_names = QComboBox(self)
        self.legend_names.setEditable(True)
        self.legend_names.setInsertPolicy(2)
        self.legend_names.setToolTip('Edit names by changing text '
                                     'and pressing return')
        legend_box_layout.addWidget(self.legend_names, 1, 2, 1, 2)

        # Heading for legend
        legend_box_layout.addWidget(Label('Header:'), 0, 4)
        self.legend_title = QLineEdit(self)
        legend_box_layout.addWidget(self.legend_title, 1, 4)

        # Extra information from header dropdown
        legend_box_layout.addWidget(Label('Extra info:'), 0, 5)
        self.extra_info = QComboBox(self)
        self.extra_info.addItems(config.info_options)
        self.extra_info.setToolTip('Show extra information from '
                                   'the file in the legend')
        legend_box_layout.addWidget(self.extra_info, 1, 5)

        # Checkbox to only show extra info
        legend_box_layout.addWidget(Label('Only extra info:'), 0, 6)
        self.only_extra = QCheckBox(self)
        legend_box_layout.addWidget(self.only_extra, 1, 6)

        # Condition legend configuration
        legend_box_layout.addWidget(Label('Condition legend:'), 2, 0)
        self.condition_legend_toggle = QCheckBox(self)
        legend_box_layout.addWidget(self.condition_legend_toggle, 2, 1)

        # Condition legend options dropdown menu
        self.condition_legend_names = QComboBox(self)
        self.condition_legend_names.setEditable(True)
        self.condition_legend_names.setInsertPolicy(2)
        self.condition_legend_names.setToolTip('Edit names by changing text '
                                               'and pressing return')
        legend_box_layout.addWidget(self.condition_legend_names, 2, 2, 1, 2)

        # Heading for condition legend
        self.condition_legend_title = QLineEdit(self)
        legend_box_layout.addWidget(self.condition_legend_title, 2, 4)

        self.condition_extra_info = QComboBox(self)
        self.condition_extra_info.addItems(config.info_options)
        self.condition_extra_info.setToolTip('Show extra information from '
                                             'the file in the legend')
        legend_box_layout.addWidget(self.condition_extra_info, 2, 5)

        # Checkbox to only show extra info
        self.condition_only_extra = QCheckBox(self)
        legend_box_layout.addWidget(self.condition_only_extra, 2, 6)

        legend_box_layout.addWidget(Spacer(), 3, 7)

        legend_box_widget = QWidget()
        legend_box_widget.setLayout(legend_box_layout)
        tabs.addTab(legend_box_widget, 'Legend')

        # --------------- STYLE CONFIGURATION

        # Style configuration
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
        tabs.addTab(style_box_widget, 'Style')

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
            for sig in reversed(data.signals):
                self.yaxis_dropdown.addItem(sig.name)
                if sig.name == 'OD':
                    self.yaxis_dropdown.addItem('ln(OD/OD0)')

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
