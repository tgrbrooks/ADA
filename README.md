[![Build Status](https://travis-ci.org/tgrbrooks/ADA.svg?branch=master)](https://travis-ci.org/tgrbrooks/ADA)

[![Documentation Status](https://readthedocs.org/projects/algaeplotter/badge/?version=latest)](https://algaeplotter.readthedocs.io/en/latest/?badge=latest)

![Logo](/images/logo_v2.png)

An PyQt5 based plotting and analysis package for algae growth curves.

# Installation

## Just the application

* MacOS [installer](https://www.dropbox.com/sh/pa48a3jmwdhks1o/AACyNKSP8AvDUff5IjPBasApa?dl=0&preview=Algae+Plotter.dmg) (via Dropbox)
  * Tested on Mojave, should still work on Catalina.
* Windows 10 [installer](https://www.dropbox.com/sh/pa48a3jmwdhks1o/AACyNKSP8AvDUff5IjPBasApa?dl=0&preview=Algae+PlotterSetup.exe) (via Dropbox)

Other operating systems can be supported upon request.

## Installing the code

Dependencies:
* Python 3.6 (other version may have unexpected behaviour)
* PyQt5
* Other required python libraries in the `requirements.txt`

### Detailed instructions for MacOS

Clone the repository

```bash
git clone https://github.com/tgrbrooks/ADA.git
```

Check your version of python

```bash
python3 --version
```

If you don't have python 3.6 installed then [download it](https://docs.python-guide.org/starting/install3/osx/)

The script `run.sh` can be used to finish the setup and run the program, the individual steps are:

* Create a virtual environment in the AlgaePlotter directory for installing the dependencies

```bash
python3 -m venv venv
source venv/bin/activate
```

* Install the dependencies

```bash
pip3 install -r requirements.txt
```

* Install ADA in edit mode

```bash
pip3 install --upgrade -e .
```

* Run the program

```bash
python3 ada/main.py
```

# Usage overview

There is in-depth documentation on the usage and available features available [here](https://algaeplotter.readthedocs.io/en/latest/).

The starting screen contains the plot, data input and commonly used features.
The tabs at the top of the screen contain more plotting and analysis options.

## Plotting

![Plotting Screen](/images/plotting_screen.png)

### Growth curve data

Algal growth curve data can be imported using the `Add Data` button, this will open a new window to allow you to select the data.

The currently supported bioreactor data types are:
* Algem Pro text files
* Algem HT-24 CSV (comma separated variable) files
* Industrial Plankton (IP) T-Iso CSV files
* Photon Systems Instruments (PSI) photobioreactor ODS files
* ADA export format/user input format CSV files

It should be possible to export files of this format from the software that is supplied with each of these bioreactors.

If you have a different bioreactor that is not currently supported please feel free to contact me and I'll try my best to add it.

The imported files will be displayed in the box below the `Add Data` button, files can be removed by clicking the red X and replicates can be added by clicking the green +.

### Growth condition data

It is possible to display growth condition data (temperature, pH, light, etc) on the right hand y axis.

Some bioreactors (IP and PSI) include the condition data in their files, others come as separate files that can be uploaded at the same time as the growth data files.

Condition data can be removed by clicking the red X next to the name.

### Plot

Hit the `Plot!` button to display the currently loaded growth and condition data.

The curves can be clicked on to chage their style.

### Calibration curve

A calibration curve (measured OD to true OD conversion) can be loaded and used to plot the calibrated density (CD).

### Quick access functions

* **`Save`**: Save the currently displayed plot as a png image.
* **`Export`**: Export the data files to ADA format CSV files.
* **`Measure`**: Interactively measure the growth rate gradient. A cursor will appear that will allow you to select two points on the growth curves to measure the gradient between them.
* **`Fit`**: Fit the displayed curves with a selection of predefined functions (if a function you need isn't present, let me know).
* **`To Table`**: Output common measurements to a table (contact me if you have any more common measurements you would like included).

## Options tabs

There are many configuration options available in the different options tabs, a summary is provided here.

As always, if there are missing features you need, open an issue or get in contact some other way.

### Axes

* Set a plot title.
* Choose plotting variables.
* Modify the axis labels and unit names.
* Set the axis ranges.

The X axis is always time, Y is usually some measure of growth such as optical density (OD) and Y2 is for growth conditions.

Leaving text boxes blank will use the variable and unit names from the data files, units can be removed by entering "none".

### Data

* Apply Savitzky-Golay smoothing to noisy data.
* Align growth curves to all start from time = 0, or at a given point on the Y axis to facilitate comparisons.
* Some bioreactors include events in their data and there is an option to show these.
* Average condition data over a given time window.
* Remove measurement errors in growth data.

### Legend

* Toggle growth and condition legends on and off (they are also draggable on the plot).
* Modify legend headings and labels (select label from dropdown, modify it and press enter).
* Include extra information in the legends.

### Style

* Change the preset matplotlib plotting style.
* Change font sizes and styles.
* Change the plot line widths.
* Change the condition axis color.
* Toggle grid lines on and off.

### Stats

Currently the only available option here is switching between the standard error and standard deviation.
