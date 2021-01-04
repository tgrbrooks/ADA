.. installation:

Installation
============

From an installer
-----------------
Installers for Windows 10 and MacOS are available on `Github <https://github.com/tgrbrooks/ADA/releases>`_.

MacOS
'''''

Download the file called ``ADA.dmg``, and click open with DiskImageMounter.

Drag the icon into your applications folder.

When you open it for the first time you will get a warning telling you it's from an unidentified developer, go to System Preferences -> Security & Privacy
and there should be a message at the bottom of the general tab that will let you open the app.

The installer was made with MacOS Mojave, earlier or later versions may or may not work. If you find any issues please open up an `issue <https://github.com/tgrbrooks/ADA/issues>`_.

Windows 10
''''''''''

There is also an installer available for Windows 10 on DropBox, the file is called ``ADASetup.exe``. 

Simply open the file and follow the installation instructions.

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
   source run.sh

Detailed Instructions
'''''''''''''''''''''

Create a virtual environment in the ADA directory for installing the dependencies

.. code-block:: bash

  python3 -m venv venv
  source venv/bin/activate

Install the dependencies

.. code-block:: bash

  pip3 install -r requirements.txt

Install the Algae Plotter app

.. code-block:: bash

   pip3 install --upgrade -e .

Run the program

.. code-block:: bash

  python3 ada/main.py

When you open a new terminal you will need to activate the virtual environment again

.. code-block:: bash

   source venv/bin/activate

You can check for, download and install updates from GitHub with

.. code-block:: bash

   git pull
   pip3 install --upgrade -e .
