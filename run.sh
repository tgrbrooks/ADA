#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd $DIR
git pull

if [ ! -d "venv" ]; then
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
else
  source venv/bin/activate
fi

pip3 install --upgrade -e .
python3 ada/main.py
deactivate
popd
