#!/bin/bash

TEST_DIR=`dirname "${BASH_SOURCE[0]}"`
CURRENT_DIR=`pwd`
cd $TEST_DIR
bash setup.sh
python3 -m unittest discover
cd $CURRENT_DIR
