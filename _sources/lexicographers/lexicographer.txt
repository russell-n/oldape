Lexicographer
=============

A module to hold a translator of configurations to configuration map.

The Lexicographers used to check configurations and do conversions, but more of that has been pushed to the builders and ConfigurationMap



.. uml::

   BaseClass <|-- Lexicographer

.. module:: apetools.lexicographers.lexicographer
.. autosummary::
   :toctree: api

   Lexicographer
   Lexicographer.filenames
   Lexicographer.finder
   Lexicographer.__iter__

