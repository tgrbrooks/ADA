# pyqt imports
from PyQt5.QtWidgets import QWidget, QFileDialog

# local imports
from src.reader.readtextfile import read_text_file
from src.reader.algemdata import AlgemData
from src.reader.dataholder import DataHolder


# Class to handle the file browser
class OpenFileHandlerGui(QWidget):

    def __init__(self, data, downsample=-1, row=-1):
        super().__init__()
        self.title = 'Open Files'
        self.width = 640
        self.height = 480
        self.data = data
        self.downsample = downsample
        self.row = row
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        self.openFileNamesDialog()

        self.show()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
                    self,
                    "Open File(s)",
                    "",
                    "All Files (*);;Text Files (*.txt)",
                    options=options)
        if files:
            for file_name in files:
                if not file_name.endswith('.txt'):
                    raise RuntimeError('%s is not a text file' % (file_name))
                algem_data = read_text_file(file_name, self.downsample)
                if(self.row == -1):
                    self.data.add_data(algem_data)
                else:
                    self.data.add_replicate(algem_data, self.row)


# Class to handle the file browser
class SaveFileHandlerGui(QWidget):

    def __init__(self, fig=None):
        super().__init__()
        self.title = 'Save File'
        self.width = 640
        self.height = 480
        if fig:
            self.fig = fig
            self.save_fig = True
        else:
            self.save_fig = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        self.saveFileDialog()

        self.show()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_name, _ = QFileDialog.getSaveFileName(
                             self,
                             "Save File",
                             "",
                             "All Files (*);;Text Files (*.txt)",
                             options=options)
        if self.file_name and self.save_fig:
            if(self.file_name == ''):
                self.fig.savefig('graph.png')
            elif(self.file_name.find('.') == -1):
                self.fig.savefig(self.file_name + '.png')
            else:
                self.fig.savefig(selg.file_name)


# Class to handle the file browser
class SaveDirectoryHandlerGui(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Select Directory'
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        self.saveDirectoryDialog()

        self.show()

    def saveDirectoryDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.directory_name = QFileDialog.getExistingDirectory(
                               self,
                               "Select Directory",
                               options=options)


def open_files(data, downsample=-1, row=-1):
    ex_file = OpenFileHandlerGui(data, downsample, row)


def save_file(fig):
    ex_file = SaveFileHandlerGui(fig)


def get_save_file_name():
    ex_file = SaveFileHandlerGui()
    return ex_file.file_name


def get_save_directory_name():
    ex_file = SaveDirectoryHandlerGui()
    return ex_file.directory_name
