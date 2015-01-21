WL Command
==========

A module to query the device for interface information.


WL Command
----------

.. uml::

   BaseWifiCommand <|-- WlCommand

.. module:: apetools.commands.wlcommand
.. autosummary::
   :toctree: api

   WlCommand
   WlCommand.interface
   WlCommand.rssi
   WlCommand.mac_address
   WlCommand.bitrate
   WlCommand.ssid
   WlCommand.noise
   WlCommand.channel
   WlCommand.bssid
   WlCommand.get
   WlCommand._match
   WlCommand.__str__

