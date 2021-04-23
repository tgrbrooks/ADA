# Local includes
from data.algae_data import AlgaeData


# Class to store data files in
class DataHolder():

    def __init__(self):
        self.empty = True
        self.data_files = []
        self.replicate_files = []

    def clear(self):
        self.empty = True
        self.data_files = []
        self.replicate_files = []

    def delete_data(self, i):
        if i >= 0 and i < len(self.data_files):
            self.data_files.pop(i)
            self.replicate_files.pop(i)
        if len(self.data_files) == 0:
            self.empty = True

    def add_data(self, data):
        self.data_files.append(data)
        self.replicate_files.append([data])
        self.empty = False

    def add_replicate(self, data, index):
        if index >= 0 and index < len(self.replicate_files):
            self.replicate_files[index].append(data)

    def delete_replicate(self, index, rindex):
        if index >= 0 and index < len(self.replicate_files):
            if rindex >= 0 and rindex < len(self.replicate_files[index]):
                self.replicate_files[index].pop(rindex)

    def get_profiles(self):
        profiles = []
        for data in self.data_files:
            profiles.append(data.profile)
        return profiles

    def get_reactors(self):
        reactors = []
        for data in self.data_files:
            reactors.append(data.reactor)
        return reactors
