import numpy as np


# Class to store algae data
class CalibrationData():

    def __init__(self, file_name):
        self.name = file_name
        self.label = (file_name.split('/')[-1]).split('.')[0]
        # Data information
        self.true = []
        self.measured = []

    def calibrate_od(self, ods):
        cds = []
        measured = self.measured
        true = self.true
        if measured[0] > measured[-1]:
            measured = list(reversed(self.measured))
            true = list(reversed(self.true))
        size = len(measured)
        if size < 2 or size != len(true):
            return ods

        low_p = np.polyfit([measured[0], measured[1]], [true[0], true[1]], 1)
        low_fit = np.poly1d(low_p)
        high_p = np.polyfit([measured[size-2], measured[size-1]], [true[size-2], true[size-1]], 1)
        high_fit = np.poly1d(high_p)
        for od in ods:
            cd = 0
            if od < measured[0]:
                # Project out from first point
                cd = low_fit(od)
            elif od > measured[-1]:
                # Project out from last point
                cd = high_fit(od)
            else:
                cd = np.interp(od, measured, true)
            cds.append(cd)
        return cds
