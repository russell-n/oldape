Mac OS device
=============

A Mac OS device. Assumes that a symlink (or alias) has been setup so that you can call the 'airport' command (rather than passing in the full path).



.. uml::

   BaseDevice <|-- MacDevice
   MacDevice o- AirportCommand
   MacDevice o- Svc
   
.. module:: apetools.devices.macdevice
.. autosummary::
   :toctree: api

   MacDevice
   MacDevice.airport
   MacDevice.channel
   MacDevice.rssi
   MacDevice.bitrate
   MacDevice.noise
   MacDevice.ssid
   MacDevice.bssid
   MacDevice.mac_address
   MacDevice.wifi_control
   MacDevice.connection
   MacDevice.wake_screen
   MacDevice.display
   MacDevice.disable_wifi
   MacDevice.enable_wifi
   MacDevice.get_wifi_info
   MacDevice.log

