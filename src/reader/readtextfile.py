# Local import
from src.reader.algemdata import AlgemData

# Standard imports
import os
from datetime import datetime, date, time
import numpy as np

# Loop over text files and read them in
def read_text_file(file_name, downsample=-1):
    algem_data = AlgemData(file_name)
    with open(file_name, 'r', errors='ignore') as f:
        try:
            # Process the header data first
            for line in f:
                if line.find('[Data]') != -1:
                    break
                # Get all the relevant data from header
                if line.find('Date=') == 0:
                    date_str = (line.split('"')[1]).split('/')
                    algem_data.date = date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
                if line.find('Time=') == 0:
                    time_str = (line.split('"')[1]).split(':')
                    algem_data.time = time(int(time_str[0]), int(time_str[1]), int(time_str[2]))
                if line.find('Title=') == 0:
                    algem_data.title = line.split('"')[1]
                if line.find('Stats=') == 0:
                    algem_data.reactor = line.split('ReactorName=')[1].split(',')[0]
                if line.find('Setup=') == 0:
                    algem_data.profile = line.split('.algp')[0].split('\\')[-1]
                if line.find('Horiz=') == 0:
                    info = (line.split('"')[1]).split(',')
                    algem_data.xaxis.set_info(info)
                if line.find('Signals') == 0 and line.find('"') != -1:
                    info = (line.split('"')[1]).split(',')
                    algem_data.signals.append(algem_data.Signal(info))

            # Some error checking
            if(algem_data.xaxis.name == ''):
                raise RuntimeError('Issue processing header:\nCould not find time (Horiz) data')
            if(len(algem_data.signals) == 0):
                raise RuntimeError('Issue processing header:\nCould not find sensor data')

            # Process the data with any downsampling included
            f.seek(0)
            begin_read = False
            count = 0
            for line in f:
                if line.find('[Data]') != -1:
                    begin_read = True
                if line.find('[End]') != -1:
                    break
                if not begin_read:
                    continue

                # Check if downsampling is used
                if downsample != -1:
                    if count % downsample != 0:
                        count = count + 1
                        continue
                count = count + 1

                # Get the data from the columns
                data_str = line.split('\t')
                if len(data_str) != 1+len(algem_data.signals):
                    continue
                for i, dat in enumerate(data_str):
                    try:
                        float(dat)
                    except:
                        raise RuntimeError('Issue processing data:\nCould not convert %s on line %i to a number' % (dat, count))
                    if i == 0:
                        algem_data.xaxis.append(float(dat))
                        continue
                    algem_data.signals[i-1].append(float(dat))

            # Check data has been read in
            if(algem_data.xaxis.data.size == 0):
                raise RuntimeError('Issue processing data:\nDid not read in any data')
            for sig in algem_data.signals:
                if(sig.data.size != algem_data.xaxis.data.size):
                    raise RuntimeError('Issue processing data:\nDifferent number of %s entries' % (sig.name))

            # If everything is successful return the algem data product
            return algem_data

        except Exception as e:
            raise RuntimeError('Error reading file '+file_name+'\n'+str(e))
