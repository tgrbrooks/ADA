.. installation:

Installation
============

From an installer
-----------------
Installers for Windows 10 and MacOS are available on `DropBox <https://www.dropbox.com/sh/pa48a3jmwdhks1o/AACyNKSP8AvDUff5IjPBasApa?dl=0>`_.

MacOS
'''''

Download the file called ``Algae Plotter.dmg``, and click open with DiskImageMounter.

Drag the icon into your applications folder.

When you open it for the first time you will get a warning telling you it's from an unidentified developer, go to System Preferences -> Security & Privacy
and there should be a message at the bottom of the general tab that will let you open the app.

The installer was made with MacOS Mojave, earlier or later versions may or may not work. If you find any issues please open up an `issue <https://github.com/tgrbrooks/ADA/issues>`_.

Windows 10
''''''''''

There is also an installer available for Windows 10 on DropBox, the file is called ``Algae PlotterSetup.exe``. 

Just open the file and follow the installation instructions.

Other
'''''

Other operating systems can be supported upon request.

From GitHub
-----------

Dependencies
''''''''''''
These software packages should be installed in the order presented before you attempt to use the Algae Plotter.

 * `Python 3.6.X <https://www.python.org/>`_
 * PyQt5
 * Matplotlib

Check your version of python

.. code-block:: bash

  python3 --version

If you don't have python 3.6 installed then `download it <https://docs.python-guide.org/starting/install3/osx/>`_

Downloading the Source Code
'''''''''''''''''''''''''''

Clone the repository from GitHub

.. code-block:: bash

  git clone https://github.com/tgrbrooks/ADA.git

Quick Set-Up
''''''''''''

After downloading the source code you can install it with

.. code-block:: bash

   cd ADA
   source setup.sh

You only need to install it once, now you can run it with

.. code-block:: bash

   source run.sh

Detailed Instructions
'''''''''''''''''''''

Create a virtual environment in the AlgaePlotter directory for installing the dependencies

.. code-block:: bash

  python3 -m venv venv
  source venv/bin/activate

Install the dependencies

.. code-block:: bash

  pip install matplotlib PyQt5==5.9.2

Install the Algae Plotter app

.. code-block:: bash

   pip install .

Run the program

.. code-block:: bash

  python3 src/main.py

When you open a new terminal you will need to activate the virtual environment again

.. code-block:: bash

   source venv/bin/activate

You can check for, download and install updates from GitHub with

.. code-bloack:: bash

   git pull
   pip install .
