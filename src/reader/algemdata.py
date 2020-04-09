from datetime import datetime, date, time
import numpy as np

class AlgemData():

    def __init__(self, file_name, lines):
        self.lines = lines
        self.name = file_name
        self.date = date(1994, 3, 16)
        self.time = time(0, 0, 0)
        self.title = ''
        self.xaxis = self.XAxis()
        self.signals = []
        self.process_header()
        self.read_data()

    def process_header(self):

        begin_read = False
        end_read = False

        for line in self.lines:
            # Check we're in the header
            if line.find('[Header]') != -1:
                begin_read = True
                continue
            if line.find('[Data]') != -1:
                end_read = True
            if not begin_read:
                continue
            if end_read:
                return

            # Get all the relevant data from header
            if line.find('Date=') == 0:
                date_str = (line.split('"')[1]).split('/')
                self.date = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
            if line.find('Time=') == 0:
                time_str = (line.split('"')[1]).split(':')
                self.time = time(int(time_str[0]), int(time_str[1]), int(time_str[2]))
            if line.find('Title=') == 0:
                self.title = line.split('"')[1]
            if line.find('Horiz=') == 0:
                info = (line.split('"')[1]).split(',')
                self.xaxis.set_info(info)
            if line.find('Signals') == 0 and line.find('"') != -1:
                info = (line.split('"')[1]).split(',')
                self.signals.append(self.Signal(info))

    def read_data(self):

        begin_read = False
        end_read = False

        for line in self.lines:
            
            # Check we're in the data section
            if line.find('[Data]') != -1:
                begin_read = True
                continue
            if line.find('[End]') != -1:
                end_read = True
            if not begin_read:
                continue
            if end_read:
                break

            # Get the data from the columns
            data_str = line.split('\t')
            if len(data_str) != 1+len(self.signals):
                continue
            for i, dat in enumerate(data_str):
                if i == 0:
                    self.xaxis.append(float(dat))
                    continue
                self.signals[i-1].append(float(dat))

    class XAxis():

        def __init__(self):
            self.name = ''
            self.unit = ''
            self.data = np.array([])

        def set_info(self, info):
            for i in info:
                if i.find('Name=') != -1:
                    self.name = i.split('=')[1]
                if i.find('Unit=') != -1:
                    self.unit = i.split('=')[1]

        def append(self, dat):
            self.data = np.append(self.data, dat)

        def title(self):
            return self.name + " [" + self.unit + "]"

    class Signal():

        def __init__(self):
            self.name = ''
            self.unit = ''
            self.range = 0
            self.data = np.array([])

        def __init__(self, info):
            for i in info:
                if i.find('Name=') != -1:
                    self.name = i.split('=')[1]
                if i.find('Unit=') != -1:
                    self.unit = i.split('=')[1]
                if i.find('Range=') != -1:
                    self.range = int(i.split('=')[1])
            self.data = np.array([])

        def append(self, dat):
            self.data = np.append(self.data, dat)

        def title(self):
            return self.name + " [" + self.unit + "]"
