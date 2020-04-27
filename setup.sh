#!/bin/bash

# Check for requirements, give warnings if not present
# Set up virtual environment?

# Get directory of this script
LOCAL=`dirname "${BASH_SOURCE[0]}"`
CURRENT=`pwd`
DIR="${CURRENT}/${LOCAL}"
#echo $DIR
export PYTHONPATH="${DIR}/src:${PYTHONPATH}"
