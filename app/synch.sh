#!/bin/bash

mkdir -p src/main/python/gui
mkdir -p src/main/python/plotter
mkdir -p src/main/python/reader

cp main.py src/main/python/.
cp ../src/gui/*.py src/main/python/gui/.
cp ../src/plotter/*.py src/main/python/plotter/.
cp ../src/reader/*.py src/main/python/reader/.

rm src/main/python/gui/__init__.py
rm src/main/python/plotter/__init__.py
rm src/main/python/reader/__init__.py

sed -i '' "s/src\.//g" src/main/python/gui/*.py
sed -i '' "s/src\.//g" src/main/python/plotter/*.py
sed -i '' "s/src\.//g" src/main/python/reader/*.py

cp -r ../images/icons/* src/main/icons/.
