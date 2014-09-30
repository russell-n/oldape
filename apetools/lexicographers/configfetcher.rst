Config Fetcher
==============

A module to fetch config files.

The ConfigFetcher copies the config file to the current working directory.

It was built to be used to pick config files from a folder of different files, but if it gets no parameters, it will load whatever is set as the DEFAULTS in the `config.constants` module.



.. uml::

   BaseClass <|-- ConfigFetcher

.. module:: apetools.lexicographers.configfetcher
.. autosummary::
   :toctree: api

   ConfigFetcher
   ConfigFetcher.folder_path
   ConfigFetcher.config_folder_path
   ConfigFetcher.config_names
   ConfigFetcher.fetch_config

