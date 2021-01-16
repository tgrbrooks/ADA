# Standard imports
import os
from datetime import datetime, date, time
import numpy as np
from dateutil.parser import parse

# Local import
from ada.reader.algae_data import AlgaeData


# Loop over text files and read them in
def read_algem_ht24_txt(file_name, downsample=-1):
    algem_data_dict = {}
    condition_data_dict = {}
    replicate_dict = {}
    date = datetime.now().date()
    time = datetime.now().time()
    title = ""
    with open(file_name, 'r', errors='ignore') as f:
        try:
            # Process the header data first
            for line in f:
                if line.find('[Data]') != -1:
                    break
                # Get all the relevant data from header
                if line.find('Date=') == 0:
                    date_str = (line.split('"')[1])
                    date = parse(date_str).date()
                if line.find('Time=') == 0:
                    time_str = (line.split('"')[1])
                    time = parse(time_str).time()
                if line.find('ExperimentName=') == 0:
                    title = line.split('"')[1]
                if line.find('ReactorDetails') == 0:
                    if line.find('ReactorDetails=') == 0:
                        continue
                    reactor = line.split('="')[1].split(',')[0]
                    profile = line.split('.algp')[0].split('\\')[-1]
                    name = file_name.split('/')[-1].split('.')[0] + ' (' + reactor + ')'

                    replicates = line.split('.algp,')[-1].split(',"')[0].split(',')
                    replicate_dict[reactor] = [replicates[5], replicates[6]]

                    algem_data = AlgaeData(file_name + ' (' + reactor + ')')
                    algem_data.label = name
                    algem_data.profile = profile
                    algem_data.date = date
                    algem_data.time = time
                    algem_data.title = title
                    algem_data.reactor = reactor
                    algem_data.xaxis.name = 'Time'
                    algem_data.xaxis.unit = 's'
                    algem_data.signals.append(algem_data.Signal())
                    algem_data.signals[0].name = 'OD'
                    algem_data_dict[reactor] = algem_data

                    condition_data = AlgaeData(file_name + ' (' + reactor + ')')
                    condition_data.label = name
                    condition_data.profile = profile
                    condition_data.date = date
                    condition_data.time = time
                    condition_data.title = title
                    condition_data.reactor = reactor
                    condition_data.xaxis.name = 'Time'
                    condition_data.xaxis.unit = 's'
                    condition_data.signals.append(condition_data.Signal())
                    condition_data.signals[0].name = 'Light'
                    condition_data.signals[0].unit = '$\mu$mol/m$^2$/s'
                    condition_data_dict[reactor] = condition_data

            # Some error checking
            if(len(algem_data_dict) == 0):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find any reactors')
            if(len(condition_data_dict) == 0):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find any reactors')

            # Process the data with any downsampling included
            f.seek(0)
            begin_read = False
            light_count = 0
            for line in f:
                if line.find('[Data]') != -1:
                    begin_read = True
                if line.find('[End]') != -1:
                    break
                if not begin_read:
                    continue

                data_str = line.split(',')
                if len(data_str) < 4:
                    continue
                # Check if downsampling is used
                if data_str[1] == 'Light':
                    if downsample != -1:
                        if light_count % downsample != 0:
                            light_count = light_count + 1
                            continue
                    light_count = light_count + 1

                reactor = data_str[0]
                if reactor not in algem_data_dict:
                    continue

                if data_str[1] == 'Light':
                    condition_data_dict[reactor].xaxis.append(float(data_str[2]))
                    condition_data_dict[reactor].signals[0].append(float(data_str[3]))
                else:
                    algem_data_dict[reactor].xaxis.append(float(data_str[2]))
                    algem_data_dict[reactor].signals[0].append(float(data_str[3]))

            # Separate out into replicates
            algem_data_list = []
            rep_algem_data_list = []
            cond_data_list = []
            rep_cond_data_list = []
            used_replicates = []
            index = 0
            for reac, reps in replicate_dict.items():
                all_reps = [reac, reps[0], reps[1]]
                if set(all_reps) in used_replicates:
                    continue
                used_replicates.append(set(all_reps))
                algem_data_list.append(algem_data_dict[reac])
                cond_data_list.append(condition_data_dict[reac])
                for rep in reps:
                    rep_algem_data_list.append([algem_data_dict[rep], index])
                    rep_cond_data_list.append([condition_data_dict[rep], index])
                index += 1

            # If everything is successful return the algem data product
            return algem_data_list, rep_algem_data_list, cond_data_list, rep_cond_data_list

        except Exception as e:
            raise RuntimeError('Error reading file '+file_name+'\n'+str(e))
