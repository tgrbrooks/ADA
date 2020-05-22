.. _options:

Options
=======

Axis
----
The axis configuration menu gives you a configuration matrix for all three axes (X = time, Y = growth, Y2 = condition value)

``Variable``
''''''''''''
Dropdown menu that will let you choose what variable to plot.

The variables are automatically loaded with the data for the Y and Y2 axes.

For the time axis the menu will let you choose the time units, changes to this will propagate to all other actions (e.g. measuring the gradient),

``Label name``
''''''''''''''
Overwrite the axis label by entering text into these boxes.

If left blank the label will be read from the header of the growth/condition file.

``Unit name``
'''''''''''''
Overwrite the axis label unit by entering text into these boxes.

If left blank the label will be read from the header of the growth/condition file.

.. note::
   You can remove the unit all together by entering ``none`` in the box.

``Range min/max``
'''''''''''''''''
Set the minimum and maximum point to plot for each axis.

Data
----
The data configuration menu provides options for operations that can applied to the growth/condition data.

``Smooth data``
'''''''''''''''
Apply `Savistky-Golay <http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay>`_ filter to smooth noisy data.

``Align at time = 0``
'''''''''''''''''''''
If something has gone wrong with your data and the time measurement has some offset from 0 you can use this to make sure all growth curves start at time = 0.

``Align at Y =``
'''''''''''''''''
To make comparisons of growth rates from a certain growth point you can align curves at a given point on the Y axis.

.. warning::
   Data can be noisy and may cross the same Y point multiple times, the first time that the curve crosses a point will be used for alignment

.. note::
   The time axis can (and probably will) extend into negative values as it now corresponds to time since Y = value

``Data outliers``
'''''''''''''''''
There are several options for removing erroneous points (points where there is a measurement error, not points that don't fit your theory!):

* ``Remove above/below``: remove any points above or below a certain Y value.
* ``Auto remove``: Attempt to automatically remove any points where there seems to be an obvious jump from the points before and after.

``Downsample readings``
'''''''''''''''''''''''
If the condition data file is very large, you have the option to downsample when reading in the file to reduce loading times.

The downsampling factor can be entered in to the box.

e.g. A factor of 10 means that only 1 in 10 data points will be read in.

``Time average``
''''''''''''''''
For noisy condition data you can also average over a time window entered into the text box.

This will calculate the mean and standard deviation over a given time window.

The standard deviation will be shown on the plot as an error bar, this can be changed to the standard error on the mean in the ``Stats`` configuration menu.

Legend
------
The legend configuration menu gives you a configuration matrix for the growth and condition legends which can be toggles on/off with the ``On`` checkbox.

The legend positions can be changed by dragging them in the plot.

``Titles``
''''''''''
The dropdown menu shows the titles of each curve which can be edited by selecting the title, changing the text and hitting the enter button on your keybourd.

``Header``
''''''''''
A title for each legend, so you could label one 'Growth' and one 'pH' for example.

``Extra info``
''''''''''''''
Show extra information retrieved from the header file in the legend.

By default, this information will be shown in brackets after the label title, to only show the extra information without the brackets use the ``Only extra info`` checkbox.

Style
-----
Modify the cosmetics of the plot.

``Style``
'''''''''
Change the default colour scheme of the plot. The available options are:
* ``default``: the default matplotlib style.
* ``grayscale``: a colour scheme appropriate for black and white printing
* ``colour blind``: a scheme easily differentiated by people with colour blindness
* ``pastel``
* ``deep``

``Font style``
''''''''''''''
Change the font style to one of the available types.

``Title/Legend/Label size``
'''''''''''''''''''''''''''
The title (plot heading and axis), legend and label (numbers on axes) font sizes can be configured separately.

.. note::
   The plot will automatically reshape itself to fit in the window when the font sizes are changed.

``Line width``
''''''''''''''
Change the width of the curves.

``Condition axis colour``
'''''''''''''''''''''''''
Change the colour of the condition Y axis.

``Grid``
Toggle a grid on/off on the plot.

Stats
-----
Configuration for any statistical things.

``Standard error``
''''''''''''''''''
Show the standard deviation (unticked) or the standard error on the mean (ticked) in the error bars.
