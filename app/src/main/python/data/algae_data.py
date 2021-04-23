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
        self.sub_reactor = ''
        self.profile = ''
        # Data information
        self.xaxis = self.XAxis()
        self.signals = []
        self.events = []

    def get_header_info(self, info):
        if(info == 'date'):
            return self.date.strftime('%d/%m/%Y')
        if(info == 'time'):
            return self.time.strftime('%H:%M:%S')
        if(info == 'date+time'):
            return (self.date.strftime('%d/%m/%Y') + ', '
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

    def get_signal_unit(self, name):
        for sig in self.signals:
            if sig.name == name:
                return sig.unit
        raise RuntimeError('Signal %s not found' % (name))

    def get_xdata(self, time_unit):
        if time_unit == 'seconds' or time_unit == '':
            return self.xaxis.data
        if time_unit == 'minutes':
            return self.xaxis.data / 60.
        if time_unit == 'hours':
            return self.xaxis.data / (60.*60.)
        if time_unit == 'days':
            return self.xaxis.data / (60.*60.*24.)

    def get_xtitle(self, time_unit, name, unit_name):
        x_title = self.xaxis.title()
        if(name != ''):
            x_title = x_title.replace(self.xaxis.name, name)
        x_unit = self.xaxis.unit
        if(time_unit == 'seconds'):
            x_unit = 'sec'
        if(time_unit == 'minutes'):
            x_unit = 'min'
        if(time_unit == 'hours'):
            x_unit = 'hr'
        if(time_unit == 'days'):
            x_unit = 'day'
        if(unit_name != ''):
            x_unit = unit_name

        if(unit_name == 'none'):
            x_title = x_title.replace(" ["+self.xaxis.unit+"]", "")
        else:
            x_title = x_title.replace("["+self.xaxis.unit+"]", "["+x_unit+"]")
        return x_title
        
    def get_ydata(self, yvar, calib=None):
        found_ydata = False
        for sig in self.signals:
            if sig.name == yvar:
                # Loaded calibration curve takes precedence
                if yvar == 'CD' and calib is not None:
                    continue
                found_ydata = True
                ydata = sig.data
            elif yvar == 'CD' and calib is not None and sig.name == 'OD':
                found_ydata = True
                ydata = calib.calibrate_od(sig.data)
        if not found_ydata:
            raise RuntimeError('Could not find signal %s' % (yvar))
        return ydata

    def get_ytitle(self, yvar, name, unit_name, calib=None, normlog=False):
        y_title = ''
        for sig in self.signals:
            if sig.name == yvar:
                if yvar == 'CD' and calib is not None:
                    continue
                y_title = sig.title()
                if(name != ''):
                    y_title = y_title.replace(sig.name, name)
                if(unit_name.lower() == 'none'):
                    y_title = y_title.replace(" ["+sig.unit+"]", "")
                elif(unit_name != ''):
                    y_title = y_title.replace("["+sig.unit+"]", "["+unit_name+"]")
            elif yvar == 'CD' and calib is not None and sig.name == 'OD':
                y_title = 'CD'
                if(name != ''):
                    y_title = y_title.replace(y_title, name)
                if(unit_name != ''):
                    y_title = y_title + " ["+unit_name+"]"
        if normlog and name == '':
            y_title = 'ln('+yvar+'/'+yvar+'$_{0}$)'
            if(name != ''):
                y_title = y_title.replace(y_title, name)
            if(unit_name != ''):
                y_title = y_title + " ["+unit_name+"]"
        return y_title


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
            if self.unit.lower() in ['m', 'min', 'mins', 'minutes', 'minute']:
                self.data = np.append(self.data, dat * 60.)
            elif self.unit.lower() in ['h', 'hr', 'hrs', 'hour', 'hours']:
                self.data = np.append(self.data, dat * 60. * 60.)
            elif self.unit.lower() in ['d', 'day', 'days']:
                self.data = np.append(self.data, dat * 60. * 60. * 24.)
            else:
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
            self.datetime = datetime(1994, 3, 16, 0, 0, 0)
            self.xpos = 0
            self.labels = []

        def get_xpos(self, time_unit):
            if time_unit == 'seconds' or time_unit == '':
                return self.xpos
            if time_unit == 'minutes':
                return self.xpos / 60.
            if time_unit == 'hours':
                return self.xpos / (60.*60.)
            if time_unit == 'days':
                return self.xpos / (60.*60.*24.)
