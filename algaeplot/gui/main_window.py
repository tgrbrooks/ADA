# Standard library imports

# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QSizePolicy,
    QGridLayout, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QComboBox,
    QCheckBox, QLabel, QLineEdit)
from PyQt5.QtCore import QPoint

# Local application imports
from algaeplot.plotter.main_plot import PlotCanvas
from algaeplot.reader.data_holder import DataHolder
from algaeplot.gui.configuration import Configuration
from algaeplot.gui.error_window import ErrorWindow
from algaeplot.gui.label import Label
from algaeplot.gui.type_functions import isfloat, isint
from algaeplot.gui.collapsible_box import CollapsibleBox
from algaeplot.gui.data_list_item import DataListItem
from algaeplot.gui.export_window import ExportWindow
from algaeplot.gui.table_window import TableWindow
from algaeplot.gui.fit_window import FitWindow
from algaeplot.gui.load_window import LoadWindow


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
        self.data_list = QListWidget(self)
        # Container for condition data
        self.condition_data = DataHolder()
        self.condition_data_list = QListWidget(self)
        self.config = Configuration()
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()

        default_font = 'font-size: 14pt; font-family: Courier;'
        big_font = 'font-size: 28pt; font-family: Courier;'

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
        data_button = QPushButton('Add Data', self)
        data_button.clicked.connect(self.update_config)
        data_button.clicked.connect(self.open_data_files)
        data_button.clicked.connect(self.update_data_list)
        data_button.setToolTip('Import data for plotting')
        data_button.setStyleSheet(default_font)
        plot_layout.addWidget(data_button, 0, 5)

        # Configure list behaviour
        self.data_list.clicked.connect(self.remove_item)

        # List of data in a scrollable area
        list_scroll = QScrollArea(self)
        list_scroll.setWidgetResizable(True)
        scroll_content = QWidget(list_scroll)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)
        scroll_layout.addWidget(self.data_list)
        list_scroll.setWidget(scroll_content)
        list_scroll.setToolTip('Click to remove')
        plot_layout.addWidget(list_scroll, 1, 5)

        # Add condition data text
        condition_data_text = Label('Condition Data:', True)
        plot_layout.addWidget(condition_data_text, 3, 5)
        # Configure list behaviour
        self.condition_data_list.clicked.connect(self.remove_condition_item)

        # List of condition data
        condition_list_scroll = QScrollArea(self)
        condition_list_scroll.setWidgetResizable(True)
        condition_scroll_content = QWidget(condition_list_scroll)
        condition_scroll_layout = QVBoxLayout(condition_scroll_content)
        condition_scroll_content.setLayout(condition_scroll_layout)
        condition_scroll_layout.addWidget(self.condition_data_list)
        condition_list_scroll.setWidget(condition_scroll_content)
        condition_list_scroll.setToolTip('Click to remove')
        plot_layout.addWidget(condition_list_scroll, 4, 5)

        # Plot button
        plot_button = QPushButton('Plot!', self)
        plot_button.clicked.connect(self.update_config)
        plot_button.clicked.connect(self.update_plot)
        plot_button.setToolTip('Plot the data!')
        plot_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        plot_button.setStyleSheet(big_font)
        plot_layout.addWidget(plot_button, 5, 5, 2, 1)

        # Saving options
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.update_config)
        save_button.clicked.connect(self.save_plot)
        save_button.setToolTip('Save the figure')
        save_button.setStyleSheet(default_font)
        plot_layout.addWidget(save_button, 6, 0)

        # Export options
        export_button = QPushButton('Export', self)
        export_button.clicked.connect(self.export_files)
        export_button.setToolTip('Export the data to another file type')
        export_button.setStyleSheet(default_font)
        plot_layout.addWidget(export_button, 6, 1)

        # Measure gradient
        measure_button = QPushButton('Measure', self)
        measure_button.clicked.connect(self.toggle_cursor)
        measure_button.clicked.connect(self.update_plot)
        measure_button.setToolTip('Measure the growth rate')
        measure_button.setStyleSheet(default_font)
        plot_layout.addWidget(measure_button, 6, 2)

        # Fit curves
        fit_button = QPushButton('Fit', self)
        fit_button.clicked.connect(self.fit_curve)
        fit_button.setToolTip('Fit the growth curves')
        fit_button.setStyleSheet(default_font)
        plot_layout.addWidget(fit_button, 6, 3)

        # Table output button
        table_button = QPushButton('To Table', self)
        table_button.clicked.connect(self.update_config)
        table_button.clicked.connect(self.create_table)
        table_button.setToolTip('Create a table of growth rates for all curves'
                                '\nConfigure in options tab')
        table_button.setStyleSheet('font-size: 14pt; font-family: Courier;')
        plot_layout.addWidget(table_button, 6, 4)

        # ---------------------------------------------------------------------
        #                           OPTIONS TAB
        # ---------------------------------------------------------------------

        # Plotting options window
        options_layout = QGridLayout()
        options_layout.setContentsMargins(5, 5, 5, 5)
        options_layout.setSpacing(5)

        options_scroll = QScrollArea(self)
        options_scroll.setWidgetResizable(True)

        # Figure title
        options_layout.addWidget(Label('Figure title:', True), 0, 0)
        self.figure_title = QLineEdit(self)
        options_layout.addWidget(self.figure_title, 0, 1, 1, 2)

        # --------------- AXIS CONFIGURATION

        # Axis configuration
        axis_box = CollapsibleBox('Axis configuration:')
        options_layout.addWidget(axis_box, 1, 0, 1, 6)
        axis_box_layout = QGridLayout()
        axis_box_layout.addWidget(Label('Variable'), 0, 1)
        axis_box_layout.addWidget(Label('Label name'), 0, 2)
        axis_box_layout.addWidget(Label('Unit name'), 0, 3)
        axis_box_layout.addWidget(Label('Range min'), 0, 4)
        axis_box_layout.addWidget(Label('Range max'), 0, 5)
        axis_box_layout.addWidget(Label('X:'), 1, 0)
        axis_box_layout.addWidget(Label('Y:'), 2, 0)
        axis_box_layout.addWidget(Label('Y2 (conditions):'), 3, 0)

        # X axis drop down menu
        self.xaxis_dropdown = QComboBox(self)
        self.xaxis_dropdown.addItem("seconds")
        self.xaxis_dropdown.addItem("minutes")
        self.xaxis_dropdown.addItem("hours")
        self.xaxis_dropdown.addItem("days")
        axis_box_layout.addWidget(self.xaxis_dropdown, 1, 1)

        # X axis titles
        self.xaxis_name = QLineEdit(self)
        axis_box_layout.addWidget(self.xaxis_name, 1, 2)
        self.xaxis_unit = QLineEdit(self)
        self.xaxis_unit.setToolTip('Enter "none" for no units')
        axis_box_layout.addWidget(self.xaxis_unit, 1, 3)

        # X axis range
        self.xaxis_min = QLineEdit(self)
        axis_box_layout.addWidget(self.xaxis_min, 1, 4)
        self.xaxis_max = QLineEdit(self)
        axis_box_layout.addWidget(self.xaxis_max, 1, 5)

        # Y axis drop down menu
        self.yaxis_dropdown = QComboBox(self)
        axis_box_layout.addWidget(self.yaxis_dropdown, 2, 1)

        # Y axis titles
        self.yaxis_name = QLineEdit(self)
        axis_box_layout.addWidget(self.yaxis_name, 2, 2)
        self.yaxis_unit = QLineEdit(self)
        self.yaxis_unit.setToolTip('Enter "none" for no units')
        axis_box_layout.addWidget(self.yaxis_unit, 2, 3)

        # Y axis range
        self.yaxis_min = QLineEdit(self)
        axis_box_layout.addWidget(self.yaxis_min, 2, 4)
        self.yaxis_max = QLineEdit(self)
        axis_box_layout.addWidget(self.yaxis_max, 2, 5)

        # Condition Y axis drop down menu
        self.condition_yaxis_dropdown = QComboBox(self)
        axis_box_layout.addWidget(self.condition_yaxis_dropdown, 3, 1)

        # Condition Y axis titles
        self.condition_yaxis_name = QLineEdit(self)
        axis_box_layout.addWidget(self.condition_yaxis_name, 3, 2)
        self.condition_yaxis_unit = QLineEdit(self)
        self.xaxis_unit.setToolTip('Enter "none" for no units')
        axis_box_layout.addWidget(self.condition_yaxis_unit, 3, 3)

        # Condition Y axis range
        self.condition_yaxis_min = QLineEdit(self)
        axis_box_layout.addWidget(self.condition_yaxis_min, 3, 4)
        self.condition_yaxis_max = QLineEdit(self)
        axis_box_layout.addWidget(self.condition_yaxis_max, 3, 5)

        axis_box.setContentLayout(axis_box_layout)

        # --------------- DATA CONFIGURATION

        # Data configuration options
        data_box = CollapsibleBox('Data configuration:')
        options_layout.addWidget(data_box, 2, 0, 1, 6)
        data_box_layout = QGridLayout()

        # Smooth noisy data button
        data_box_layout.addWidget(Label('Smooth data:'), 0, 0)
        self.smooth_data = QCheckBox(self)
        self.smooth_data.setToolTip('Apply Savitzky-Golay to noisy data')
        data_box_layout.addWidget(self.smooth_data, 0, 1)

        # Align all data with 0 checkbox
        data_box_layout.addWidget(Label('Align at time = 0:'), 0, 2)
        self.align_data = QCheckBox(self)
        self.align_data.setToolTip('Start growth curves at 0 time')
        data_box_layout.addWidget(self.align_data, 0, 3)

        # Align all data at Y position
        data_box_layout.addWidget(Label('Align at Y ='), 0, 4)
        self.y_alignment = QLineEdit(self)
        self.y_alignment.setToolTip('Align all growth curves at given Y value')
        data_box_layout.addWidget(self.y_alignment, 0, 5)

        # Remove any obvious outliers from the growth data
        data_box_layout.addWidget(Label('Data outliers:'), 1, 0)
        data_box_layout.addWidget(Label('Auto remove:'), 1, 1)
        self.auto_remove = QCheckBox(self)
        data_box_layout.addWidget(self.auto_remove, 1, 2)
        data_box_layout.addWidget(Label('Remove above:'), 1, 3)
        self.remove_above = QLineEdit(self)
        data_box_layout.addWidget(self.remove_above, 1, 4)
        data_box_layout.addWidget(Label('Remove below:'), 1, 5)
        self.remove_below = QLineEdit(self)
        data_box_layout.addWidget(self.remove_below, 1, 6)

        # Condition data downsampling and averaging
        data_box_layout.addWidget(Label('Condition data:'), 2, 0)
        data_box_layout.addWidget(Label('Time average:'), 2, 1)
        self.condition_average = QLineEdit(self)
        self.condition_average.setToolTip('Average over time window')
        data_box_layout.addWidget(self.condition_average, 2, 2)

        data_box.setContentLayout(data_box_layout)

        # --------------- LEGEND CONFIGURATION

        # Legend configuration options
        legend_box = CollapsibleBox('Legend configuration:')
        options_layout.addWidget(legend_box, 3, 0, 1, 6)
        legend_box_layout = QGridLayout()

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
        self.extra_info.addItem("none")
        self.extra_info.addItem("reactor")
        self.extra_info.addItem("profile")
        self.extra_info.addItem("title")
        self.extra_info.addItem("date")
        self.extra_info.addItem("time")
        self.extra_info.addItem("date+time")
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
        self.condition_extra_info.addItem("none")
        self.condition_extra_info.addItem("reactor")
        self.condition_extra_info.addItem("profile")
        self.condition_extra_info.addItem("title")
        self.condition_extra_info.addItem("date")
        self.condition_extra_info.addItem("time")
        self.condition_extra_info.addItem("date+time")
        self.condition_extra_info.setToolTip('Show extra information from '
                                             'the file in the legend')
        legend_box_layout.addWidget(self.condition_extra_info, 2, 5)

        # Checkbox to only show extra info
        self.condition_only_extra = QCheckBox(self)
        legend_box_layout.addWidget(self.condition_only_extra, 2, 6)

        legend_box.setContentLayout(legend_box_layout)

        # --------------- STYLE CONFIGURATION

        # Style configuration
        style_box = CollapsibleBox('Style configuration:')
        options_layout.addWidget(style_box, 4, 0, 1, 6)
        style_box_layout = QGridLayout()

        # Plot style dropdown menu
        style_box_layout.addWidget(Label('Style:'), 0, 0)
        self.style_dropdown = QComboBox(self)
        self.style_dropdown.addItem("default")
        self.style_dropdown.addItem("greyscale")
        self.style_dropdown.addItem("colour blind")
        self.style_dropdown.addItem("pastel")
        self.style_dropdown.addItem("deep")
        style_box_layout.addWidget(self.style_dropdown, 0, 1)

        # Font style dropdown menu
        style_box_layout.addWidget(Label('Font style:'), 0, 2)
        self.font_dropdown = QComboBox(self)
        self.font_dropdown.addItem("sans-serif")
        self.font_dropdown.addItem("serif")
        self.font_dropdown.addItem("cursive")
        self.font_dropdown.addItem("fantasy")
        self.font_dropdown.addItem("monospace")
        style_box_layout.addWidget(self.font_dropdown, 0, 3)

        # Font size textbox
        style_box_layout.addWidget(Label('Title font size:'), 1, 0)
        self.title_size = QLineEdit(self)
        style_box_layout.addWidget(self.title_size, 1, 1)

        style_box_layout.addWidget(Label('Legend font size:'), 1, 2)
        self.legend_size = QLineEdit(self)
        style_box_layout.addWidget(self.legend_size, 1, 3)

        style_box_layout.addWidget(Label('Label font size:'), 1, 4)
        self.label_size = QLineEdit(self)
        style_box_layout.addWidget(self.label_size, 1, 5)

        # Line width textbox
        style_box_layout.addWidget(Label('Line width:'), 2, 0)
        self.line_width = QLineEdit(self)
        style_box_layout.addWidget(self.line_width, 2, 1)

        # Condition axis colour
        style_box_layout.addWidget(Label('Condition axis colour:'), 2, 2)
        self.axis_colour = QLineEdit(self)
        style_box_layout.addWidget(self.axis_colour, 2, 3)

        style_box_layout.addWidget(Label('Grid:'), 2, 4)
        self.grid_toggle = QCheckBox(self)
        style_box_layout.addWidget(self.grid_toggle, 2, 5)

        style_box.setContentLayout(style_box_layout)

        # --------------- STATS CONFIGURATION

        # Stats configuration
        stats_box = CollapsibleBox('Stats configuration:')
        options_layout.addWidget(stats_box, 5, 0, 1, 6)
        stats_box_layout = QGridLayout()

        stats_box_layout.addWidget(Label('Standard error:'), 0, 0)
        self.std_err = QCheckBox(self)
        self.std_err.setToolTip('Checked = show standard error on mean\n'
                                'Unchecked = show standard deviation')
        stats_box_layout.addWidget(self.std_err, 0, 1)

        stats_box.setContentLayout(stats_box_layout)

        # Add layouts to tabs via widgets
        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        tabs.addTab(plot_widget, 'Plotting')
        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        options_scroll.setWidget(options_widget)
        tabs.addTab(options_scroll, 'Options')

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
            self.plot.plot(self.data, self.condition_data, self.config)
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    # Function: Save the main plot
    def save_plot(self):
        try:
            self.plot.save(self.config)
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
        self.config.do_fit = False
        self.config.cursor = not self.config.cursor

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
        self.config.title = self.figure_title.text()

        # x axis config
        self.config.xvar = self.xaxis_dropdown.currentText()
        self.config.xname = self.xaxis_name.text()
        self.config.xunit = self.xaxis_unit.text()
        if(isfloat(self.xaxis_min.text())):
            self.config.xmin = float(self.xaxis_min.text())
        else:
            self.config.xmin = -1
        if(isfloat(self.xaxis_max.text())):
            self.config.xmax = float(self.xaxis_max.text())
        else:
            self.config.xmax = -1

        # y axis config
        self.config.yvar = self.yaxis_dropdown.currentText()
        self.config.yname = self.yaxis_name.text()
        self.config.yunit = self.yaxis_unit.text()
        if(isfloat(self.yaxis_min.text())):
            self.config.ymin = float(self.yaxis_min.text())
        else:
            self.config.ymin = -1
        if(isfloat(self.yaxis_max.text())):
            self.config.ymax = float(self.yaxis_max.text())
        else:
            self.config.ymax = -1

        # Condition y axis config
        self.config.condition_yvar = \
            self.condition_yaxis_dropdown.currentText()
        self.config.condition_yname = self.condition_yaxis_name.text()
        self.config.condition_yunit = self.condition_yaxis_unit.text()
        if(isfloat(self.condition_yaxis_min.text())):
            self.config.condition_ymin = \
                float(self.condition_yaxis_min.text())
        else:
            self.config.condition_ymin = -1
        if(isfloat(self.condition_yaxis_max.text())):
            self.config.condition_ymax = float(self.condition_yaxis_max.text())
        else:
            self.config.condition_ymax = -1

        # Data config
        self.config.smooth = self.smooth_data.isChecked()
        self.config.align = self.align_data.isChecked()
        if(isfloat(self.y_alignment.text())):
            self.config.y_alignment = float(self.y_alignment.text())
        else:
            self.config.y_alignment = -1
        self.config.auto_remove = self.auto_remove.isChecked()
        if(isfloat(self.remove_above.text())):
            self.config.remove_above = float(self.remove_above.text())
        else:
            self.config.remove_above = -1
        if(isfloat(self.remove_below.text())):
            self.config.remove_below = float(self.remove_below.text())
        else:
            self.config.remove_below = -1
        if(isfloat(self.condition_average.text())):
            self.config.condition_average = \
                float(self.condition_average.text())
        else:
            self.config.condition_average = -1

        # Legend config
        self.config.legend = self.legend_toggle.isChecked()
        self.config.condition_legend = \
            self.condition_legend_toggle.isChecked()
        self.config.legend_title = self.legend_title.text()
        if(self.config.legend_title.lower() == 'none'):
            self.config.legend_title = ''
        self.config.condition_legend_title = self.condition_legend_title.text()
        if(self.config.condition_legend_title.lower() == 'none'):
            self.config.condition_legend_title = ''
        self.config.label_names.clear()
        for i in range(self.legend_names.count()):
            self.config.label_names.append(self.legend_names.itemText(i))
        self.config.condition_label_names.clear()
        for i in range(self.condition_legend_names.count()):
            self.config.condition_label_names.append(
                self.condition_legend_names.itemText(i)
            )
        self.config.extra_info = self.extra_info.currentText()
        self.config.condition_extra_info = \
            self.condition_extra_info.currentText()
        self.config.only_extra = self.only_extra.isChecked()
        self.config.condition_only_extra = \
            self.condition_only_extra.isChecked()

        # Style config
        self.config.style = self.style_dropdown.currentText()
        self.config.font_style = self.font_dropdown.currentText()
        if(isfloat(self.title_size.text())):
            self.config.title_size = float(self.title_size.text())
        else:
            self.config.title_size = -1
        if(isfloat(self.legend_size.text())):
            self.config.legend_size = float(self.legend_size.text())
        else:
            self.config.legend_size = -1
        if(isfloat(self.label_size.text())):
            self.config.label_size = float(self.label_size.text())
        else:
            self.config.label_size = -1
        if(isfloat(self.line_width.text())):
            self.config.line_width = float(self.line_width.text())
        else:
            self.config.line_width = -1
        self.config.axis_colour = self.axis_colour.text()
        self.config.grid = self.grid_toggle.isChecked()

        # Stats config
        self.config.std_err = self.std_err.isChecked()

        self.config.do_fit = False
