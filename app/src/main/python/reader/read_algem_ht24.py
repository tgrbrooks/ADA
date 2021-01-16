# Standard imports
import os
import csv
from datetime import datetime, date, time
import numpy as np
from dateutil.parser import parse

# Local import
from reader.algae_data import AlgaeData


# Loop over text files and read them in
def read_algem_ht24(file_name, downsample=-1):
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
                    algem_data = AlgaeData(file_name + ' (' + info[1] + ')')
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


def get_index(name, data_list):
    for i, data in enumerate(data_list):
        if data.label.split('(')[-1].split(')')[0] == name:
            return i
    return -1


def read_details(file_name, duplicate_name, downsample=-1):

    # Read in the algem data from the other file
    algem_data_list = read_algem_ht24(file_name, downsample)

    f = open(duplicate_name, 'r', errors='ignore')
    reader = csv.reader(f, delimiter=',')

    date_row = next(reader)
    date_all = parse(date_row[1]).date()

    time_row = next(reader)
    time_all = parse(time_row[1]).time()

    exp_name_row = next(reader)
    exp_name = ''
    if(len(exp_name_row) > 1):
        exp_name = exp_name_row

    reac_row = next(reader)
    reactor = ''
    if(len(reac_row) > 1):
        reactor = reac_row[1]

    setup_row = next(reader)

    profiles = []
    replicates = []
    for row in reader:
        if row[0].split(' ')[-1] == 'Profile':
            profile = row[1].split('.algp')[0].split('\\')[-1]
            profiles.append(profile)

        if row[0].split(' ')[-1] == 'Replicates':
            rep_list = [row[0].split(' ')[0]]
            for replicate in row[1].split(' ')[1:]:
                if replicate == rep_list[0]:
                    continue
                rep_list.append(replicate)
            replicates.append(rep_list)

    # Add the information to the algem data
    name_dict = {}
    for i, algem_data in enumerate(algem_data_list):
        algem_data.date = date_all
        algem_data.time = time_all
        algem_data.title = exp_name
        algem_data.reactor = reactor
        algem_data.profile = profiles[i]
        name_dict[algem_data.label.split('(')[-1].split(')')[0]] = i

    replicate_data_list = []
    used_replicates = []
    # Remove the replicates from main list and put in a new one
    for i, replicate in enumerate(replicates):
        # Check if replicates have been used
        if set(replicate) in used_replicates:
            continue
        first_data = replicate[0]
        first_i = get_index(first_data, algem_data_list)
        if len(replicate) != 1:
            # Loop over the replicates
            for rep in replicate[1:]:
                rep_i = get_index(rep, algem_data_list)
                replicate_data_list.append([algem_data_list[rep_i], first_i])
                algem_data_list.pop(rep_i)
        used_replicates.append(set(replicate))

    return algem_data_list, replicate_data_list

def read_algem_ht24_details(file_name1, file_name2, downsample=-1):
    
    # Determine which file is the details file
    f1 = open(file_name1, 'r', errors='ignore')
    reader1 = csv.reader(f1, delimiter=',')
    date1 = next(reader1)
    f2 = open(file_name2, 'r', errors='ignore')
    reader2 = csv.reader(f2, delimiter=',')
    date2 = next(reader2)

    # First file is details file
    if date1[0] == 'Date':
        f1.close()
        f2.close()
        return read_details(file_name2, file_name1, downsample)
    # Second file is details file
    elif date2[0] == 'Date':
        f1.close()
        f2.close()
        return read_details(file_name1, file_name2, downsample)
    else:
        raise RuntimeError('Neither file is a details file')
