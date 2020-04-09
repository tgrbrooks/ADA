# Local import
from reader.algemdata import AlgemData

# Standard imports
import os

def read_text_file(file_name):
    with open(file_name, 'r', errors='replace') as f:
        lines = f.readlines()
        algem_data = AlgemData(file_name, lines)
        return algem_data
    return
