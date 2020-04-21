# Local import
from reader.algemdata import AlgemData

# Standard imports
import os

# Loop over text files and read them in
def read_text_file(file_name, downsample=-1):
    with open(file_name, 'r', errors='ignore') as f:
        try:
            lines = f.readlines()
            algem_data = AlgemData(file_name, lines, downsample)
            return algem_data
        except Exception as e:
            raise RuntimeError('Error reading file '+file_name+'\n'+str(e))
    return
