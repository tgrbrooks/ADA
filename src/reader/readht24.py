# Standard imports
import os
import csv
from datetime import datetime, date, time
import numpy as np

# Local import
from src.reader.algemdata import AlgemData


# Loop over text files and read them in
def read_ht24(file_name, downsample=-1):
    algem_data_list = []
    with open(file_name, 'r', errors='ignore') as f:
        try:
            reader = csv.reader(f, delimiter=',') 
            # Process the header data first
            header = next(reader)
            x_name = ''
            x_unit = ''
            for i, name in enumerate(header):
                info = name.split(' ')
                if i == 0 and len(info) >= 1:
                    x_name = info[0]
                    if len(info) > 1:
                        x_unit = info[1][1:-1]
                if i != 0 and len(info) >= 2:
                    algem_data = AlgemData(file_name + ' (' + info[1] + ')')
                    algem_data.label = algem_data.label + ' (' + info[1] + ')'
                    algem_data.xaxis.name = x_name
                    algem_data.xaxis.unit = x_unit
                    algem_data.signals.append(algem_data.Signal())
                    algem_data.signals[0].name = info[0]
                    if len(info) > 2:
                        # Strip brackets from unit
                        algem_data.signals[0].unit = info[2][1:-1]
                    algem_data_list.append(algem_data)

            # Some error checking
            if(len(algem_data_list) == 0):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find any reactors')
            if(algem_data_list[0].xaxis.name == ''):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find time data')
            if(len(algem_data_list[0].signals) == 0):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find sensor data')

            # TODO when to load details file
            count = 0
            for row in reader:

                # Check if downsampling is used
                if downsample != -1:
                    if count % downsample != 0:
                        count = count + 1
                        continue
                count = count + 1

                x_data = 0
                for i, dat in enumerate(row):
                    try:
                        float(dat)
                    except Exception:
                        raise RuntimeError('Issue processing data:\n'
                                           'Could not convert %s on line %i '
                                           'to a number' % (dat, count))
                    if i == 0:
                        x_data = float(dat)
                    if i != 0:
                        algem_data_list[i-1].xaxis.append(x_data)
                        algem_data_list[i-1].signals[0].append(float(dat))

            # Check data has been read in
            if(algem_data_list[0].xaxis.data.size == 0):
                raise RuntimeError('Issue processing data:\n'
                                   'Did not read in any data')
            for sig in algem_data_list[0].signals:
                if(sig.data.size != algem_data_list[0].xaxis.data.size):
                    raise RuntimeError('Issue processing data:\n'
                                       'Different number of %s entries'
                                       % (sig.name))
            # If everything is successful return the algem data product
            return algem_data_list

        except Exception as e:
            raise RuntimeError('Error reading file '+file_name+'\n'+str(e))
