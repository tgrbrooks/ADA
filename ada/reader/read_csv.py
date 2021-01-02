# Standard imports
import os
import csv
from datetime import datetime, date, time
import numpy as np

# Local import
from ada.reader.algae_data import AlgaeData


# Loop over ADA csv files and read them in
def read_csv(file_name):
    csv_data = AlgaeData(file_name)
    condition_data = AlgaeData(file_name)
    with open(file_name, 'r', errors='ignore') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0].lower() == 'name':
                csv_data.reactor = row[1]
                condition_data.reactor = row[1]
                csv_data.title = row[3]
                condition_data.title = row[3]
                csv_data.reactor = row[5]
                condition_data.reactor = row[5]
                csv_data.profile = row[7]
                condition_data.profile = row[7]

            elif row[0].lower() == 'date':
                date_str = row[1].split('-')
                start_date = date(int(date_str[0]), int(date_str[1]),
                                  int(date_str[2]))
                csv_data.date = start_date
                condition_data.date = start_date
                time_str = row[3].split(':')
                start_time = time(int(time_str[0]), int(time_str[1]),
                                  int(time_str[2]))
                csv_data.time = start_time
                condition_data.time = start_time

            elif row[0].find('Time') == 0:
                csv_data.xaxis.name = row[0].split(' [')[0]
                csv_data.xaxis.unit = row[0].split(' [')[1].split(']')[0]
                condition_data.xaxis.name = row[0].split(' [')[0]
                condition_data.xaxis.unit = row[0].split(' [')[1].split(']')[0]
                is_conditions = False
                cond_i = 0
                for i, measurement_name in enumerate(row):
                    if i == 0:
                        continue
                    if measurement_name.lower() in ['conditions', 'condition']:
                        is_conditions = True
                        cond_i = i
                        continue
                    if measurement_name == '':
                        continue
                    signal = csv_data.Signal()
                    signal.name = measurement_name.split(' [')[0]
                    if len(measurement_name.split(' [')) < 2:
                        signal.unit = ''
                    else:
                        signal.unit = measurement_name.split(' [')[0].split(']')[0]
                    if not is_conditions:
                        csv_data.signals.append(signal)
                    else:
                        condition_data.signals.append(signal)

            else:
                for i, measurement in enumerate(row):
                    if measurement == '':
                        continue
                    if i == 0:
                        csv_data.xaxis.append(float(measurement))
                        condition_data.xaxis.append(float(measurement))
                    elif i < cond_i:
                        csv_data.signals[i-1].append(float(measurement))
                    elif i > cond_i:
                        condition_data.signals[i-cond_i-1].append(float(measurement))

    # Some error checking
    if(csv_data.xaxis.name == ''):
        raise RuntimeError('Issue processing header:\n'
                           'Could not find time (Horiz) data')
    if(len(csv_data.signals) == 0):
        raise RuntimeError('Issue processing header:\n'
                           'Could not find sensor data')
            
    # Check data has been read in
    if(csv_data.xaxis.data.size == 0):
        raise RuntimeError('Issue processing data:\n'
                           'Did not read in any data')
    for sig in csv_data.signals:
        if(sig.data.size != csv_data.xaxis.data.size):
            raise RuntimeError('Issue processing data:\n'
                               'Different number of %s entries'
                               % (sig.name))

    # If everything is successful return the csv data product
    return csv_data, condition_data
