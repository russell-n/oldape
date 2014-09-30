Linux Device
============

A configurer and queryier for linux devices.



.. uml::

   BaseDevice <|-- LinuxDevice

.. module:: apetools.devices.linuxdevice
.. autosummary::
   :toctree: api

   LinuxDevice
   LinuxDevice.ifconfig
   LinuxDevice.wifi_query
   LinuxDevice.address
   LinuxDevice.mac_address
   LinuxDevice.bssid
   LinuxDevice.ssid
   LinuxDevice.noise
   LinuxDevice.channel
   LinuxDevice.rssi
   LinuxDevice.bitrate
   LinuxDevice.disable_wifi
   LinuxDevice.enable_wifi
   LinuxDevice.log

