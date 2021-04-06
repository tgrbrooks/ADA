.. _api:

API
===

Directory structure
-------------------
- ``configuration.py``: Initial plotting/analysis configuration values

- ``logger.py``: Logging configuration

- ``styles.py``: Contains style sheets for components

- ``ada``: Source code

    * ``gui``: Graphical windows

    * ``data``: Data storage and processing classes/functions

    * ``plotter``: Matplotlib canvases and related classes

    * ``reader``: File parsing functions

    * ``components``: Wrappers around PyQt widgets adding custom styles and functionalities

- ``docs``: Read-the-docs documentation

- ``images``: Logos, icons and other images

- ``test``: unit tests and example data files

    * ``files``

        - ``Algem-HT24``: Test files for the Algem HT24 bioreactor

        - ``Algem-Pro``: Test files for the Algem Pro bioreactor

        - ``IP``: Test files for the Industrial Phytoplankton bioreactor

        - ``PSI``: Test files for the Photon Systems Instruments bioreactor

        - ``ADA``: Test files in the ADA file format
