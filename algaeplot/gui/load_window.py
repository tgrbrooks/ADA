import csv

from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget
from PyQt5.QtWidgets import QCheckBox, QPushButton, QComboBox

from algaeplot.gui.error_window import ErrorWindow
from algaeplot.gui.file_handler import get_file_names
from algaeplot.reader.read_algem_ht24 import (read_algem_ht24,
    read_algem_ht24_details)
from algaeplot.reader.read_algem_pro import read_algem_pro


class LoadWindow(QMainWindow):

    def __init__(self, parent, data):
        super(LoadWindow, self).__init__(parent)
        self.title = 'Load Files'
        self.width = 200
        self.height = 150
        self.parent = parent
        self.data = data
        self.details = None
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        layout = QGridLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        file_text = QLabel('File type:')
        file_text.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(file_text, 0, 0)
        self.file_type = QComboBox(self)
        self.file_type.addItem('Algem Pro')
        self.file_type.addItem('Algem HT24')
        self.file_type.addItem('IP T-Iso')
        self.file_type.addItem('PSI')
        self.file_type.addItem('csv')
        self.file_type.addItem('txt')
        layout.addWidget(self.file_type, 0, 1)

        select_file_button = QPushButton("Select data file(s)", self)
        select_file_button.clicked.connect(self.select_data)
        select_file_button.clicked.connect(self.update_options)
        select_file_button.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(select_file_button, 1, 0)

        self.file_name_text = QLabel('')
        self.file_name_text.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(self.file_name_text, 1, 1)

        self.select_details_button = QPushButton("Select details file", self)
        self.select_details_button.clicked.connect(self.select_details)
        self.select_details_button.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(self.select_details_button, 2, 0)
        self.select_details_button.hide()

        self.details_name_text = QLabel('')
        self.details_name_text.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(self.details_name_text, 2, 1)
        self.details_name_text.hide()

        load_button = QPushButton("Load", self)
        load_button.clicked.connect(self.load)
        load_button.setStyleSheet(
            'font-size: 14pt; font-weight: bold; font-family: Courier;'
        )
        layout.addWidget(load_button, 3, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_options(self):
        if self.file_type.currentText() == 'Algem HT24':
            self.select_details_button.show()
            self.details_name_text.show()
        else:
            self.select_details_button.hide()
            self.details_name_text.hide()

    def select_data(self):
        try:
            self.files = get_file_names()
            file_name_text = ''
            for file_name in self.files:
                file_name_text += file_name + '\n'
            self.file_name_text.setText(file_name_text)
            self.show()
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def select_details(self):
        try:
            self.details = get_file_names()
            details_name_text = ''
            for file_name in self.details:
                details_name_text += file_name + ', '
            self.details_name_text.setText(details_name_text)
        except Exception as e:
            print('Error: ' + str(e))
            self.error = ErrorWindow(str(e), self)
            self.error.show()

    def load(self):
        file_type = self.file_type.currentText()
        extension = '.csv'
        if file_type == 'txt' or file_type == 'Algem Pro':
            extension = '.txt'
        for file_name in self.files:
            if not file_name.endswith(extension):
                raise RuntimeError("File %s has the wrong extension" % (file_name))
            if file_type == 'Algem Pro':
                algem_data = read_algem_pro(file_name,
                                            self.parent.config.downsample)
                self.data.add_data(algem_data)
            elif file_type == 'Algem HT24' and not self.details:
                algem_data_list = read_algem_ht24(file_name,
                                                  self.parent.config.downsample)
                for algem_data in algem_data_list:
                    self.data.add_data(algem_data)
            elif file_type == 'Algem HT24':
                algem_data_list, replicate_data_list = read_algem_ht24_details(
                    file_name, self.details[0], self.parent.config.downsample)
                for algem_data in algem_data_list:
                    self.data.add_data(algem_data)
                for replicate in replicate_data_list:
                    self.data.add_replicate(replicate[0], replicate[1])
        self.parent.update_data_list()
        self.close()