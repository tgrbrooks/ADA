# local imports
from reader.readtextfile import read_text_file
from reader.algemdata import AlgemData
from reader.dataholder import DataHolder

# pyqt imports
from PyQt5.QtWidgets import QWidget, QFileDialog

class FileHandlerGui(QWidget):

    def __init__(self, mode, data):
        super().__init__()
        self.title = 'Files'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.mode = mode
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        if(self.mode == "open_file"):
            self.openFileNameDialog()
        if(self.mode == "open_files"):
            self.openFileNamesDialog()
        if(self.mode == "save_files"):
            self.saveFileDialog()
        
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Open File", "","All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            algem_data = read_text_file(file_name)
            self.data.add_data(algem_data)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Open File(s)", "","All Files (*);;Text Files (*.txt)", options=options)
        if files:
            for file_name in files:
                algem_data = read_text_file(file_name)
                self.data.add_data(algem_data)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(file_name)

def open_files(data):
    ex_file = FileHandlerGui("open_files", data)

def open_file(data):
    ex_file = FileHandlerGui("open_file", data)

def save_file(data):
    ex_file = FileHandlerGui("save_file", data)
