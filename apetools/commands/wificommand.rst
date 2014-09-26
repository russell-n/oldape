WiFi Command
============

A module to query the device for interface information.


Wifi Command Error
------------------

.. uml::

   CommandError <|-- WifiCommandError

.. module:: apetools.commands.wificommand
.. autosummary::
   :toctree: api

   WifiCommandError



Wifi Command
------------

.. uml:: 

   BaseWifiCommand <|-- WifiCommand

.. autosummary::
   :toctree: api

   WifiCommand
   WifiCommand.bitrate
   WifiCommand.interface
   WifiCommand.rssi
   WifiCommand.mac_address
   WifiCommand.ssid
   WifiCommand.noise
   WifiCommand.channel
   WifiCommand.bssid
   WifiCommand.get
   WifiCommand._match
   WifiCommand.__str__

