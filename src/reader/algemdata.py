from datetime import datetime, date, time
import numpy as np

# Class to store algem data
class AlgemData():

    def __init__(self, file_name, lines, downsample=-1):
        self.lines = lines
        self.name = file_name
        self.downsample = downsample
        self.label = (file_name.split('/')[-1]).split('.')[0]
        self.date = date(1994, 3, 16)
        self.time = time(0, 0, 0)
        self.title = ''
        self.xaxis = self.XAxis()
        self.signals = []
        self.process_header()
        self.read_data()

    # Function: Read the header and extract useful information
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

        # Some error checking
        if(self.xaxis.name == ''):
            raise RuntimeError('Issue processing header:\nCould not find time (Horiz) data')

        if(len(self.signals) == 0):
            raise RuntimeError('Issue processing header:\nCould not find sensor data')

    # Function: Read the data and store it in a useful way
    def read_data(self):

        begin_read = False
        end_read = False

        increment = 1
        if(self.downsample != -1):
            increment = self.downsample
        for line_i in range(0, len(self.lines), increment):
            
            # Check we're in the data section
            if self.lines[line_i].find('[Data]') != -1:
                begin_read = True
                continue
            if self.lines[line_i].find('[End]') != -1:
                end_read = True
            if not begin_read:
                continue
            if end_read:
                break

            # Get the data from the columns
            data_str = self.lines[line_i].split('\t')
            if len(data_str) != 1+len(self.signals):
                continue
            for i, dat in enumerate(data_str):
                try:
                    float(dat)
                except:
                    raise RuntimeError('Issue processing data:\nCould not convert %s on line %i to a number' % (dat, line_i))
                if i == 0:
                    self.xaxis.append(float(dat))
                    continue
                self.signals[i-1].append(float(dat))

        # Check data has been read in
        if(self.xaxis.data.size == 0):
            raise RuntimeError('Issue processing data:\nDid not read in any data')
        for sig in self.signals:
            if(sig.data.size != self.xaxis.data.size):
                raise RuntimeError('Issue processing data:\nDifferent number of %s entries' % (sig.name))


    # Class: Store x axis data (time)
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

    # Class: Store generic sensor data
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
                    self.range = float(i.split('=')[1])
            self.data = np.array([])

        def append(self, dat):
            self.data = np.append(self.data, dat)

        def title(self):
            return self.name + " [" + self.unit + "]"
