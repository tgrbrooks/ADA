# Standard imports
import os
import csv
from datetime import datetime, date, time
import numpy as np

# Local import
from ada.reader.algae_data import AlgaeData


def str_to_datetime(datetime_str):
    date_str = (datetime_str.split(' ')[0]).split('/')
    time_str = (datetime_str.split(' ')[1]).split(':')
    datetime_out = datetime(int(date_str[2]), int(date_str[0]),
                            int(date_str[1]), int(time_str[0]),
                            int(time_str[1]), 0)
    return datetime_out


# Loop over text files and read them in
def read_ip_t_iso(file_name):
    ip_data = AlgaeData(file_name)
    condition_data = AlgaeData(file_name)
    with open(file_name, 'r', errors='ignore') as f:
        reader = csv.reader(f, delimiter=',')
        device_header = next(reader)
        ip_data.reactor = device_header[0]
        condition_data.reactor = device_header[0]

        name_header = next(reader)
        ip_data.title = name_header[1]
        condition_data.title = name_header[1]

        measurement_header = next(reader)
        od_index = 0
        for i, measurement_title in enumerate(measurement_header):
            if i == 0:
                ip_data.xaxis.name = 'Time'
                ip_data.xaxis.unit = 's'
                condition_data.xaxis.name = 'Time'
                condition_data.xaxis.unit = 's'
            elif measurement_title == 'RelativeDensity':
                ip_signal = ip_data.Signal()
                ip_signal.name = 'OD'
                ip_signal.unit = ''
                ip_data.signals.append(ip_signal)
                od_index = i
            else:
                condition_signal = condition_data.Signal()
                if len(measurement_title.split('_')) == 2:
                    condition_signal.name = measurement_title.split('_')[0]
                    condition_signal.unit = measurement_title.split('_')[1]
                else:
                    condition_signal.name = measurement_title
                    condition_signal.unit = ''
                condition_data.signals.append(condition_signal)

        # Some error checking
        if(ip_data.xaxis.name == ''):
            raise RuntimeError('Issue processing header:\n'
                               'Could not find time (Horiz) data')
        if(len(ip_data.signals) == 0):
            raise RuntimeError('Issue processing header:\n'
                               'Could not find sensor data')
                    
        first_measurement = next(reader)
        start_datetime = str_to_datetime(first_measurement[0])
        ip_data.date = start_datetime.date()
        condition_data.date = start_datetime.date()
        ip_data.time = start_datetime.time()
        condition_data.time = start_datetime.time()

        cond_i = 0
        for i, measurement in enumerate(first_measurement):
            if i == 0:
                ip_data.xaxis.append(0)
                condition_data.xaxis.append(0)
            elif i == od_index:
                ip_data.signals[0].append(float(measurement))
            else:
                condition_data.signals[cond_i].append(float(measurement))
                cond_i += 1;

        for row in reader:
            if row[0] == "Event: ":
                current_datetime = str_to_datetime(row[1])
                time_diff = (current_datetime - start_datetime).total_seconds()
                # Possible to have multiple events at the same time
                found_existing = False
                for evt in ip_data.events:
                    if time_diff == evt.xpos:
                        found_existing =  True
                        evt.labels.append(row[2])
                if not found_existing:
                    data_event = ip_data.Event()
                    data_event.datetime = current_datetime
                    data_event.xpos = time_diff
                    data_event.labels = [row[2]]
                    ip_data.events.append(data_event)
                continue
            current_datetime = str_to_datetime(row[0])
            time_diff = (current_datetime - start_datetime).total_seconds()
            cond_i = 0
            for i, measurement in enumerate(row):
                if i == 0:
                    ip_data.xaxis.append(time_diff)
                    condition_data.xaxis.append(time_diff)
                elif i == od_index:
                    ip_data.signals[0].append(float(measurement))
                else:
                    condition_data.signals[cond_i].append(float(measurement))
                    cond_i += 1

            
    # Check data has been read in
    if(ip_data.xaxis.data.size == 0):
        raise RuntimeError('Issue processing data:\n'
                           'Did not read in any data')
    for sig in ip_data.signals:
        if(sig.data.size != ip_data.xaxis.data.size):
            raise RuntimeError('Issue processing data:\n'
                               'Different number of %s entries'
                               % (sig.name))

    # If everything is successful return the IP data product
    return ip_data, condition_data
