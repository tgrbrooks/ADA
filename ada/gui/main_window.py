# Related third party imports
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QSizePolicy, QToolBar,
                             QGridLayout, QVBoxLayout, QGraphicsDropShadowEffect, QSizePolicy,
                             QHBoxLayout, QMenu, QAction, QSplitter)
from PyQt5.QtCore import QPoint, Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon

# Local application imports
from ada.plotter.main_plot import PlotCanvas
from ada.data.data_manager import data_manager
from ada.reader.read_calibration import read_calibration
from ada.components.label import TopLabel, DelLabel
from ada.components.user_input import TextEntry, SpinBox, DropDown, CheckBox, RadioButton
from ada.components.list import List
from ada.components.spacer import Spacer
from ada.components.button import Button, BigButton
from ada.components.data_list_item import DataListItem, ConditionListItem
from ada.components.layout_widget import LayoutWidget
from ada.components.form import Form
from ada.gui.error_window import error_wrapper
from ada.gui.export_window import ExportWindow
from ada.gui.table_window import TableWindow
from ada.gui.fit_window import FitWindow
from ada.gui.load_window import LoadWindow
from ada.gui.correlation_window import CorrelationWindow
from ada.gui.test_window import TestWindow
from ada.gui.file_handler import get_file_names, get_save_file_name
from ada.configuration import config
import ada.options as opt
import ada.styles as styles
import ada.gui.qrc_resources
from ada.logger import logger


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Algal Data Analyser'
        # Default dimensions
        self.left = 10 * config['width_ratio']
        self.top = 60 * config['width_ratio']
        self.width = 960 * config['width_ratio']
        self.height = 600 * config['width_ratio']
        logger.debug('Creating main window [left:%.2f, top:%.2f, width:%.2f, height:%.2f]' % (
            self.left, self.top, self.width, self.height))
        self.setStyleSheet(styles.main_background)
        self._createMenuBar()
        self.initUI()

    def _createMenuBar(self):
        logger.info('Creating menu')
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu("&File")
        self.save_action = QAction('Save plot', self)
        self.save_action.triggered.connect(self.save_plot)
        file_menu.addAction(self.save_action)
        self.export_action = QAction('Export data', self)
        self.export_action.triggered.connect(self.export_files)
        file_menu.addAction(self.export_action)

        help_menu = menu_bar.addMenu("&Help")
        self.docs_action = QAction('Documentation', self)
        self.docs_action.triggered.connect(self.open_docs)
        help_menu.addAction(self.docs_action)
        self.video_action = QAction('Tutorials', self)
        self.video_action.triggered.connect(self.open_video)
        help_menu.addAction(self.video_action)
        self.issues_action = QAction('Issues', self)
        self.issues_action.triggered.connect(self.open_issues)
        help_menu.addAction(self.issues_action)

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        wr = config['width_ratio']
        hr = config['width_ratio']

        tabs = QTabWidget()
        tabs.setStyleSheet(styles.tab_style)

        # ---------------------------------------------------------------------
        #                           PLOTTING TAB
        # ---------------------------------------------------------------------

        # Main plotting window
        splitter = QSplitter()

        plot_view = LayoutWidget(QGridLayout, margin=5, spacing=10)

        # Main plot window (row, column, row extent, column extent)
        self.plot = plot_view.addWidget(PlotCanvas(self, width=10*wr, height=4*hr, dpi=100*wr), 0, 1, 5, 5)
        shadow = QGraphicsDropShadowEffect(
            blurRadius=10*wr, xOffset=3*wr, yOffset=3*hr)
        self.plot.setGraphicsEffect(shadow)
        self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        toolbar = plot_view.addWidget(QToolBar("Tools", self), 0, 0, 5, 1)
        toolbar.setOrientation(Qt.Vertical)
        toolbar.setStyleSheet(styles.toolbar_style)

        toolbar_icons = [":measure.svg", ":fit.svg", ":table.svg", ":correlations.svg", ":template.svg", ":normal.svg"]
        toolbar_labels = ['&Measure', '&Fit', '&To Table', '&Correlations', '&Download Template', '&Statisitical Tests']
        toolbar_actions = [self.toggle_cursor, self.fit_curve, self.create_table, self.open_correlation, self.download_template, self.open_tests]
        for i, icon in enumerate(toolbar_icons):
            toolbar_action = QAction(QIcon(icon), toolbar_labels[i], self)
            toolbar_action.triggered.connect(toolbar_actions[i])
            toolbar.addAction(toolbar_action)

        splitter.addWidget(plot_view.widget)

        data_entry = LayoutWidget(QVBoxLayout, margin=5, spacing=10)
        self.data_button, self.data_list, _, self.condition_data_list, _, self.calibration_file, _ = data_entry.addWidgets([
            Button('Add Data', tooltip='Import data for plotting', clicked=self.open_data_files),
            List(scroll=True),
            TopLabel('Condition Data:'),
            List(scroll=True),
            Button('Add Calibration Curve', tooltip='Set OD to CD conversion from file', clicked=self.open_calibration_file),
            DelLabel('', clicked=self.remove_calibration_file),
            BigButton('Plot!', tooltip='Plot the data!', clicked=self.update_plot)])

        self.data_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_button.customContextMenuRequested.connect(
            self.on_context_menu)

        self.clear_menu = QMenu(self)
        self.clear_action = QAction('Clear all', self)
        self.clear_menu.addAction(self.clear_action)

        self.calibration_file.setFixedHeight(40*hr)

        splitter.addWidget(data_entry.widget)

        tabs.addTab(splitter, 'Plotting')

        # ---------------------------------------------------------------------
        #                           OPTIONS TABS
        # ---------------------------------------------------------------------

        # --------------- AXIS CONFIGURATION

        # Axis configuration
        axis_options = LayoutWidget(QVBoxLayout, style=styles.white_background)
        axis_h = LayoutWidget(QHBoxLayout)

        self.figure_title = axis_options.addWidget(
            TextEntry('Figure title:'))

        x_options = LayoutWidget(QVBoxLayout)
        x_options.addWidget(TopLabel('X (time):'))

        # X axis config
        x_form = Form()
        self.xaxis_dropdown, self.xaxis_name, self.xaxis_unit, self.xaxis_min, self.xaxis_max, self.xaxis_log = x_form.addRows([
            DropDown('Variable:', opt.xaxis_units, index=2),
            TextEntry('Label:'),
            TextEntry('Unit name:', tooltip='Enter "none" for no units'),
            TextEntry('Range min:', default=config['plot']['x_axis']['min']),
            TextEntry('Range max:', default=config['plot']['x_axis']['max']),
            CheckBox('Log scale')],
            padding=[False, False, False, False, False, True])

        x_options.addWidget(x_form.widget)
        axis_h.addWidget(x_options.widget)

        y_options = LayoutWidget(QVBoxLayout)
        y_options.addWidget(TopLabel('Y (growth):'))
        # Y axis config
        y_form = Form()
        self.yaxis_dropdown, self.yaxis_name, self.yaxis_unit, self.yaxis_min, self.yaxis_max = y_form.addRows([
            DropDown('Variable:', []),
            TextEntry('Label:'),
            TextEntry('Unit name:', tooltip='Enter "none" for no units'),
            TextEntry('Range min:', default=config['plot']['y_axis']['min']),
            TextEntry('Range max:', default=config['plot']['y_axis']['max'])])

        # Y axis log scale
        ylog_hbox = LayoutWidget(QHBoxLayout)
        ylog_hbox.layout.setSpacing(15*wr)
        ylog_hbox.layout.setContentsMargins(0, 0, 1*wr, 1*hr)
        self.yaxis_log, self.yaxis_normlog = ylog_hbox.addWidgets([
            CheckBox('Log scale'),
            CheckBox('ln(Y/Y0)')])
        y_form.addRow(ylog_hbox.widget, pad=True)

        y_options.addWidget(y_form.widget)
        axis_h.addWidget(Spacer())
        axis_h.addWidget(y_options.widget)

        z_options = LayoutWidget(QVBoxLayout)
        z_options.addWidget(TopLabel('Y2 (conditions):'))
        # Condition Y axis drop down menu
        z_form = Form()
        self.condition_yaxis_dropdown, self.condition_yaxis_name, self.condition_yaxis_unit, self.condition_yaxis_min, self.condition_yaxis_max, self.condition_yaxis_log = z_form.addRows([
            DropDown('Variable:', []),
            TextEntry('Label:'),
            TextEntry('Unit name:', tooltip='Enter "none" for no units'),
            TextEntry('Range min:', default=config['plot']['condition_axis']['min']),
            TextEntry('Range max:', default=config['plot']['condition_axis']['max']),
            CheckBox('Log scale')],
            padding=[False, False, False, False, False, True])

        z_options.addWidget(z_form.widget)
        axis_h.addWidget(Spacer())
        axis_h.addWidget(z_options.widget)
        axis_options.addWidget(axis_h.widget)
        axis_options.addWidget(Spacer())

        tabs.addTab(axis_options.widget, 'Axes')

        # --------------- DATA CONFIGURATION

        # Data configuration options
        data_options = LayoutWidget(QHBoxLayout, style=styles.white_background)
        data_form = Form()

        self.smooth_data, self.align_data, self.y_alignment, self.initial_y, self.growth_average, self.condition_average, self.show_events = data_form.addRows([
            CheckBox('Data smoothing off/on', tooltip='Apply Savitzky-Golay to noisy data'),
            CheckBox('Alignment at time = 0 on/off', tooltip='Start growth curves at 0 time'),
            TextEntry('Align at Y:', default=config['data']['y_alignment'], tooltip='Align all growth curves at given Y value'),
            TextEntry('Set initial Y:', default=config['data']['initial_y'], tooltip='Start growth curves at a given Y value'),
            TextEntry('Growth data time average:', default=config['data']['growth_average'], tooltip='Average over a given time window'),
            TextEntry('Condition data time average:', default=config['data']['condition_average'], tooltip='Average over a given time window'),
            CheckBox('Show events off/on')],
            padding=[True, True, False, False, False, False, True])

        data_options.addWidget(data_form.widget)

        # Remove any obvious outliers from the growth data
        outlier_options = LayoutWidget(QVBoxLayout)
        outlier_options.addWidget(TopLabel('Data outliers:'))
        outlier_form = Form()
        self.auto_remove, self.remove_above, self.remove_below = outlier_form.addRows([
            CheckBox('Auto-remove outliers off/on'),
            TextEntry('Remove above:', default=config['data']['remove_above']),
            TextEntry('Remove below:', default=config['data']['remove_below'])],
            padding=[True, False, False])
        outlier_options.addWidget(outlier_form.widget)
        outlier_options.addWidget(Spacer())

        data_options.addWidget(outlier_options)
        data_options.addWidget(Spacer())

        tabs.addTab(data_options.widget, 'Data')

        # --------------- LEGEND CONFIGURATION

        # Legend configuration options
        legend_options = LayoutWidget(QHBoxLayout, style=styles.white_background)

        # Legend on/off checkbox
        growth_options = LayoutWidget(QVBoxLayout)
        growth_options.addWidget(TopLabel('Growth Legend:'))
        growth_form = Form()
        self.legend_toggle, self.legend_names, self.legend_title, self.extra_info, self.only_extra = growth_form.addRows([
            CheckBox('Legend on'),
            DropDown('Labels:', [], tooltip='Edit names by changing text and pressing return', edit=True),
            TextEntry('Heading:', tooltip='Show extra information from the file in the legend'),
            DropDown('Extra text:', opt.info_options),
            CheckBox('Remove labels')],
            padding=[True, False, False, False, True])

        growth_options.addWidget(growth_form.widget)
        growth_options.addWidget(Spacer())
        legend_options.addWidget(growth_options.widget)

        # Condition legend configuration
        condition_options = LayoutWidget(QVBoxLayout)
        condition_options.addWidget(TopLabel('Condition legend:'))
        condition_form = Form()
        self.condition_legend_toggle, self.condition_legend_names, self.condition_legend_title, self.condition_extra_info, self.condition_only_extra = condition_form.addRows([
            CheckBox('Legend on'),
            DropDown('Labels:', [], tooltip='Edit names by changing text and pressing return', edit=True),
            TextEntry('Heading:'),
            DropDown('Extra text:', opt.info_options, tooltip='Show extra information from the file in the legend'),
            CheckBox('Remove labels')],
        padding=[True, False, False, False, True])

        condition_options.addWidget(condition_form.widget)
        condition_options.addWidget(Spacer())
        legend_options.addWidget(condition_options.widget)
        legend_options.addWidget(Spacer())

        tabs.addTab(legend_options.widget, 'Legend')

        # --------------- STYLE CONFIGURATION

        # Style configuration
        style_options = LayoutWidget(QHBoxLayout, style=styles.white_background)

        # Plot style dropdown menu
        style_form = Form(align=True)
        self.style_dropdown, self.font_dropdown, self.axis_colour, self.grid_toggle = style_form.addRows([
            DropDown('Style:', opt.style_options),
            DropDown('Font style:', opt.font_options),
            TextEntry('Condition axis color:'),
            CheckBox('Grid on/off')],
            padding=[False, False, False, True])

        style_options.addWidget(style_form.widget)

        # Sized
        style_numeric_form = Form(align=True)
        self.title_size, self.legend_size, self.label_size, self.line_width, self.marker_size, self.capsize, self.save_dpi = style_numeric_form.addRows([
            SpinBox('Title font size:', start=config['style']['title_size'], min_val=0, max_val=100),
            SpinBox('Legend font size:', start=config['style']['legend_size'], min_val=0, max_val=100),
            SpinBox('Label font size:', start=config['style']['label_size'], min_val=0, max_val=100),
            SpinBox('Line width:', start=config['style']['line_width'], min_val=0, max_val=20),
            SpinBox('Marker size:', start=config['style']['marker_size'], min_val=0, max_val=20),
            SpinBox('Error cap size:', start=config['style']['capsize'], min_val=0, max_val=20),
            SpinBox('Saved figure DPI:', start=config['style']['save_dpi'], min_val=10, max_val=2000)])

        style_options.addWidget(style_numeric_form.widget)

        tabs.addTab(style_options.widget, 'Style')

        # --------------- STATS CONFIGURATION

        # Stats configuration
        stats_form = Form(align=True, style=styles.white_background)
        self.std_err, self.sig_figs, self.show_fit_text, self.show_fit_result, self.show_fit_errors = stats_form.addRows([
            RadioButton('Standard deviation', 'Standard error', tooltip='Show standard deviation or the standard error on the mean in plots and measurements'),
            SpinBox('Significant figures:', start=config['stats']['sig_figs'], min_val=0, max_val=20),
            CheckBox('Show fit model text', tooltip='Checked = display equation for fitted model\n'
                                                                 'Unchecked = don''t display equation'),
            CheckBox('Show fit parameters', tooltip='Checked = show fitted values of model parameters\n'
                                                                 'Unchecked = don''t show fit parameters'),
            CheckBox('Show fit errors', tooltip='Checked = show uncertainties on fit parameters\n'
                                                             'Unchecked = don''t show uncertainties')],
            padding=[True, False, True, True, True])

        tabs.addTab(stats_form.widget, 'Stats')

        # --------------- ADVANCED CONFIGURATION

        # Advanced configuration
        advanced_options = LayoutWidget(QHBoxLayout, style=styles.white_background)

        sg_form = Form(align=True, style=styles.white_background)
        _, self.sg_window_size, self.sg_order, self.sg_deriv, self.sg_rate = sg_form.addRows([
            TopLabel('Savitsky-Golay smoothing:'),
            TextEntry('Window size', default=config['advanced']['savitsky_golay']['window_size']),
            TextEntry('Order of polynomial', default=config['advanced']['savitsky_golay']['sg_order']),
            TextEntry('Order of derivative', default=config['advanced']['savitsky_golay']['sg_deriv']),
            TextEntry('Sample spacing', default=config['advanced']['savitsky_golay']['sg_rate'])
        ])

        adv_outlier_form = Form(align=True, style=styles.white_background)
        self.outlier_threshold = adv_outlier_form.addRow(
            TextEntry('Auto outlier threshold', default=config['advanced']['outlier_threshold']))

        advanced_options.addWidget(sg_form.widget)
        advanced_options.addWidget(adv_outlier_form.widget)
        tabs.addTab(advanced_options.widget, 'Advanced')

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

    def open_docs(self):
        url = QUrl("https://algaeplotter.readthedocs.io/en/latest/")
        QDesktopServices.openUrl(url)

    def open_video(self):
        url = QUrl("https://www.youtube.com/channel/UCN5YtDhGqRBfPnk--78lsAQ")
        QDesktopServices.openUrl(url)

    def open_issues(self):
        url = QUrl("https://github.com/tgrbrooks/ADA/issues/new/choose")
        QDesktopServices.openUrl(url)

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
            if data.legend:
                self.legend_names.addItem(data.legend)
            else:
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
            if data.legend:
                self.condition_legend_names.addItem(data.legend)
            else:
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

    # Function: Remove file from list of data
    def set_visibility(self):
        row = self.get_data_row()
        for i, _ in enumerate(data_manager.get_growth_data_files()):
            if i != row:
                continue
            data_manager.get_growth_file(i).visible = not data_manager.get_growth_file(i).visible

    # Function: Remove file from list of data
    def set_condition_visibility(self):
        row = self.get_condition_row()
        for i, _ in enumerate(data_manager.get_condition_data_files()):
            if i != row:
                continue
            data_manager.get_condition_file(i).visible = not data_manager.get_condition_file(i).visible

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
        config['fit']['do_fit'] = False
        config['plot']['cursor'] = not config['plot']['cursor']
        self.update_plot()

    # Open window for fitting data
    @error_wrapper
    def fit_curve(self):
        if not config['fit']['do_fit']:
            logger.debug('Opening fit window')
            self.fit = FitWindow(self)
            self.fit.show()
        else:
            config['fit']['do_fit'] = False
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

    # Open window for performing statistical tests
    @error_wrapper
    def open_tests(self):
        self.update_config()
        logger.debug('Opening test window')
        self.tests = TestWindow(self)
        self.tests.show()

    # Function: Update the global configuration
    def update_config(self):
        logger.debug('Updating configuration')
        config['plot']['title'] = self.figure_title.text()

        # x axis config
        config['plot']['x_axis'] = {
            'variable': self.xaxis_dropdown.currentText(),
            'name': self.xaxis_name.text(),
            'unit': self.xaxis_unit.text(),
            'min': self.xaxis_min.get_float(),
            'max': self.xaxis_max.get_float(),
            'log': self.xaxis_log.isChecked()
        }

        # y axis config
        config['plot']['y_axis'] = {
            'variable': self.yaxis_dropdown.currentText(),
            'name': self.yaxis_name.text(),
            'unit': self.yaxis_unit.text(),
            'min': self.yaxis_min.get_float(),
            'max': self.yaxis_max.get_float(),
            'log': self.yaxis_log.isChecked(),
            'normlog': self.yaxis_normlog.isChecked()
        }

        # Condition y axis config
        config['plot']['condition_axis'] = {
            'var': self.condition_yaxis_dropdown.currentText(),
            'name': self.condition_yaxis_name.text(),
            'unit': self.condition_yaxis_unit.text(),
            'min': self.condition_yaxis_min.get_float(),
            'max': self.condition_yaxis_max.get_float(),
            'log': self.condition_yaxis_log.isChecked()
        }

        # Data config
        config['data'] = {
            'smooth': self.smooth_data.isChecked(),
            'align': self.align_data.isChecked(),
            'y_alignment': self.y_alignment.get_float(),
            'initial_y': self.initial_y.get_float(),
            'auto_remove': self.auto_remove.isChecked(),
            'remove_above': self.remove_above.get_float(),
            'remove_below': self.remove_below.get_float(),
            'growth_average': self.growth_average.get_float(),
            'condition_average': self.condition_average.get_float(),
            'show_events': self.show_events.isChecked()
        }

        # Legend config
        config['legend'] = {
            'show': self.legend_toggle.isChecked(),
            'title': self.legend_title.text(),
            'label_names': self.legend_names.get_list(),
            'extra_info': self.extra_info.currentText(),
            'only_extra': self.only_extra.isChecked()
        }
        for i, label in enumerate(config['legend']['label_names']):
            data_manager.get_growth_file(i).legend = label

        config['condition_legend'] = {
            'show': self.condition_legend_toggle.isChecked(),
            'title': self.condition_legend_title.text(),
            'label_names': self.condition_legend_names.get_list(),
            'extra_info': self.condition_extra_info.currentText(),
            'only_extra': self.condition_only_extra.isChecked()
        }
        for i, label in enumerate(config['condition_legend']['label_names']):
            data_manager.get_condition_file(i).legend = label

        # Style config
        config['style'] = {
            'style': self.style_dropdown.currentText(),
            'font_style': self.font_dropdown.currentText(),
            'title_size': self.title_size.get_float(),
            'legend_size': self.legend_size.get_float(),
            'label_size': self.label_size.get_float(),
            'line_width': self.line_width.get_float(),
            'axis_colour': self.axis_colour.text(),
            'marker_size': self.marker_size.get_float(),
            'capsize': self.capsize.get_float(),
            'save_dpi': self.save_dpi.get_float(),
            'grid': self.grid_toggle.isChecked()
        }

        # Stats config
        config['stats'] = {
            'std_err': self.std_err.isChecked(),
            'show_fit_text': self.show_fit_text.isChecked(),
            'show_fit_result': self.show_fit_result.isChecked(),
            'show_fit_errors': self.show_fit_errors.isChecked(),
            'sig_figs': self.sig_figs.get_int()
        }

        # Advanced config
        config['advanced']['savitsky_golay'] = {
            'window_size': self.sg_window_size.get_float(),
            'order': self.sg_order.get_float(),
            'deriv': self.sg_deriv.get_float(),
            'rate': self.sg_rate.get_float()
        }
        config['advanced']['outlier_threshold'] = self.outlier_threshold.get_float()
