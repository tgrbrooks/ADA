# Local imports
from gui.filehandler import open_files
from plotter.mainplot import PlotCanvas
from reader.dataholder import DataHolder
from gui.configuration import Configuration

# Standard imports
import csv

# pyqt imports
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget, QGridLayout, QWidget, QTabWidget, QScrollArea, QVBoxLayout, QSizePolicy, QComboBox, QLabel, QLineEdit, QCheckBox
from PyQt5.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

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

        # Main plotting window
        plot_layout = QGridLayout()
        plot_layout.setContentsMargins(0,0,0,0)
        plot_layout.setSpacing(20)

        # Main plot window (row, column, row extent, column extent)
        plot = PlotCanvas(self, width=10, height=4)
        plot_layout.addWidget(plot, 0, 0, 6, 4)

        # Add data button
        data_button = QPushButton('Add Data', self)
        data_button.clicked.connect(lambda: open_files(self.data))
        data_button.clicked.connect(self.update_data_list)
        data_button.setToolTip('Import data for plotting')
        data_button.setStyleSheet('font-size: 14pt; font-family: Courier;')
        plot_layout.addWidget(data_button, 0, 4)

        # Configure list behaviour
        self.data_list.clicked.connect(self.remove_item)

        # List of data
        list_scroll = QScrollArea(self)
        list_scroll.setWidgetResizable(True)
        scroll_content = QWidget(list_scroll)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)
        scroll_layout.addWidget(self.data_list)
        list_scroll.setWidget(scroll_content)
        list_scroll.setToolTip('Click to remove')
        plot_layout.addWidget(list_scroll, 1, 4)

        # Add data button
        condition_data_button = QPushButton('Add Condition Data', self)
        condition_data_button.clicked.connect(lambda: open_files(self.condition_data))
        condition_data_button.clicked.connect(self.update_condition_data_list)
        condition_data_button.setToolTip('Import condition data (temp, light, etc) for plotting')
        condition_data_button.setStyleSheet('font-size: 14pt; font-family: Courier;')
        plot_layout.addWidget(condition_data_button, 3, 4,)

        # Configure list behaviour
        self.condition_data_list.clicked.connect(self.remove_condition_item)

        # List of data
        condition_list_scroll = QScrollArea(self)
        condition_list_scroll.setWidgetResizable(True)
        condition_scroll_content = QWidget(condition_list_scroll)
        condition_scroll_layout = QVBoxLayout(condition_scroll_content)
        condition_scroll_content.setLayout(condition_scroll_layout)
        condition_scroll_layout.addWidget(self.condition_data_list)
        condition_list_scroll.setWidget(condition_scroll_content)
        condition_list_scroll.setToolTip('Click to remove')
        plot_layout.addWidget(condition_list_scroll, 4, 4)

        # Plot button
        plot_button = QPushButton('Plot!', self)
        plot_button.clicked.connect(self.update_config)
        plot_button.clicked.connect(lambda: plot.plot(self.data, self.condition_data, self.config))
        plot_button.setToolTip('Plot the data')
        plot_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        plot_button.setStyleSheet('font-size: 28pt; font-family: Courier;')
        plot_layout.addWidget(plot_button, 5, 4, 2, 1)

        # Saving options
        save_button = QPushButton('Save', self)
        plot_button.clicked.connect(self.update_config)
        save_button.clicked.connect(lambda: plot.save(self.config))
        save_button.setToolTip('Save the figure')
        save_button.setStyleSheet('font-size: 14pt; font-family: Courier;')
        plot_layout.addWidget(save_button, 6, 0)

        # Export options
        export_button = QPushButton('Export', self)
        export_button.clicked.connect(self.export_to_csv)
        export_button.setToolTip('Export the data to csv file')
        export_button.setStyleSheet('font-size: 14pt; font-family: Courier;')
        plot_layout.addWidget(export_button, 6, 1)

        # Measure gradient
        measure_button = QPushButton('Measure', self)
        measure_button.clicked.connect(self.toggle_cursor)
        measure_button.clicked.connect(lambda: plot.plot(self.data, self.condition_data, self.config))
        measure_button.setToolTip('Measure the growth rate')
        measure_button.setStyleSheet('font-size: 14pt; font-family: Courier;')
        plot_layout.addWidget(measure_button, 6, 2)

        # Toggle grid
        grid_button = QPushButton('Grid', self)
        grid_button.clicked.connect(self.toggle_grid)
        grid_button.clicked.connect(lambda: plot.plot(self.data, self.condition_data, self.config))
        grid_button.setToolTip('Toggle grid on/off')
        grid_button.setStyleSheet('font-size: 14pt; font-family: Courier;')
        plot_layout.addWidget(grid_button, 6, 3)

        # Plotting options window
        options_layout = QGridLayout()
        options_layout.setContentsMargins(0,0,0,0)
        options_layout.setSpacing(20)

        # File name
        options_layout.addWidget(QLabel('File name:'), 0, 0)
        self.file_name = QLineEdit(self) 
        options_layout.addWidget(self.file_name, 0, 1)

        # Figure title
        options_layout.addWidget(QLabel('Figure title:'), 0, 2)
        self.figure_title = QLineEdit(self) 
        options_layout.addWidget(self.figure_title, 0, 3)

        # Axis configuration
        options_layout.addWidget(QLabel('Axis configuration:'), 1, 0)
        options_layout.addWidget(QLabel('Variable'), 2, 1)
        options_layout.addWidget(QLabel('Label name'), 2, 2)
        options_layout.addWidget(QLabel('Unit name'), 2, 3)
        options_layout.addWidget(QLabel('X:'), 3, 0)
        options_layout.addWidget(QLabel('Y:'), 4, 0)
        options_layout.addWidget(QLabel('Y2 (conditions):'), 5, 0)

        # X axis drop down menu
        self.xaxis_dropdown = QComboBox(self)
        self.xaxis_dropdown.addItem("seconds")
        self.xaxis_dropdown.addItem("minutes")
        self.xaxis_dropdown.addItem("hours")
        self.xaxis_dropdown.addItem("days")
        options_layout.addWidget(self.xaxis_dropdown, 3, 1)

        # X axis titles
        self.xaxis_name = QLineEdit(self) 
        options_layout.addWidget(self.xaxis_name, 3, 2)
        self.xaxis_unit = QLineEdit(self) 
        options_layout.addWidget(self.xaxis_unit, 3, 3)

        # Y axis drop down menu
        self.yaxis_dropdown = QComboBox(self)
        options_layout.addWidget(self.yaxis_dropdown, 4, 1)

        # Y axis titles
        self.yaxis_name = QLineEdit(self) 
        options_layout.addWidget(self.yaxis_name, 4, 2)
        self.yaxis_unit = QLineEdit(self) 
        options_layout.addWidget(self.yaxis_unit, 4, 3)

        # Condition Y axis drop down menu
        self.condition_yaxis_dropdown = QComboBox(self)
        options_layout.addWidget(self.condition_yaxis_dropdown, 5, 1)

        # Y axis titles
        self.condition_yaxis_name = QLineEdit(self) 
        options_layout.addWidget(self.condition_yaxis_name, 5, 2)
        self.condition_yaxis_unit = QLineEdit(self) 
        options_layout.addWidget(self.condition_yaxis_unit, 5, 3)

        # Data configuration options
        options_layout.addWidget(QLabel('Data configuration:'), 6, 0)

        options_layout.addWidget(QLabel('Smooth data:'), 7, 0)
        self.smooth_data = QCheckBox(self)
        options_layout.addWidget(self.smooth_data, 7, 1)

        # Legend configuration options
        options_layout.addWidget(QLabel('Legend configuration:'), 8, 0)

        options_layout.addWidget(QLabel('Legend on:'), 9, 0)
        self.legend_toggle = QCheckBox(self)
        options_layout.addWidget(self.legend_toggle, 9, 1)

        options_layout.addWidget(QLabel('Legend titles:'), 9, 2)
        self.legend_names = QComboBox(self)
        self.legend_names.setEditable(True)
        self.legend_names.setInsertPolicy(2)
        options_layout.addWidget(self.legend_names, 9, 3)

        options_layout.addWidget(QLabel('Condition legend:'), 9, 4)
        self.condition_legend_names = QComboBox(self)
        self.condition_legend_names.setEditable(True)
        self.condition_legend_names.setInsertPolicy(2)
        options_layout.addWidget(self.condition_legend_names, 9, 5)

        # Add layouts to tabs via widgets
        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        tabs.addTab(plot_widget, 'Plotting')
        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        tabs.addTab(options_widget, 'Options')

        self.setCentralWidget(tabs)
        self.show()

    def update_data_list(self):
        self.data_list.clear()
        self.yaxis_dropdown.clear()
        self.legend_names.clear()
        for i, data in enumerate(self.data.data_files):
            self.data_list.addItem(data.name)
            self.legend_names.addItem(data.label)
            if i > 0:
                continue
            for sig in data.signals:
                self.yaxis_dropdown.addItem(sig.name)

    def update_condition_data_list(self):
        self.condition_data_list.clear()
        self.condition_yaxis_dropdown.clear()
        self.condition_legend_names.clear()
        for i, data in enumerate(self.condition_data.data_files):
            self.condition_data_list.addItem(data.name)
            self.condition_legend_names.addItem(data.label)
            if i > 0:
                continue
            for sig in data.signals:
                self.condition_yaxis_dropdown.addItem(sig.name)

    def remove_item(self, index):
        for i, data in enumerate(self.data.data_files):
            if i != index.row():
                continue
            self.data.delete_data(i)
        self.update_data_list()

    def remove_condition_item(self, index):
        for i, data in enumerate(self.condition_data.data_files):
            if i != index.row():
                continue
            self.condition_data.delete_data(i)
        self.update_condition_data_list()

    def toggle_cursor(self):
        self.config.cursor = not self.config.cursor

    def toggle_grid(self):
        self.config.grid = not self.config.grid

    def export_to_csv(self):
        for data in self.data.data_files:
            filename = data.name.replace('.txt', '.csv')
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                header = [data.xaxis.name]
                for sig in data.signals:
                    header.append(sig.name)
                writer.writerow(header)
                for i, xdat in enumerate(data.xaxis.data):
                    row = [xdat]
                    for sig in data.signals:
                        row.append(sig.data[i])
                    writer.writerow(row)

    def update_config(self):
        self.config.file_name = self.file_name.text()
        self.config.title = self.figure_title.text()
        self.config.xvar = self.xaxis_dropdown.currentText()
        self.config.xname = self.xaxis_name.text()
        self.config.xunit = self.xaxis_unit.text()
        self.config.yvar = self.yaxis_dropdown.currentText()
        self.config.yname = self.yaxis_name.text()
        self.config.yunit = self.yaxis_unit.text()
        self.config.condition_yvar = self.condition_yaxis_dropdown.currentText()
        self.config.condition_yname = self.condition_yaxis_name.text()
        self.config.condition_yunit = self.condition_yaxis_unit.text()
        self.config.smooth = self.smooth_data.isChecked()
        self.config.legend = self.legend_toggle.isChecked()
        self.config.label_names.clear()
        for i in range(self.legend_names.count()):
            self.config.label_names.append(self.legend_names.itemText(i))
        self.config.condition_label_names.clear()
        for i in range(self.condition_legend_names.count()):
            self.config.condition_label_names.append(self.condition_legend_names.itemText(i))
