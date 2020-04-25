from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget, QCheckBox, QPushButton, QComboBox

from gui.errorwindow import ErrorWindow

class ExportWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(ExportWindow, self).__init__(parent)
        self.title = 'Export Files'
        self.left = 50
        self.top = 50
        self.width = 150
        self.height = 100
        self.parent = parent
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(5)

        file_text = QLabel('File type:')
        file_text.setStyleSheet('font-size: 14pt; font-weight: bold; font-family: Courier;')
        layout.addWidget(file_text, 0, 0)
        self.file_type = QComboBox(self)
        self.file_type.addItem('txt')
        self.file_type.addItem('csv')
        layout.addWidget(self.file_type, 0, 1)

        rename_text = QLabel('Rename with profile:')
        rename_text.setStyleSheet('font-size: 14pt; font-weight: bold; font-family: Courier;')
        layout.addWidget(rename_text, 1, 0)
        self.rename = QCheckBox(self)
        layout.addWidget(self.rename, 1, 1)

        export_button = QPushButton("Export", self)
        export_button.clicked.connect(self.export)
        export_button.setStyleSheet('font-size: 14pt; font-weight: bold; font-family: Courier;')
        layout.addWidget(export_button, 2, 0, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def export(self):
        extension = '.csv'
        if(self.file_type.currentText() == 'txt'):
            extension = '.txt'
        for data in parent.data.data_files:
            try:
                filename = data.name.split('.')[0] + extension
                if(self.rename.isChecked()):
                    filename = data.profile + extension
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
            except:
                e = str('Could not convert file %s to csv' % (data.name))
                print('Error: ' + e)
                self.error = ErrorWindow(e, self)
                self.error.show()

