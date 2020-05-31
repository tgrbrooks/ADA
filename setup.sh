#!/bin/bash

python3 -m venv venv
source venv/bin/activate

pip install matplotlib PyQt5==5.9.2
pip install .
