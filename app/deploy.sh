#!/bin/bash

# Deactivate any currently running virtual env
if [ -x "$(command -v deactivate)" ]; then
  deactivate
fi

# Create a virtual environment if one doesn't already exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
else
  source venv/bin/activate
fi

# Checkout the most recent code and copy it over to the required directory structure for fbs
git pull
git merge master
source synch.sh

# Do the freezing and create the installer
fbs freeze
fbs installer
