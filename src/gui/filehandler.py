# local imports
from reader.readtextfile import read_text_file
from reader.algemdata import AlgemData
from reader.dataholder import DataHolder

# pyqt imports
from PyQt5.QtWidgets import QWidget, QFileDialog

# Class to handle the file browser
class OpenFileHandlerGui(QWidget):

    def __init__(self, data, downsample=-1):
        super().__init__()
        self.title = 'Open Files'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.data = data
        self.downsample = downsample
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.openFileNamesDialog()
        
        self.show()
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Open File(s)", "","All Files (*);;Text Files (*.txt)", options=options)
        if files:
            for file_name in files:
                if not file_name.endswith('.txt'):
                    raise RuntimeError('%s is not a text file' % (file_name))
                algem_data = read_text_file(file_name, self.downsample)
                self.data.add_data(algem_data)

# Class to handle the file browser
class SaveFileHandlerGui(QWidget):

    def __init__(self, fig):
        super().__init__()
        self.title = 'Save File'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.fig = fig
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.saveFileDialog()
        
        self.show()
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            if(file_name == ''):
                self.fig.savefig('graph.png')
            elif(file_name.find('.') == -1):
                self.fig.savefig(file_name + '.png')
            else:
                self.fig.savefig(file_name)

def open_files(data, downsample=-1):
    ex_file = OpenFileHandlerGui(data, downsample)

def save_file(fig):
    ex_file = SaveFileHandlerGui(fig)
