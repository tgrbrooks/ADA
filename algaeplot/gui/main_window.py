# Standard library imports

# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QSizePolicy,
    QGridLayout, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QComboBox,
    QCheckBox, QLabel, QLineEdit)
from PyQt5.QtCore import QPoint

# Local application imports
from algaeplot.plotter.main_plot import PlotCanvas
from algaeplot.reader.data_holder import DataHolder
from algaeplot.components.label import Label
from algaeplot.components.spacer import Spacer
from algaeplot.components.button import Button, BigButton
from algaeplot.components.collapsible_box import CollapsibleBox
from algaeplot.components.data_list_item import DataListItem
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
        self.width = 960
        self.height = 600
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
        plot_layout.setContentsMargins(0, 0, 0, 0)
        plot_layout.setSpacing(20)

        # Main plot window (row, column, row extent, column extent)
        self.plot = PlotCanvas(self, width=10, height=4)
        plot_layout.addWidget(self.plot, 0, 0, 6, 5)

        # Add data button
        data_button = Button('Add Data', self,
                             'Import data for plotting')
        data_button.clicked.connect(self.update_config)
        data_button.clicked.connect(self.open_data_files)
        data_button.clicked.connect(self.update_data_list)
        plot_layout.addWidget(data_button, 0, 5)

        # List of data in a scrollable area
        self.data_list = QListWidget(self)
        self.data_list.clicked.connect(self.remove_item)
        self.data_list.setToolTip('Click to remove')
        plot_layout.addWidget(self.data_list, 1, 5)

        # Add condition data text
        condition_data_text = Label('Condition Data:', True)
        plot_layout.addWidget(condition_data_text, 3, 5)
        # List of condition data
        self.condition_data_list = QListWidget(self)
        self.condition_data_list.clicked.connect(self.remove_condition_item)
        self.condition_data_list.setToolTip('Click to remove')
        plot_layout.addWidget(self.condition_data_list, 4, 5)

        # Plot button
        plot_button = BigButton('Plot!', self, 'Plot the data!')
        plot_button.clicked.connect(self.update_config)
        plot_button.clicked.connect(self.update_plot)
        plot_layout.addWidget(plot_button, 5, 5, 2, 1)

        # Saving options
        save_button = Button('Save', self, 'Save the figure')
        save_button.clicked.connect(self.update_config)
        save_button.clicked.connect(self.save_plot)
        plot_layout.addWidget(save_button, 6, 0)

        # Export options
        export_button = Button('Export', self,
                               'Export the data to CSV')
        export_button.clicked.connect(self.export_files)
        plot_layout.addWidget(export_button, 6, 1)

        # Measure gradient
        measure_button = Button('Measure', self, 'Measure the growth rate')
        measure_button.clicked.connect(self.toggle_cursor)
        measure_button.clicked.connect(self.update_plot)
        plot_layout.addWidget(measure_button, 6, 2)

        # Fit curves
        fit_button = Button('Fit', self, 'Fit the growth curves')
        fit_button.clicked.connect(self.fit_curve)
        plot_layout.addWidget(fit_button, 6, 3)

        # Table output button
        table_button = Button('To Table', self, 
                              'Create a table of growth rates for all curves'
                              '\nConfigure in options tab')
        table_button.clicked.connect(self.update_config)
        table_button.clicked.connect(self.create_table)
        plot_layout.addWidget(table_button, 6, 4)

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

        axis_box_layout.addWidget(Label('Figure title:', True), 0, 0)
        self.figure_title = QLineEdit(self)
        axis_box_layout.addWidget(self.figure_title, 0, 1, 1, 2)
        axis_box_layout.addWidget(Label('Variable'), 1, 1)
        axis_box_layout.addWidget(Label('Label name'), 1, 2)
        axis_box_layout.addWidget(Label('Unit name'), 1, 3)
        axis_box_layout.addWidget(Label('Range min'), 1, 4)
        axis_box_layout.addWidget(Label('Range max'), 1, 5)
        axis_box_layout.addWidget(Label('X:'), 2, 0)
        axis_box_layout.addWidget(Label('Y:'), 3, 0)
        axis_box_layout.addWidget(Label('Y2 (conditions):'), 4, 0)

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
        data_box_layout = QGridLayout()
        data_box_layout.setContentsMargins(5, 5, 5, 5)
        data_box_layout.setSpacing(5)

        # Smooth noisy data button
        data_box_layout.addWidget(Label('Smooth data:'), 0, 0)
        self.smooth_data = QCheckBox(self)
        self.smooth_data.setToolTip('Apply Savitzky-Golay to noisy data')
        data_box_layout.addWidget(self.smooth_data, 0, 1)

        # Align all data with 0 checkbox
        data_box_layout.addWidget(Label('Align at time = 0:'), 1, 0)
        self.align_data = QCheckBox(self)
        self.align_data.setToolTip('Start growth curves at 0 time')
        data_box_layout.addWidget(self.align_data, 1, 1)

        # Align all data at Y position
        data_box_layout.addWidget(Label('Align at Y ='), 1, 2)
        self.y_alignment = QLineEdit(self)
        self.y_alignment.setToolTip('Align all growth curves at given Y value')
        data_box_layout.addWidget(self.y_alignment, 1, 3)

        # Remove any obvious outliers from the growth data
        data_box_layout.addWidget(Label('Data outliers:'), 2, 0)
        data_box_layout.addWidget(Label('Auto remove:'), 3, 0)
        self.auto_remove = QCheckBox(self)
        data_box_layout.addWidget(self.auto_remove, 3, 1)
        data_box_layout.addWidget(Label('Remove above:'), 3, 2)
        self.remove_above = QLineEdit(self)
        data_box_layout.addWidget(self.remove_above, 3, 3)
        data_box_layout.addWidget(Label('Remove below:'), 3, 4)
        self.remove_below = QLineEdit(self)
        data_box_layout.addWidget(self.remove_below, 3, 5)

        # Condition data downsampling and averaging
        data_box_layout.addWidget(Label('Condition data:'), 4, 0)
        data_box_layout.addWidget(Label('Time average:'), 4, 1)
        self.condition_average = QLineEdit(self)
        self.condition_average.setToolTip('Average over time window')
        data_box_layout.addWidget(self.condition_average, 4, 2)

        data_box_layout.addWidget(Label('Show Events:'), 5, 0)
        self.show_events = QCheckBox(self)
        data_box_layout.addWidget(self.show_events, 5, 1)

        data_box_layout.addWidget(Spacer(), 6, 5)

        data_box_widget = QWidget()
        data_box_widget.setLayout(data_box_layout)
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
        style_box_layout = QGridLayout()
        style_box_layout.setContentsMargins(5, 5, 5, 5)
        style_box_layout.setSpacing(5)

        # Plot style dropdown menu
        style_box_layout.addWidget(Label('Style:'), 0, 0)
        self.style_dropdown = QComboBox(self)
        self.style_dropdown.addItems(config.style_options)
        style_box_layout.addWidget(self.style_dropdown, 0, 1)

        # Font style dropdown menu
        style_box_layout.addWidget(Label('Font style:'), 1, 0)
        self.font_dropdown = QComboBox(self)
        self.font_dropdown.addItems(config.font_options)
        style_box_layout.addWidget(self.font_dropdown, 1, 1)

        # Font size textbox
        style_box_layout.addWidget(Label('Title font size:'), 2, 0)
        self.title_size = QLineEdit(self)
        style_box_layout.addWidget(self.title_size, 2, 1)

        style_box_layout.addWidget(Label('Legend font size:'), 3, 0)
        self.legend_size = QLineEdit(self)
        style_box_layout.addWidget(self.legend_size, 3, 1)

        style_box_layout.addWidget(Label('Label font size:'), 4, 0)
        self.label_size = QLineEdit(self)
        style_box_layout.addWidget(self.label_size, 4, 1)

        # Line width textbox
        style_box_layout.addWidget(Label('Line width:'), 5, 0)
        self.line_width = QLineEdit(self)
        style_box_layout.addWidget(self.line_width, 5, 1)

        # Condition axis colour
        style_box_layout.addWidget(Label('Condition axis colour:'), 6, 0)
        self.axis_colour = QLineEdit(self)
        style_box_layout.addWidget(self.axis_colour, 6, 1)

        style_box_layout.addWidget(Label('Grid:'), 7, 0)
        self.grid_toggle = QCheckBox(self)
        style_box_layout.addWidget(self.grid_toggle, 7, 1)

        style_box_layout.addWidget(Spacer(), 8, 2)

        style_box_widget = QWidget()
        style_box_widget.setLayout(style_box_layout)
        tabs.addTab(style_box_widget, 'Style')

        # --------------- STATS CONFIGURATION

        # Stats configuration
        stats_box_layout = QGridLayout()
        stats_box_layout.setContentsMargins(5, 5, 5, 5)
        stats_box_layout.setSpacing(5)

        stats_box_layout.addWidget(Label('Standard error:'), 0, 0)
        self.std_err = QCheckBox(self)
        self.std_err.setToolTip('Checked = show standard error on mean\n'
                                'Unchecked = show standard deviation')
        stats_box_layout.addWidget(self.std_err, 0, 1)

        stats_box_layout.addWidget(Spacer(), 1, 2)

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
            self.condition_data_list.addItem(data.name.split('/')[-1])
            self.condition_legend_names.addItem(data.label)
            if i > 0:
                continue
            for sig in data.signals:
                self.condition_yaxis_dropdown.addItem(sig.name)

    # Function: Remove file from list of data
    def remove_item(self):
        # Horrible stuff to get list item
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = self.data_list.viewport().mapFromGlobal(gp)
        row = self.data_list.row(self.data_list.itemAt(lp))
        for i, data in enumerate(self.data.data_files):
            if i != row:
                continue
            self.data.delete_data(i)
        self.update_data_list()

    # Function: Remove file from list of data
    def remove_replicate(self, index):
        # Horrible stuff to get list item
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = self.data_list.viewport().mapFromGlobal(gp)
        row = self.data_list.row(self.data_list.itemAt(lp))
        for i, data in enumerate(self.data.data_files):
            if i != row:
                continue
            self.data.delete_replicate(i, index)
        self.update_data_list()

    # Function: Remove file from list of condition data
    def remove_condition_item(self, index):
        for i, data in enumerate(self.condition_data.data_files):
            if i != index.row():
                continue
            self.condition_data.delete_data(i)
        self.update_condition_data_list()

    def add_to_item(self):
        # Horrible stuff to get list item
        widget = self.sender()
        gp = widget.mapToGlobal(QPoint())
        lp = self.data_list.viewport().mapFromGlobal(gp)
        row = self.data_list.row(self.data_list.itemAt(lp))
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
