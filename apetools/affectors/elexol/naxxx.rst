The NAXXX
=========

A module to run the NAXXX Network Power Supply.



.. uml::
   
   AffectorError <|-- NaxxxError

.. module:: apetools.affectors.elexol.naxxx
.. autosummary::
   :toctree: api

   NaxxxError


.. uml::

   BaseClass <|-- Naxxxx

.. autosummary::
   :toctree: api

   Naxxx
   Naxxx.naxxx
   Naxxx._clean_outlets
   Naxxx.run
   Naxxx.__call__

