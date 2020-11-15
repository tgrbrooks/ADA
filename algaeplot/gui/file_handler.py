# pyqt imports
from PyQt5.QtWidgets import QWidget, QFileDialog

# local imports
from algaeplot.reader.read_algem_pro import read_algem_pro
from algaeplot.reader.read_algem_ht24 import (read_algem_ht24,
    read_algem_ht24_details)
from algaeplot.reader.algae_data import AlgaeData
from algaeplot.reader.data_holder import DataHolder


# Class to handle the file browser
class OpenFileHandlerGui(QWidget):

    def __init__(self, data=None, downsample=-1):
        super().__init__()
        self.title = 'Open Files'
        self.width = 640
        self.height = 480
        self.data = data
        self.downsample = downsample
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
                    self,
                    "Open File(s)",
                    "",
                    "All Files (*);;Text Files (*.txt)",
                    options=options)
        self.files = files
        if files and self.data:
            for file_name in files:
                if file_name.endswith('.txt'):
                    algem_data = read_algem_pro(file_name, self.downsample)
                    self.data.add_data(algem_data)
                elif file_name.endswith('.csv'):
                    # Assume there is no details file
                    if len(files) == 1:
                        algem_data_list = read_algem_ht24(file_name, self.downsample)
                        # Ask user if there is a details file
                        for algem_data in algem_data_list:
                            self.data.add_data(algem_data)
                    elif len(files) == 2 and files[1].endswith('.csv'):
                        algem_data_list, replicate_data_list = read_algem_ht24_details(file_name, 
                                                                                 files[1], 
                                                                                 self.downsample)
                        for algem_data in algem_data_list:
                            self.data.add_data(algem_data)
                        for replicate in replicate_data_list:
                            self.data.add_replicate(replicate[0], replicate[1])
                        break
                    else:
                        raise RuntimeError('Can only read in one HT-24 file\n'
                                           '(With optional details file)')
                else:
                    raise RuntimeError('%s is not a text or csv file'
                                       % (file_name))


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

        #self.show()

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

        #self.show()

    def saveDirectoryDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.directory_name = QFileDialog.getExistingDirectory(
                               self,
                               "Select Directory",
                               options=options)

def get_file_names():
    ex_file = OpenFileHandlerGui()
    files = ex_file.files
    ex_file.close()
    return ex_file.files


def open_files(data, downsample=-1):
    ex_file = OpenFileHandlerGui(data, downsample)


def save_file(fig):
    ex_file = SaveFileHandlerGui(fig)


def get_save_file_name():
    ex_file = SaveFileHandlerGui()
    return ex_file.file_name


def get_save_directory_name():
    ex_file = SaveDirectoryHandlerGui()
    return ex_file.directory_name
