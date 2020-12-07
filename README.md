[![Build Status](https://travis-ci.org/tgrbrooks/ADA.svg?branch=master)](https://travis-ci.org/tgrbrooks/AlgaePlotter)

[![Documentation Status](https://readthedocs.org/projects/algaeplotter/badge/?version=latest)](https://algaeplotter.readthedocs.io/en/latest/?badge=latest)

![Logo](/images/logo.png)

An interactive PyQt5 based plotting package for algae growth curves.

# Installation

## Just the application

Installers for MacOS are available on [Dropbox](https://www.dropbox.com/sh/pa48a3jmwdhks1o/AACyNKSP8AvDUff5IjPBasApa?dl=0).

Other operating systems can be supported upon request.

## Installing the code

Dependencies:
* Python 3.6 (other version may have unexpected behaviour)
* PyQt5
* Matplotlib

### Detailed instructions for MacOS

Clone the repository

```bash
git clone https://github.com/tgrbrooks/AlgaePlotter.git
```

Check your version of python

```bash
python3 --version
```

If you don't have python 3.6 installed then [download it](https://docs.python-guide.org/starting/install3/osx/)

Create a virtual environment in the AlgaePlotter directory for installing the dependencies

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies

```bash
pip install matplotlib PyQt5==5.9.2
```

Run the program

```bash
python3 src/main.py
```

# Usage

This is a GUI based application, all configuration is through the user interface.

There are two tabs, a plotting tab and an options tab

## Plotting

![Plotting Screen](/images/plotting_screen.png)

### Growth curve data

Algal growth curve data can be imported using the `Add Data` button, this will open a file browser to allow you to select the data.

Currently only text files from the Algem photobioreactor are supported, contact me if you need other file types added.
The selected files will be displayed in the box below, files can be remove by clicking their names.

The files will be plotted in the order that they are loaded.

### Growth condition data

It is possible to display growth condition data (temperature, pH, light, etc) on the right hand y axis.

Data is loaded and removed in the same way as the growth curve data.

### Quick access functions

* **`Save`**: save the plot as an image file, the file name can be configured in the options tab.
* **`Export`**: export the data files to comma separated variable (`.csv`) files.
* **`Measure`**: interactively measure the growth rate gradient. A cursor will appear that will allow you to select two points on the growth curves to measure the gradient between them.
* **`Grid`**: toggle the grid on and off.

## Options

![Options Screen](/images/options_screen.png)

### Axis configuration

Choose the plotting variable, axis label and axis range for the x (time), y (usually some measure of growth/algae density) and y2 (growth conditions).

Leaving text boxes blank will use the variable and unit names from the data files.

### Data configuration

* **`Smooth data`**: apply Savitzky-Golay [1,2,3] smoothing to noisy data.
* **`Align`**: where there is an offset in the start times between the data files they can be aligned at time 0 by subtracting the first measured time from all subsequent times.

### Legend configuration

Toggle the legend on and off.

The default legend titles are taken from the file names, they can be modified by selecting them in the drop-down menu, changing the text, and pressing return.

### Style configuration

The default matplotlib plotting [style](https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html), font family, font size and line width can be modified.

[1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of Data by Simplified Least Squares Procedures. Analytical Chemistry, 1964, 36 (8), pp 1627-1639.

[2] Numerical Recipes 3rd Edition: The Art of Scientific Computing W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery Cambridge University Press ISBN-13: 9780521880688

[3] SciPy Cookbook (http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay)
