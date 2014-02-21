Busybox wget
============
.. _busybox-wget:
A wget hack for the busybox wget command (to simulate file-transfers over the internet).

.. currentmodule:: apetools.commands.busyboxwget



The Busybox Wget Data
---------------------

This is what will be returned by the wget. The idea I am converging on is that `commands` get data and return it, `tools` and `sessions` are the ones that know what to do with it (like save it).

.. uml::

   BusyboxWgetData : elapsed
   BusyboxWgetData : error
   BusyboxWgetData : percentage
   BusyboxWgetData : kbits

.. csv-table:: BusyboxWgetData Fields
   :header: Attribute, Meaning

   elapsed,Seconds from `wget` call until the output is complete
   error,Error message found in the output (if any)
   percentage, Percentage of transfer that successfully finished
   kbits, kbits successfully transferred
   


The Busybox Enum
----------------

A holder of constants for users of this module.

.. autosummary::
   :toctree: api

   BusyboxEnum.destination


   

The Busybox Wget Command
------------------------

.. uml::

   BusyboxWget -|> BaseClass

.. autosummary::
   :toctree: api

   BusyboxWget
   BusyboxWget.arguments
   BusyboxWget.expression
   BusyboxWget.run
   BusyboxWget.__call__






