# Standard library imports
import csv

# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget, QSizePolicy,
                             QGridLayout, QVBoxLayout, QScrollArea, QPushButton, QListWidget, QComboBox,
                             QCheckBox, QLabel, QLineEdit, QGraphicsDropShadowEffect, QSizePolicy,
                             QFormLayout, QHBoxLayout, QMenu, QAction, QSplitter)
from PyQt5.QtCore import QPoint, Qt

# Local application imports
from ada.plotter.main_plot import PlotCanvas
from ada.data.data_manager import data_manager
from ada.reader.read_calibration import read_calibration
from ada.components.label import Label, TopLabel, LeftLabel, DelLabel
from ada.components.user_input import TextEntry, SpinBox, DropDown, CheckBox, RadioButton
from ada.components.list import List
from ada.components.spacer import Spacer
from ada.components.button import Button, BigButton
from ada.components.data_list_item import (DataListItem, ConditionListItem,
                                           DelListItem)
from ada.gui.error_window import error_wrapper
from ada.gui.export_window import ExportWindow
from ada.gui.table_window import TableWindow
from ada.gui.fit_window import FitWindow
from ada.gui.load_window import LoadWindow
from ada.gui.correlation_window import CorrelationWindow
from ada.gui.file_handler import get_file_names, get_save_file_name
from ada.type_functions import isfloat, isint, set_float, set_int
import ada.configuration as config
import ada.styles as styles
from ada.logger import logger


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Algal Data Analyser'
        # Default dimensions
        self.left = 10 * config.wr
        self.top = 60 * config.wr
        self.width = 960 * config.wr
        self.height = 600 * config.wr
        logger.debug('Creating main window [left:%.2f, top:%.2f, width:%.2f, height:%.2f]' % (
            self.left, self.top, self.width, self.height))
        self.setStyleSheet(styles.main_background)
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        wr = config.wr
        hr = config.wr

        tabs = QTabWidget()
        tabs.setStyleSheet(styles.tab_style)

        # ---------------------------------------------------------------------
        #                           PLOTTING TAB
        # ---------------------------------------------------------------------

        # Main plotting window
        splitter = QSplitter()

        plot_layout = QGridLayout()
        plot_layout.setContentsMargins(5*wr, 5*hr, 5*wr, 5*hr)
        plot_layout.setSpacing(10*wr)

        # Main plot window (row, column, row extent, column extent)
        self.plot = PlotCanvas(self, width=10*wr, height=4*hr, dpi=100*wr)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=10*wr, xOffset=3*wr, yOffset=3*hr)
        self.plot.setGraphicsEffect(shadow)
        self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        plot_layout.addWidget(self.plot, 0, 0, 5, 6)

        # Saving options
        save_button = Button('Save Plot', self, 'Save the figure')
        save_button.clicked.connect(self.save_plot)
        plot_layout.addWidget(save_button, 5, 0)

        # Export options
        export_button = Button('Export Data', self,
                               'Export the data to CSV')
        export_button.clicked.connect(self.export_files)
        plot_layout.addWidget(export_button, 5, 1)

        # Measure gradient
        measure_button = Button('Measure', self, 'Measure the growth rate')
        measure_button.clicked.connect(self.toggle_cursor)
        plot_layout.addWidget(measure_button, 5, 2)

        # Fit curves
        fit_button = Button('Fit', self, 'Fit the growth curves')
        fit_button.clicked.connect(self.fit_curve)
        plot_layout.addWidget(fit_button, 5, 3)

        # Table output button
        table_button = Button('To Table', self,
                              'Create a table of growth rates for all curves'
                              '\nConfigure in options tab')
        table_button.clicked.connect(self.create_table)
        plot_layout.addWidget(table_button, 5, 4)

        # Correlations output button
        correlation_button = Button('Correlations', self,
                                    'Create additional plots showing correlations between growth and condition variables')
        correlation_button.clicked.connect(self.open_correlation)
        plot_layout.addWidget(correlation_button, 5, 5)

        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        splitter.addWidget(plot_widget)

        data_entry_layout = QVBoxLayout()
        data_entry_layout.setSpacing(10*wr)
        data_entry_layout.setContentsMargins(5*wr, 5*hr, 5*wr, 5*hr)
        # Add data button
        self.data_button = Button('Add Data', self,
                                  'Import data for plotting')
        self.data_button.clicked.connect(self.open_data_files)
        data_entry_layout.addWidget(self.data_button)
        self.data_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_button.customContextMenuRequested.connect(
            self.on_context_menu)

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
        self.calibration_file.button.clicked.connect(
            self.remove_calibration_file)
        self.calibration_file.setFixedHeight(40*hr)
        data_entry_layout.addWidget(self.calibration_file)

        # Plot button
        plot_button = BigButton('Plot!', self, 'Plot the data!')
        plot_button.clicked.connect(self.update_plot)
        data_entry_layout.addWidget(plot_button)

        data_entry_widget = QWidget()
        data_entry_widget.setLayout(data_entry_layout)
        splitter.addWidget(data_entry_widget)

        tabs.addTab(splitter, 'Plotting')

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
        self.xaxis_min = TextEntry('Range min:', self, config.xmin)
        x_form_layout.addRow(self.xaxis_min)
        self.xaxis_max = TextEntry('Range max:', self, config.xmax)
        x_form_layout.addRow(self.xaxis_max)

        # X axis log scale
        self.xaxis_log = CheckBox('Log scale', self)
        x_form_layout.addRow(' ', self.xaxis_log)

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
        self.yaxis_min = TextEntry('Range min:', self, config.ymin)
        y_form_layout.addRow(self.yaxis_min)
        self.yaxis_max = TextEntry('Range max:', self, config.ymax)
        y_form_layout.addRow(self.yaxis_max)

        # Y axis log scale
        self.yaxis_log = CheckBox('Log scale', self)
        self.yaxis_normlog = CheckBox('ln(Y/Y0)', self)
        ylog_hbox = QHBoxLayout()
        ylog_hbox.setSpacing(15*wr)
        ylog_hbox.setContentsMargins(0, 0, 1*wr, 1*hr)
        ylog_hbox.addWidget(self.yaxis_log)
        ylog_hbox.addWidget(self.yaxis_normlog)
        ylog_widget = QWidget()
        ylog_widget.setLayout(ylog_hbox)
        y_form_layout.addRow(' ', ylog_widget)

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
        self.condition_yaxis_min = TextEntry(
            'Range min:', self, config.condition_ymin)
        z_form_layout.addRow(self.condition_yaxis_min)
        self.condition_yaxis_max = TextEntry(
            'Range max:', self, config.condition_ymax)
        z_form_layout.addRow(self.condition_yaxis_max)

        # Condition Y axis log scale
        self.condition_yaxis_log = CheckBox('Log scale', self)
        z_form_layout.addRow(' ', self.condition_yaxis_log)

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
        axis_box_widget.setStyleSheet(styles.white_background)
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
        self.y_alignment = TextEntry('Align at Y:', self, config.y_alignment)
        self.y_alignment.setToolTip('Align all growth curves at given Y value')
        data_box_layout.addRow(self.y_alignment)

        # Align all data with 0 checkbox
        self.initial_y = TextEntry('Set initial Y:', self, config.initial_y)
        self.initial_y.setToolTip('Start growth curves at a given Y value')
        data_box_layout.addRow(self.initial_y)

        # Growth data averaging
        self.growth_average = TextEntry(
            'Growth data time average:', self, config.growth_average)
        self.growth_average.setToolTip('Average over a given time window')
        data_box_layout.addRow(self.growth_average)

        # Condition data averaging
        self.condition_average = TextEntry(
            'Condition data time average:', self, config.condition_average)
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
        self.remove_above = TextEntry(
            'Remove above:', self, config.remove_above)
        data_v_form_layout.addRow(self.remove_above)
        self.remove_below = TextEntry(
            'Remove below:', self, config.remove_below)
        data_v_form_layout.addRow(self.remove_below)
        self.remove_zeros = CheckBox('Remove points with y=0 off/on', self)
        data_v_form_layout.addRow(' ', self.remove_zeros)
        data_v_form_widget = QWidget()
        data_v_form_widget.setLayout(data_v_form_layout)
        data_v_layout.addWidget(data_v_form_widget)
        data_v_layout.addWidget(Spacer())

        data_v_widget = QWidget()
        data_v_widget.setLayout(data_v_layout)
        data_h_layout.addWidget(data_v_widget)
        data_h_layout.addWidget(Spacer())

        data_box_widget = QWidget()
        data_box_widget.setStyleSheet(styles.white_background)
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

        self.condition_extra_info = DropDown(
            'Extra text:', config.info_options, self)
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
        legend_box_widget.setStyleSheet(styles.white_background)
        legend_box_widget.setLayout(legend_h_layout)
        tabs.addTab(legend_box_widget, 'Legend')

        # --------------- STYLE CONFIGURATION

        # Style configuration
        style_h_layout = QHBoxLayout()
        style_box_layout = QFormLayout()
        style_numeric_layout = QFormLayout()

        # Plot style dropdown menu
        self.style_dropdown = DropDown('Style:', config.style_options, self)
        style_box_layout.addRow(self.style_dropdown)

        # Font style dropdown menu
        self.font_dropdown = DropDown('Font style:', config.font_options, self)
        style_box_layout.addRow(self.font_dropdown)

        # Font size textbox
        self.title_size = SpinBox(
            'Title font size:', config.title_size, 0, 100, self)
        style_numeric_layout.addRow(self.title_size)

        self.legend_size = SpinBox(
            'Legend font size:', config.legend_size, 0, 100, self)
        style_numeric_layout.addRow(self.legend_size)

        self.label_size = SpinBox(
            'Label font size:', config.label_size, 0, 100, self)
        style_numeric_layout.addRow(self.label_size)

        # Line width textbox
        self.line_width = SpinBox(
            'Line width:', config.line_width, 0, 20, self)
        style_numeric_layout.addRow(self.line_width)

        self.marker_size = SpinBox(
            'Marker size:', config.marker_size, 0, 20, self)
        style_numeric_layout.addRow(self.marker_size)

        self.capsize = SpinBox(
            'Error cap size:', config.capsize, 0, 20, self)
        style_numeric_layout.addRow(self.capsize)

        self.save_dpi = SpinBox(
            'Saved figure DPI:', config.save_dpi, 10, 2000, self)
        style_numeric_layout.addRow(self.save_dpi)

        # Condition axis colour
        self.axis_colour = TextEntry('Condition axis color:', self)
        style_box_layout.addRow(self.axis_colour)

        self.grid_toggle = CheckBox('Grid on/off', self)
        style_box_layout.addRow(' ', self.grid_toggle)

        style_box_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        style_box_layout.setLabelAlignment(Qt.AlignCenter)

        style_box_widget = QWidget()
        style_box_widget.setLayout(style_box_layout)

        style_numeric_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        style_numeric_layout.setLabelAlignment(Qt.AlignCenter)

        style_numeric_widget = QWidget()
        style_numeric_widget.setLayout(style_numeric_layout)

        style_h_layout.addWidget(style_box_widget)
        style_h_layout.addWidget(style_numeric_widget)
        style_h_widget = QWidget()
        style_h_widget.setLayout(style_h_layout)
        style_h_widget.setStyleSheet(styles.white_background)
        tabs.addTab(style_h_widget, 'Style')

        # --------------- STATS CONFIGURATION

        # Stats configuration
        stats_box_layout = QFormLayout()

        self.std_err = RadioButton('Standard deviation', 'Standard error', self)
        self.std_err.setToolTip('Show standard deviation or the standard error on the mean in plots and measurements')
        stats_box_layout.addRow(' ', self.std_err)

        self.sig_figs = SpinBox(
            'Significant figures:', config.sig_figs, 0, 20, self)
        stats_box_layout.addRow(self.sig_figs)

        self.show_fit_text = CheckBox('Show fit model text', self)
        self.show_fit_text.setToolTip('Checked = display equation for fitted model\n'
                                      "Unchecked = don't display equation")
        stats_box_layout.addRow(' ', self.show_fit_text)

        self.show_fit_result = CheckBox('Show fit parameters', self)
        self.show_fit_result.setToolTip('Checked = show fitted values of model parameters\n'
                                        'Unchecked = don''t show fit parameters')
        stats_box_layout.addRow(' ', self.show_fit_result)

        self.show_fit_errors = CheckBox('Show fit errors', self)
        self.show_fit_errors.setToolTip('Checked = show uncertainties on fit parameters\n'
                                        'Unchecked = don''t show uncertainties')
        stats_box_layout.addRow(' ', self.show_fit_errors)

        stats_box_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        stats_box_layout.setLabelAlignment(Qt.AlignCenter)

        stats_box_widget = QWidget()
        stats_box_widget.setStyleSheet(styles.white_background)
        stats_box_widget.setLayout(stats_box_layout)
        tabs.addTab(stats_box_widget, 'Stats')

        # --------------- ADVANCED CONFIGURATION

        # Advanced configuration
        advanced_h_layout = QHBoxLayout()
        advanced_left_layout = QFormLayout()
        advanced_right_layout = QFormLayout()

        advanced_left_layout.addWidget(TopLabel('Savitsky-Golay smoothing:'))
        self.sg_window_size = TextEntry(
            'Window size', self, config.sg_window_size)
        advanced_left_layout.addWidget(self.sg_window_size)
        self.sg_order = TextEntry('Order of polynomial', self, config.sg_order)
        advanced_left_layout.addWidget(self.sg_order)
        self.sg_deriv = TextEntry('Order of derivative', self, config.sg_deriv)
        advanced_left_layout.addWidget(self.sg_deriv)
        self.sg_rate = TextEntry('Sample spacing', self, config.sg_rate)
        advanced_left_layout.addWidget(self.sg_rate)

        self.outlier_threshold = TextEntry(
            'Auto outlier threshold', self, config.outlier_threshold)
        advanced_right_layout.addWidget(self.outlier_threshold)

        advanced_left_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        advanced_left_layout.setLabelAlignment(Qt.AlignCenter)
        advanced_right_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        advanced_right_layout.setLabelAlignment(Qt.AlignCenter)

        advanced_left_widget = QWidget()
        advanced_left_widget.setStyleSheet(styles.white_background)
        advanced_left_widget.setLayout(advanced_left_layout)
        advanced_h_layout.addWidget(advanced_left_widget)
        advanced_right_widget = QWidget()
        advanced_right_widget.setStyleSheet(styles.white_background)
        advanced_right_widget.setLayout(advanced_right_layout)
        advanced_h_layout.addWidget(advanced_right_widget)
        advanced_widget = QWidget()
        advanced_widget.setStyleSheet(styles.white_background)
        advanced_widget.setLayout(advanced_h_layout)
        tabs.addTab(advanced_widget, 'Advanced')

        # ----------------------------------
        self.setCentralWidget(tabs)
        self.show()

    # -------------------------------------------------------------------------
    #                           MEMBER FUNCTIONS
    # -------------------------------------------------------------------------

    # Open the load window to read in data files
    @error_wrapper
    def open_data_files(self):
        self.update_config()
        logger.debug('Opening data files')
        self.load = LoadWindow(self)
        self.load.show()

    # Open the file explorer and read in calibration file
    @error_wrapper
    def open_calibration_file(self):
        logger.debug('Loading calibration curve from file')
        self.calibration_file.clear()
        calib_file_name = get_file_names()
        self.calibration_file.setText(calib_file_name[0])
        data_manager.calibration = read_calibration(calib_file_name[0])
        self.update_data_list()

    # Remove the calibration file
    @error_wrapper
    def remove_calibration_file(self):
        logger.debug('Removing calibration curve')
        self.calibration_file.clear()
        data_manager.calibration = None

    # Define right click behaviour
    @error_wrapper
    def on_context_menu(self, point):
        # show context menu
        action = self.clear_menu.exec_(self.data_button.mapToGlobal(point))
        if action == self.clear_action:
            logger.debug('Clearing all data')
            data_manager.clear()
            self.remove_calibration_file()
            self.update_data_list()
            self.update_condition_data_list()

    # Update the main plot
    @error_wrapper
    def update_plot(self):
        self.update_config()
        logger.debug('Updating the main plot')
        self.plot.plot()

    # Save the main plot
    @error_wrapper
    def save_plot(self):
        logger.info('Saving the plot')
        self.plot.save()

    # Update the list of data files and associated options
    def update_data_list(self):
        logger.debug('Updating the list of data files')
        self.data_list.clear()
        self.yaxis_dropdown.clear()
        self.legend_names.clear()
        for i, data in enumerate(data_manager.get_growth_data_files()):
            data_list_item = DataListItem(data.label, i, self)
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
                    contains_od = True
                if sig.name == 'CD':
                    contains_cd = True
            if contains_od and not contains_cd and data_manager.calibration is not None:
                self.yaxis_dropdown.addItem('CD')

    # Function: Update the list of condition data and associated options
    def update_condition_data_list(self):
        logger.debug('Updating the list of condition data files')
        self.condition_data_list.clear()
        self.condition_yaxis_dropdown.clear()
        self.condition_legend_names.clear()
        for i, data in enumerate(data_manager.get_condition_data_files()):
            data_list_item = ConditionListItem(data.label, i, self)
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
        logger.debug('Removing data list item %i' % row)
        for i, _ in enumerate(data_manager.get_growth_data_files()):
            if i != row:
                continue
            data_manager.growth_data.delete_data(i)
        self.update_data_list()

    # Function: Remove file from list of data
    def remove_replicate(self, index):
        row = self.get_data_row()
        logger.debug('Removing replicate %i from data list item %i' %
                     (index, row))
        for i, _ in enumerate(data_manager.get_growth_data_files()):
            if i != row:
                continue
            data_manager.growth_data.delete_replicate(i, index)
        self.update_data_list()

    # Function: Remove file from list of data
    def remove_condition_replicate(self, index):
        row = self.get_condition_row()
        logger.debug('Removing replicate %i from condition list item %i' %
                     (index, row))
        for i, _ in enumerate(data_manager.get_condition_data_files()):
            if i != row:
                continue
            data_manager.condition_data.delete_replicate(i, index)
        self.update_condition_data_list()

    # Function: Remove file from list of condition data
    def remove_condition_item(self):
        row = self.get_condition_row()
        logger.debug('Removing condition data list item %i' % row)
        for i, _ in enumerate(data_manager.get_condition_data_files()):
            if i != row:
                continue
            data_manager.condition_data.delete_data(i)
        self.update_condition_data_list()

    def add_to_item(self):
        row = self.get_data_row()
        logger.debug('Adding replicate to data list item %i' % row)
        # Open file with file handler
        self.load = LoadWindow(self, row)
        self.load.show()

    @error_wrapper
    def download_template(self):
        logger.debug('Downloading ADA data template')
        template = ['Name,,Title,,Reactor,,Profile,\n',
                    'Date,2020-01-15,Time,18:18:18\n',
                    'Time [hr],OD [],Conditions\n']
        file_name = get_save_file_name()
        file_name = file_name.split('.')[0] + '.csv'
        with open(file_name, 'w', newline='') as csvfile:
            for row in template:
                csvfile.write(row)

    # Function: Toggle cursor on and off
    @error_wrapper
    def toggle_cursor(self):
        config.do_fit = False
        config.cursor = not config.cursor
        self.update_plot()

    # Open window for fitting data
    @error_wrapper
    def fit_curve(self):
        if not config.do_fit:
            logger.debug('Opening fit window')
            self.fit = FitWindow(self)
            self.fit.show()
        else:
            config.do_fit = False
            self.update_plot()

    # Open window for creating a data table
    @error_wrapper
    def create_table(self):
        self.update_config()
        logger.debug('Opening table window')
        self.table = TableWindow(self)
        self.table.show()

    # Function: Open window for exporting data to csv format
    @error_wrapper
    def export_files(self):
        logger.debug('Opening export window')
        self.export = ExportWindow(self)
        self.export.show()

    # Open window for evaluating correlations
    @error_wrapper
    def open_correlation(self):
        self.update_config()
        logger.debug('Opening correlation window')
        self.correlation = CorrelationWindow(self)
        self.correlation.show()

    # Function: Update the global configuration
    def update_config(self):
        logger.debug('Updating configuration')
        config.title = self.figure_title.text()

        # x axis config
        config.xvar = self.xaxis_dropdown.currentText()
        config.xname = self.xaxis_name.text()
        config.xunit = self.xaxis_unit.text()
        config.xmin = self.xaxis_min.get_float()
        config.xmax = self.xaxis_max.get_float()
        config.xlog = self.xaxis_log.isChecked()

        # y axis config
        config.yvar = self.yaxis_dropdown.currentText()
        config.yname = self.yaxis_name.text()
        config.yunit = self.yaxis_unit.text()
        config.ymin = self.yaxis_min.get_float()
        config.ymax = self.yaxis_max.get_float()
        config.ylog = self.yaxis_log.isChecked()
        config.ynormlog = self.yaxis_normlog.isChecked()

        # Condition y axis config
        config.condition_yvar = \
            self.condition_yaxis_dropdown.currentText()
        config.condition_yname = self.condition_yaxis_name.text()
        config.condition_yunit = self.condition_yaxis_unit.text()
        config.condition_ymin = self.condition_yaxis_min.get_float()
        config.condition_ymax = self.condition_yaxis_max.get_float()
        config.condition_ylog = self.condition_yaxis_log.isChecked()

        # Data config
        config.smooth = self.smooth_data.isChecked()
        config.align = self.align_data.isChecked()
        config.y_alignment = self.y_alignment.get_float()
        config.initial_y = self.initial_y.get_float()
        config.auto_remove = self.auto_remove.isChecked()
        config.remove_zeros = self.remove_zeros.isChecked()
        config.remove_above = self.remove_above.get_float()
        config.remove_below = self.remove_below.get_float()
        config.growth_average = self.growth_average.get_float()
        config.condition_average = self.condition_average.get_float()
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
        config.label_names = self.legend_names.get_list()
        config.condition_label_names = self.condition_legend_names.get_list()
        config.extra_info = self.extra_info.currentText()
        config.condition_extra_info = \
            self.condition_extra_info.currentText()
        config.only_extra = self.only_extra.isChecked()
        config.condition_only_extra = \
            self.condition_only_extra.isChecked()

        # Style config
        config.style = self.style_dropdown.currentText()
        config.font_style = self.font_dropdown.currentText()
        config.title_size = self.title_size.get_float()
        config.legend_size = self.legend_size.get_float()
        config.label_size = self.label_size.get_float()
        config.line_width = self.line_width.get_float()
        config.axis_colour = self.axis_colour.text()
        config.marker_size = self.marker_size.get_float()
        config.capsize = self.capsize.get_float()
        config.save_dpi = self.save_dpi.get_float()
        config.grid = self.grid_toggle.isChecked()

        # Stats config
        config.std_err = self.std_err.isChecked()
        config.show_fit_text = self.show_fit_text.isChecked()
        config.show_fit_result = self.show_fit_result.isChecked()
        config.show_fit_errors = self.show_fit_errors.isChecked()
        config.sig_figs = self.sig_figs.get_int()

        # Advanced config
        config.sg_window_size = self.sg_window_size.get_float()
        config.sg_order = self.sg_order.get_float()
        config.sg_deriv = self.sg_deriv.get_float()
        config.sg_rate = self.sg_rate.get_float()
        config.outlier_threshold = self.outlier_threshold.get_float()
