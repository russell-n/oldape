Windows Device
==============

A Windows Device controller and queryer.



.. uml::

   BaseDevice <|-- WindowsDevice
   WindowsDevice o- WindowsSSIDConnect
   WindowsDevice o- Ipconfig
   WindowsDevice o- WmicWin32NetworkAdapter
   WindowsDevice o- WinRssi
   WindowsDevice o- NetshWlan
   WindowsDevice o- SSHConnection

.. module:: apetools.devices.windowsdevice
.. autosummary::
   :toctree: api

   WindowsDevice
   WindowsDevice.ssid_connect
   WindowsDevice.ipconfig
   WindowsDevice.wifi_control
   WindowsDevice.rssi_query
   WindowsDevice.rssi
   WindowsDevice.wifi_info
   WindowsDevice.wify_query
   WindowsDevice.address
   WindowsDevice.enable_wifi
   WindowsDevice.disable_wifi
   WindowsDevice.display
   WindowsDevice.log
   WindowsDevice.wake_screen
   WindowsDevice.connect
   WindowsDevice.disconnect

