.. installation:

Installation
============

From a DMG Image
----------------
An installer for MacOS is available on `DropBox <https://www.dropbox.com/sh/pa48a3jmwdhks1o/AACyNKSP8AvDUff5IjPBasApa?dl=0>`_.
Other operating systems can be supported upon request

From GitHub
-----------

Dependencies
''''''''''''
These software packages should be installed in the order presented before you attempt to use the Algae Plotter.

 * `Python 3.6.X <https://www.python.org/>`_
 * PyQt5
 * Matplotlib

Instructions
''''''''''''

Clone the repository

.. code-block:: bash

  git clone https://github.com/tgrbrooks/AlgaePlotter.git

Check your version of python

.. code-block:: bash

  python3 --version

If you don't have python 3.6 installed then `download it <https://docs.python-guide.org/starting/install3/osx/>`_

Create a virtual environment in the AlgaePlotter directory for installing the dependencies

.. code-block:: bash

  python3 -m venv venv
  source venv/bin/activate

Install the dependencies

.. code-block:: bash

  pip install matplotlib PyQt5==5.9.2

Run the program

.. code-block:: bash

  python3 src/main.py
