# Standard imports
from dateutil.parser import parse

import ezodf as ods

# Local import
from ada.data.algae_data import AlgaeData


# Loop over text files and read them in
def read_spectrostar(file_name):
    spectrostar_data = {}

    ods_data = ods.opendoc(file_name)
    for sheet in ods_data.sheets:

        if sheet.name == 'All_Cycles':
            # Get title
            title = sheet[3, 0].plaintext().split(': ')[1]
            # Get start date
            start_datetime = parse(sheet[4, 0].plaintext().split(': ')[1]+' '+sheet[5,0].plaintext().split(': ')[1])
            data_date = start_datetime.date()
            # Get start time
            data_time = start_datetime.time()

            times = [0]
            col = 5
            while sheet[11, col].plaintext() != '':
                time = sheet[11, col].plaintext().split(':')
                times.append(60*60*int(time[0]) + 60*int(time[1]) + int(time[2]))
                col += 1

            for i in range(12, 72):
                if sheet[i, 1].plaintext() == '':
                    continue
                data = AlgaeData(file_name)
                data.title = title
                data.date = data_date
                data.time = data_time
                data.reactor = sheet[i, 0].plaintext()
                data.label = sheet[i, 1].plaintext()[:-2]
                data.profile = sheet[i, 2].plaintext()
                # Get titles and units of measurements
                signal = data.Signal()
                signal.name = 'OD'
                signal.unit = ''
                data.signals.append(signal)

                data.xaxis.name = 'Time'
                data.xaxis.unit = 's'
                for j in range(5, col):
                    data.xaxis.append(times[j-5])
                    data.signals[0].append(float(sheet[i, j].value))

                if data.label not in spectrostar_data:
                    spectrostar_data[data.label] = []
                spectrostar_data[data.label].append(data)

    # Check data has been read in
    if(len(spectrostar_data.keys()) == 0):
        raise RuntimeError('Issue processing data:\n'
                           'Did not read in any data')

    # If everything is successful return the data
    return spectrostar_data
