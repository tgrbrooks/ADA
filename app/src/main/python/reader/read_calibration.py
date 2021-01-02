# Standard imports
import os
import csv
import numpy as np

# Local import
from reader.calibration_data import CalibrationData


# Loop over ADA csv files and read them in
def read_calibration(file_name):
    calibration_data = CalibrationData(file_name)
    with open(file_name, 'r', errors='ignore') as f:
        reader = csv.reader(f, delimiter=',')
        # Skip the header
        next(reader)
        for row in reader:
            calibration_data.true.append(float(row[0]))
            calibration_data.measured.append(float(row[1]))
    return calibration_data
