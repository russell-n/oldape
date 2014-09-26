Netcfg
======

A module to query the device for interface information (using `netcfg`).


Netcfg Command
--------------

.. uml::

   BaseClass <|-- NetcfgCommand

.. module:: apetools.commands.netcfg
.. autosummary::
   :toctree: api

   NetcfgCommand
   NetcfgCommand.operating_system
   NetcfgCommand.ip_address
   NetcfgCommand.interface
   NetcfgCommand.mac_address
   NetcfgCommand.output
   NetcfgCommand._match
   NetcfgCommand.__str__

