Win RSSI
========

A command to interpret the output of Miller's rssi puller.


Win Rssi Error
--------------

.. uml::

   CommandError <|-- WinRssiError

.. module:: apetools.commands.winrssi
.. autosummary::
   :toctree: api

   WinRssiError



Win RSSI
--------

.. uml::

   BaseClass <|-- WinRssi

.. autosummary::
   :toctree: api

   WinRssi
   WinRssi.expression
   WinRssi.validate
   WinRssi.__call__

