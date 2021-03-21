# Standard imports
import os
import csv
from datetime import datetime, date, time
import numpy as np
from dateutil.parser import parse

# Local import
from ada.data.algae_data import AlgaeData


# Loop over ADA csv files and read them in
def read_ada(file_name):
    ada_data = AlgaeData(file_name)
    condition_data = AlgaeData(file_name)
    has_conditions = False
    with open(file_name, 'r', errors='ignore') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0].lower() == 'name':
                ada_data.reactor = row[1]
                condition_data.reactor = row[1]
                ada_data.title = row[3]
                condition_data.title = row[3]
                ada_data.reactor = row[5]
                condition_data.reactor = row[5]
                ada_data.profile = row[7]
                condition_data.profile = row[7]

            elif row[0].lower() == 'date':
                start_date = parse(row[1]).date()
                ada_data.date = start_date
                condition_data.date = start_date
                start_time = parse(row[3]).time()
                ada_data.time = start_time
                condition_data.time = start_time

            elif row[0].find('Time') == 0:
                ada_data.xaxis.name = row[0].split(' [')[0]
                ada_data.xaxis.unit = row[0].split(' [')[1].split(']')[0]
                condition_data.xaxis.name = row[0].split(' [')[0]
                condition_data.xaxis.unit = row[0].split(' [')[1].split(']')[0]
                is_conditions = False
                cond_i = 0
                for i, measurement_name in enumerate(row):
                    if i == 0:
                        continue
                    if measurement_name.lower() in ['conditions', 'condition']:
                        is_conditions = True
                        has_conditions = True
                        cond_i = i
                        continue
                    if measurement_name == '':
                        continue
                    signal = ada_data.Signal()
                    signal.name = measurement_name.split(' [')[0]
                    if len(measurement_name.split(' [')) < 2:
                        signal.unit = ''
                    else:
                        signal.unit = measurement_name.split(
                            ' [')[0].split(']')[0]
                    if not is_conditions:
                        ada_data.signals.append(signal)
                    else:
                        condition_data.signals.append(signal)

            else:
                for i, measurement in enumerate(row):
                    if measurement == '':
                        continue
                    if i == 0:
                        ada_data.xaxis.append(float(measurement))
                        if has_conditions:
                            condition_data.xaxis.append(float(measurement))
                    elif i < cond_i or not has_conditions:
                        ada_data.signals[i-1].append(float(measurement))
                    elif i > cond_i:
                        condition_data.signals[i-cond_i -
                                               1].append(float(measurement))

    # Some error checking
    if(ada_data.xaxis.name == ''):
        raise RuntimeError('Issue processing header:\n'
                           'Could not find time (Horiz) data')
    if(len(ada_data.signals) == 0):
        raise RuntimeError('Issue processing header:\n'
                           'Could not find sensor data')

    # Check data has been read in
    if(ada_data.xaxis.data.size == 0):
        raise RuntimeError('Issue processing data:\n'
                           'Did not read in any data')
    for sig in ada_data.signals:
        if(sig.data.size != ada_data.xaxis.data.size):
            raise RuntimeError('Issue processing data:\n'
                               'Different number of %s entries'
                               % (sig.name))

    if not has_conditions:
        condition_data = None

    # If everything is successful return the csv data product
    return ada_data, condition_data
