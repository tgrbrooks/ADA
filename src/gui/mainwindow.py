# Local imports
from gui.filehandler import open_files
from plotter.mainplot import PlotCanvas
from reader.dataholder import DataHolder

# pyqt imports
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget, QGridLayout, QWidget, QTabWidget, QScrollArea, QVBoxLayout
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
        plot_layout.addWidget(list_scroll, 1, 4, 4, 1)

        # Plot button
        plot_button = QPushButton('Plot!', self)
        plot_button.clicked.connect(lambda: plot.plot(self.data))
        plot_button.setToolTip('Plot the data')
        plot_layout.addWidget(plot_button, 5, 4)

        # Saving options
        plot_layout.addWidget(Color('green'), 6, 0, 1, 5)

        # Plotting options window
        options_layout = QGridLayout()
        options_layout.setContentsMargins(0,0,0,0)
        options_layout.setSpacing(20)
        options_layout.addWidget(Color('green'), 0, 0)

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
        for data in self.data.data_files:
            self.data_list.addItem(data.name)

    def remove_item(self, index):
        print(index.row())
