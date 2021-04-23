#!/bin/bash

mkdir -p src/main/python/gui
mkdir -p src/main/python/data
mkdir -p src/main/python/plotter
mkdir -p src/main/python/reader
mkdir -p src/main/python/components

cp main.py src/main/python/.
cp ../ada/type_functions.py src/main/python/.
cp ../ada/configuration.py src/main/python/.
cp ../ada/logger.py src/main/python/.
cp ../ada/styles.py src/main/python/.
cp ../ada/gui/*.py src/main/python/gui/.
cp ../ada/data/*.py src/main/python/data/.
cp ../ada/plotter/*.py src/main/python/plotter/.
cp ../ada/reader/*.py src/main/python/reader/.
cp ../ada/components/*.py src/main/python/components/.

rm src/main/python/gui/__init__.py
rm src/main/python/data/__init__.py
rm src/main/python/plotter/__init__.py
rm src/main/python/reader/__init__.py
rm src/main/python/components/__init__.py

sed -i '' "s/ada\.//g" src/main/python/gui/*.py
sed -i '' "s/ada\.//g" src/main/python/data/*.py
sed -i '' "s/ada\.//g" src/main/python/plotter/*.py
sed -i '' "s/ada\.//g" src/main/python/reader/*.py
sed -i '' "s/ada\.//g" src/main/python/components/*.py

cp -r ../images/icons/* src/main/icons/.
