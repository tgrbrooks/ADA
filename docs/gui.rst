.. _gui:

The GUI
=======

Importing Data
--------------

Allowed Formats
'''''''''''''''
Currently the only accepted input format is the plain text files produced by the Algem photobioreactor.

There are plans to support the csv format returned by the newer version of the reactor and a more general csv file format.

Growth Data
'''''''''''
Growth data can be imported with the ``Add Data`` button.
This will open up a file browser that will allow you to find the ``.txt`` files with your data.

Select the file and hit open and you should be able to see it in the box below the ``Add Data`` button.

The ``del`` button next to it will remove the data (just from the software, it won't delete the original file!).

The ``add`` button allows you to add replicate data, any files added this way will be averaged with the top level files.

To plot separate data just keep hitting the ``Add Data`` button.

Conditions Data
'''''''''''''''
It is often the case that the condition data (temperature, pH, etc) comes in a separate text file.

If you want to plot the condition data alongside the growth data it can be added with the ``Add Condition Data``.
The condition data will be plotted on the same X axis but with a Y axis on the right.

Plotting
--------
To plot the data with the default configuration just hit the ``Plot!`` button.

If you want to change how the plot looks, head over to the :ref:`options` tab.

.. note::
   You can change the individual line colours and styles by clicking on the curves.

Saving
''''''
To save the plot just hit the ``Save`` button, this will open up a file browser to let you choose a file name and location.

Exporting Data
--------------
You can export the loaded growth data to csv format for easy viewing in your favourite spreadsheet software by hitting the ``Export`` button.

.. warning::
   Header information is not saved and replicate data not yet supported.

Making Measurements
-------------------

On the Plot
'''''''''''
You can measure the growth rates (gradients) on the plot by pressing the ``Measure`` button.

This will let you click between any two points on any of the plotted curves and display the gradient on the plot.

To a Table
''''''''''
If you've got a lot of growth curves and you don't want to measure everything manually you can configure standard measurements to be applied to all curves automatically with the ``To Table`` button.

This will open up a new window that contains a dropdown menu with the available measurements/info, add a row to the table by selecting it in the dropdown menu and hit ``Add Row``

This will show the row in the list below and allow you to configure it.

The available measurements/info are:

* ``profile``: The profile name from the header information.
* ``reactor``: The name of the reactor the sample was grown in.
* ``gradient``: The gradient of Y data (selected with dropdown) between two times (entered in the text boxes).
* ``time to``: The time taken for the the Y data (selected with dropdown) to reach a certain point (entered in text box).
* ``average of condition``: The average of the condition data (associated with the growth data by comparing the reactor ID and start date/time) between two times (entered in the text boxes).
* ``condition at time``: The value of the condition data (selected with dropdown) at a certain time (entered in text box).

Measurements can be added as many times as you want if you want to measure multiple conditions.

The ``Create Table`` button will open up a file browser to let you chose a file name and location, the table will be saved in csv format.

