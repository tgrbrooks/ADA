.. _contributing:

Contributing
============

Issues and New Features
-----------------------
If you find a bug or there are any features you would like added please open up an issue `here <https://github.com/tgrbrooks/ADA/issues>`_.

Adding to the Code
------------------
If you would like to contribute to the code yourself, drop me an email at tom.g.r.brooks@gmail.com and I will add you as a collaborator.

Contributions will operate on a pull request model:

Create a fork of the repository by hitting the ``Fork`` button in the top right.

Clone your fork, and set it to track the original repository

.. code:: bash

   git clone https://github.com/< username >/ADA.git
   cd ADA
   git remote add upstream https://github.com/tgrbrooks/ADA.git

Create a new branch to work on your feature

.. code:: bash

   git checkout -b < branch name >

Add your new code, committing and pushing to your branch as usual.

When finished, make sure all the changed files have been committed and pushed to your GitHub repository.

.. code:: bash

   git commit -a -m "Commit message"
   git push origin < branch name >

Find your branch on GitHub and click ``New pull request``. Add a message about the new feature and then I will review it and merge if appropriate.

Adding a new file type
----------------------

* Add a reader function in the ``reader`` directory. It should take a file name and return a collection of ``AlgaeData`` objects, depending on the contents of the file.
* Add a load function to ``load_window.py`` that calls the reader function and adds the ``AlgaeData`` object to the data manager.
* Add name of file to ``file_types`` and ``replicate_types`` in ``configuration.py``.
* Add the load function to the ``load`` method in ``load_window.py``, calling it if the ``file_type`` matches the name given in the configuration.

Adding a new model
------------------

* Create a model class that inherits from ``GrowthModel`` in ``models.py``.
* The inner ``__init__`` must contain:
   * A Latex equation string of the function.
   * A list of short descriptions of parameters for displaying options in the app.
   * A list of Latex parameter strings.
   * A list of the units of each parameter as a function of the X and Y units passed to the outer ``__init__``.
* Add the new model class to the ``get_model`` function.
* Add the model name to ``fit_options`` in ``configuration.py``

Adding a new table row type
---------------------------

* Create a function for calculating the measurement in ``DataManager``.
* Add the measurement type inputs to ``TableListItem``.
* In ``table_window.py`` call the data manager function in ``get_row_data`` and set the corresponding title in ``get_row_title``.
* Add the measurement name to ``table_row_options`` in ``configuration.py``.