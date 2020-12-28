.. _gui:

The GUI
=======

Importing Data
--------------

Allowed Formats
'''''''''''''''
Currently the accepted input formats are:
- Algem Pro text files
- Algem HT-24 CSV (comma separated variable) files
- Industrial Plankton (IP) T-Iso CSV files
- Photon Systems Instruments (PSI) photobioreactor ODS files
- ADA export format/user input format CSV files

It should be possible to export files of this format from the software that is supplied with each of these bioreactors.

If you have a different bioreactor that is not currently supported please feel free to contact me and I'll try my best to add it.

Growth Data
'''''''''''
Growth data can be imported with the ``Add Data`` button.

This will open up a window that will allow you to select the type of file to upload and include any additional files (such as condition files).

``Select data file(s)`` will open up a file browser where you can select one or more files of the same type.

.. warning::
   It is not possible to upload different types of files at the same time, you must ``Add Data`` for each file type you want to upload.

After selecting the files, more options will appear depending on the file type:

Algem Pro
    Growth condition files are stored separately and can be added.
    There is also an option to downsample the condition data, this will read in every X measurements. If the frequency of the condition measurements is much greater than the frequency of growth measurements it can take a long time to load the file without downsampling.

Algem HT-24
    A growth conditions file can be added.
    Condition downsampling can be specified.
    A details file can be added, this contains replicate and other information.
    The ``Merge details`` button will use the replicate information from the details file to average replicate measurements together.

Industrial Plankton (IP T-Iso)
    The condition data is contained in the file and will be automatically loaded

Photon Systems Instruments (PSI)
    The condition data is contained in the file and will be automatically loaded

ADA
    Other file types can be exported to this type which contains both growth and conditions data.
    It is also possible to download a template file from the ``Data`` tab to upload custom data. Just open up the template file in your favourite spreadsheet software and add the information to the indicated locations and then load in the data with the ``ADA`` option.

Hit the ``Load`` button to upload the files, they should appear in the box below the ``Add Data`` button and the condition data will appear in the box below that.

The ``x`` button next to it will remove the data (just from the software, it won't delete the original file!).

The ``+`` button allows you to add replicate data, any files added this way will be averaged with the top level files.

To plot more data just keep hitting the ``Add Data`` button.

Plotting
--------
To plot the data with the default configuration just hit the ``Plot!`` button.

If you want to change how the plot looks, head over to the :ref:`options` tabs.

.. note::
   You can change the individual line colours and styles by clicking on the curves.

Saving
''''''
To save the plot just hit the ``Save`` button, this will open up a file browser to let you choose a file name and location.

.. warning::
   You cannot create new folders with the file browser, this will cause an error.

Exporting Data
--------------
You can export the loaded growth data to csv format for easy viewing in your favourite spreadsheet software by hitting the ``Export`` button.

.. warning::
   Replicate data is not yet supported, the top level data file will be exported and any replicates will be ignored.

Making Measurements
-------------------

On the Plot
'''''''''''
You can measure the growth rates (gradients) on the plot by pressing the ``Measure`` button.

This will let you click between any two points on any of the plotted curves and display the gradient on the plot.

Fitting
'''''''
You can fit curves to the growth data with the ``Fit`` button.

The available fits are (:math:`y` = growth data, :math:`x` = time data):
- Flat line :math:`y = p_{0}`
- Linear :math:`y = p_{1}x + p_{0}`
- Quadratic :math:`y = p_{2}x^2 + p_{1}x + p_{0}`
- Exponential :math:`y = p_{0}e^{p_{1}x}`

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

The ``Create Table`` button will show the table in the ``Table`` tab.

The ``Save Table`` button will open up a file browser to let you chose a file name and location, the table will be saved in csv format.

