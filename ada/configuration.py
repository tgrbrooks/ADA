import os
import json

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as myfile:
    data=myfile.read()
    
config = json.loads(data)