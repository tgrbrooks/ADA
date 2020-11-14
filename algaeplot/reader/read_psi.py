# Standard imports
import os
import csv
from datetime import datetime, date, time
import numpy as np

import ezodf as ods

# Local import
from algaeplot.reader.algae_data import AlgaeData


def str_to_datetime(datetime_str):
    date_str = (datetime_str.split(' ')[0]).split('.')
    time_str = (datetime_str.split(' ')[1]).split(':')
    datetime_out = datetime(int(date_str[2]), int(date_str[1]),
                            int(date_str[0]), int(time_str[0]),
                            int(time_str[1]), int(time_str[2]))
    return datetime_out


# Loop over text files and read them in
def read_psi(file_name):
    psi_data = AlgaeData(file_name)
    condition_data = AlgaeData(file_name)

    ods_data = ods.opendoc(file_name)
    psi_index_map = {}
    cond_index_map = {}
    for sheet in ods_data.sheets:

        if sheet.name == 'Info':
            # Get title
            psi_data.title = sheet[0, 1].plaintext()
            condition_data.title = sheet[0, 1].plaintext()
            # Get start date
            start_datetime = str_to_datetime(sheet[1, 1].plaintext())
            psi_data.date = start_datetime.date()
            condition_data.date = start_datetime.date()
            # Get start time
            psi_data.time = start_datetime.time()
            condition_data.time = start_datetime.time()
            # Get profile (medium + organism)
            medium = sheet[10, 1].plaintext()
            organism = sheet[11, 1].plaintext()
            psi_data.profile = medium + ' ' + organism
            condition_data.profile = medium + ' ' + organism
            # Get time units
            psi_data.xaxis.name = 'Time'
            psi_data.xaxis.unit = 's'
            condition_data.xaxis.name = 'Time'
            condition_data.xaxis.unit = 's'

        if sheet.name == 'Devices':
            # Get reactor
            psi_data.reactor = sheet[1, 1].plaintext()
            condition_data.reactor = sheet[1, 1].plaintext()

        if sheet.name == 'Accessories':
            # Get titles and units of measurements
            psi_i = 0
            cond_i = 0
            for i in range(1, sheet.nrows()):
                measurement_key = sheet[i, 0].plaintext()
                measurement_name = sheet[i, 1].plaintext()
                measurement_unit = sheet[i, 2].plaintext()
                if measurement_name.find('OD') == 0:
                    psi_signal = psi_data.Signal()
                    psi_signal.name = measurement_name
                    psi_signal.unit = measurement_unit
                    psi_data.signals.append(psi_signal)
                    psi_index_map[measurement_key] = psi_i
                    psi_i += 1
                else:
                    condition_signal = condition_data.Signal()
                    condition_signal.name = measurement_name
                    condition_signal.unit = measurement_unit
                    condition_data.signals.append(condition_signal)
                    cond_index_map[measurement_key] = cond_i
                    cond_i += 1

        if sheet.name == 'Data':
            psi_col_index = {}
            cond_col_index = {}
            for j in range(2, sheet.ncols()):
                measurement_key = sheet[0, j].plaintext()
                if measurement_key in psi_index_map:
                    psi_col_index[j] = psi_index_map[measurement_key]
                if measurement_key in cond_index_map:
                    cond_col_index[j] = cond_index_map[measurement_key]
            # Get the measurement data
            for i in range(1, sheet.nrows()):
                time_s = float(sheet[i, 0].value) * 60 * 60
                od_measured = False
                condition_data.xaxis.append(time_s)
                for j in range(2, sheet.ncols()):
                    try:
                        measurement = sheet[i, j].value
                    except:
                        measurement = 0
                    if measurement != '':
                        measurement = float(measurement)
                    else:
                        measurement = None
                    if j in psi_col_index and measurement is not None:
                        psi_data.signals[psi_col_index[j]].append(measurement)
                        # Only record time if OD was measured
                        if not od_measured:
                            od_measured = True
                            psi_data.xaxis.append(time_s)
                    if j in cond_col_index:
                        if measurement is None:
                            measurement = condition_data.signals[cond_col_index[j]].data[-1]
                        condition_data.signals[cond_col_index[j]].append(measurement)

    # Some error checking
    if(psi_data.xaxis.name == ''):
        raise RuntimeError('Issue processing header:\n'
                           'Could not find time (Horiz) data')
    if(len(psi_data.signals) == 0):
        raise RuntimeError('Issue processing header:\n'
                           'Could not find sensor data')
            
    # Check data has been read in
    if(psi_data.xaxis.data.size == 0):
        raise RuntimeError('Issue processing data:\n'
                           'Did not read in any data')
    for sig in psi_data.signals:
        if(sig.data.size != psi_data.xaxis.data.size):
            print(sig.data.size)
            print(psi_data.xaxis.data.size)
            raise RuntimeError('Issue processing data:\n'
                               'Different number of %s entries'
                               % (sig.name))
                               
    # If everything is successful return the IP data product
    return psi_data, condition_data

