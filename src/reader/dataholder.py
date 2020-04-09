# Local includes
from reader.algemdata import AlgemData

class DataHolder():

    def __init__(self):
        self.empty = True
        self.data_files = []

    def delete_data(self, i):
        if i >= 0 and i < len(self.data_files):
            self.data_files.pop(i)
        if len(self.data_files) == 0:
            self.empty = True

    def add_data(self, data):
        self.data_files.append(data)
        self.empty = False
