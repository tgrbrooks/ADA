# pyqt imports
from PyQt5.QtWidgets import QWidget, QFileDialog

import configuration as config
import styles as styles
from logger import logger


# Class to handle the file browser
class FileHandlerGui(QWidget):

    def __init__(self, purpose='open', fig=None):
        super().__init__()
        if purpose == 'open':
            self.title = 'Open Files'
        elif purpose == 'save':
            self.title = 'Save File'
        elif purpose == 'directory':
            self.title = 'Choose Directory'
        self.purpose = purpose
        if fig:
            self.fig = fig
            self.save_fig = True
        else:
            self.save_fig = False
        self.width = 960*config.wr
        self.height = 600*config.hr
        logger.debug('Creating file handler window [width:%.2f, height:%.2f]' % (
            self.width, self.height))
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        if self.purpose == 'open':
            self.openFileNamesDialog()
        if self.purpose == 'save':
            self.saveFileDialog()
        if self.purpose == 'directory':
            self.saveDirectoryDialog()

    def openFileNamesDialog(self):
        logger.debug('Creating window for getting file names for opening')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Open File(s)",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options)
        self.file_names = files

    def saveFileDialog(self):
        logger.debug('Creating window for creating file name for saving')
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
                self.fig.savefig('graph.png', dpi=1200)
            elif(self.file_name.find('.') == -1):
                self.fig.savefig(self.file_name + '.png')
            else:
                self.fig.savefig(self.file_name)

    def saveDirectoryDialog(self):
        logger.debug('Creating window for choosing save directory')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.directory_name = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            options=options)


def get_file_names():
    ex_file = FileHandlerGui('open')
    files = ex_file.file_names
    ex_file.close()
    return files


def save_file(fig):
    ex_file = FileHandlerGui('save', fig)
    ex_file.close()


def get_save_file_name():
    ex_file = FileHandlerGui('save')
    return ex_file.file_name


def get_save_directory_name():
    ex_file = FileHandlerGui('directory')
    return ex_file.directory_name
