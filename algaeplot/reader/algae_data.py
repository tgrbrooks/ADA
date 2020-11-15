from datetime import datetime, date, time
import numpy as np


# Class to store algae data
class AlgaeData():

    def __init__(self, file_name):
        self.name = file_name
        self.label = (file_name.split('/')[-1]).split('.')[0]
        # Header information
        self.date = date(1994, 3, 16)
        self.time = time(0, 0, 0)
        self.title = ''
        self.reactor = ''
        self.profile = ''
        # Data information
        self.xaxis = self.XAxis()
        self.signals = []
        self.events = []

    def get_header_info(self, info):
        if(info == 'date'):
            return self.date.strftime('%m/%d/%Y')
        if(info == 'time'):
            return self.time.strftime('%H:%M:%S')
        if(info == 'date+time'):
            return (self.date.strftime('%m/%d/%Y') + ', '
                    + self.time.strftime('%H:%M:%S'))
        if(info == 'title'):
            return self.title
        if(info == 'reactor'):
            return self.reactor
        if(info == 'profile'):
            return self.profile

    def get_signal(self, name):
        for sig in self.signals:
            if sig.name == name:
                return sig.data
        raise RuntimeError('Signal %s not found' % (name))

    def get_xdata(self, unit):
        if unit == 'seconds' or unit == '':
            return self.xaxis.data
        if unit == 'minutes':
            return self.xaxis.data / 60.
        if unit == 'hours':
            return self.xaxis.data / (60.*60.)
        if unit == 'days':
            return self.xaxis.data / (60.*60.*24.)

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

        def __init__(self, info=''):
            self.name = ''
            self.unit = ''
            self.range = 0
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

    class Event():

        def __init__(self):
            self.date = date(1994, 3, 16)
            self.time = time(0, 0, 0)
            self.xpos = 0
            self.label = ''
