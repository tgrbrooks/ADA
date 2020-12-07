#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd $DIR
git pull
source venv/bin/activate
pip install --upgrade .
python3 ada/main.py
deactivate
popd
