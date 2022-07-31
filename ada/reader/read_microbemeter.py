# Standard imports
import csv
from dateutil.parser import parse

# Local import
from ada.data.algae_data import AlgaeData


# Loop over text files and read them in
def read_microbemeter(file_name, downsample=-1):
    data_list = []
    condition_data = AlgaeData(file_name)
    with open(file_name, 'r', errors='ignore') as f:
        try:
            reader = csv.reader(f, delimiter='\t')
            # Process the header data first
            header = next(reader)
            title = ''
            date = ''
            for _, name in enumerate(header):
                if name.find("Experiment Name:") != -1:
                    title = name.split(": ")[1]
                if name.find("Date:") != -1:
                    date = parse(name.split(": ")[1])
            headings = next(reader)
            first_data = next(reader)
            start_datetime = parse(first_data[0])

            condition_data.title = title
            condition_data.date = date.date()
            condition_data.time = date.time()
            condition_data.xaxis.name = headings[0]
            condition_data.xaxis.unit = 's'
            condition_data.xaxis.append(0)
            condition_data.signals.append(condition_data.Signal())
            condition_data.signals[0].name = headings[1]
            condition_data.signals[0].unit = 'C'
            condition_data.signals[0].append(float(first_data[1]))

            for i, name in enumerate(headings):
                if i >= 2 and first_data[i] != 'Blank':
                    data = AlgaeData(file_name + ' (' + name + ')')
                    data.title = title
                    data.date = date.date()
                    data.time = date.time()
                    data.label = '(' + name + ') ' + data.label
                    data.reactor = name
                    data.xaxis.name = headings[0]
                    data.xaxis.unit = 's'
                    data.signals.append(data.Signal())
                    data.signals[0].name = 'OD'
                    data.xaxis.append(0)
                    data.signals[0].append(float(first_data[i]))
                    data_list.append(data)

            if(len(data_list) == 0):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find any reactors')
            if(data_list[0].xaxis.name == ''):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find time data')
            if(len(data_list[0].signals) == 0):
                raise RuntimeError('Issue processing header:\n'
                                   'Could not find sensor data')

            count = 0
            for row in reader:
                # Check if downsampling is used
                if downsample != -1:
                    if count % downsample != 0:
                        count = count + 1
                        continue
                count = count + 1

                current_datetime = parse(row[0])
                x_data = (current_datetime - start_datetime).total_seconds()
                condition_data.xaxis.append(x_data)
                condition_data.signals[0].append(float(row[1]))
                for i, dat in enumerate(row):
                    if i < 2 or dat == 'Blank':
                        continue
                    try:
                        float(dat)
                    except Exception:
                        raise RuntimeError('Issue processing data:\n'
                                           'Could not convert %s on line %i '
                                           'to a number' % (dat, count))
                    data_list[i-2].xaxis.append(x_data)
                    data_list[i-2].signals[0].append(float(dat))

            # Check data has been read in
            if(data_list[0].xaxis.data.size == 0):
                raise RuntimeError('Issue processing data:\n'
                                   'Did not read in any data')
            for sig in data_list[0].signals:
                if(sig.data.size != data_list[0].xaxis.data.size):
                    raise RuntimeError('Issue processing data:\n'
                                       'Different number of %s entries'
                                       % (sig.name))
            # If everything is successful return the algem data product
            return data_list, condition_data

        except Exception as e:
            raise RuntimeError('Error reading file '+file_name+'\n'+str(e))
