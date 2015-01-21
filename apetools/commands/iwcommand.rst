IW Command
==========

A module to query the device for interface information.



The Iw Command
--------------

.. uml::

   BaseClass <|-- IwCommand

.. module:: apetools.commands.iwcommand
.. autosummary::
   :toctree: api

   IwCommand
   IwCommand.operating_system
   IwCommand.interface
   IwCommand.ssid
   IwCommand.channel
   IwCommand.rssi
   IwCommand.mac_address
   IwCommand._match
   IwCommand.__str__

