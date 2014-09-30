An ADB device
=============
::

    commands = {"iw":IwCommand,
                'wl':WlCommand,
                'wifi':WifiCommand,
                'wpa_cli':WpaCliCommand}
    
    



The ADB Device
--------------

.. uml::

   BaseDevice <|-- AdbDevice

.. module:: apetools.devices.adbdevice
.. autosummary::
   :toctree: api

   AdbDevice
   AdbDevice.channel
   AdbDevice.rssi
   AdbDevice.bitrate
   AdbDevice.noise
   AdbDevice.ssid
   AdbDevice.bssid
   AdbDevice.mac_address
   AdbDevice.wifi_commands
   AdbDevice.wifi_querier
   AdbDevice.netcfg
   AdbDevice.wifi_control
   AdbDevice.wake_screen
   AdbDevice.display
   AdbDevice.disable_wifi
   AdbDevice.enable_wifi
   AdbDevice.get_wifi_info
   AdbDevice.log
   AdbDevice.root
   AdbDevice.address
   


The ADB WiFi Command Finder
---------------------------

.. uml::

   BaseClass <|-- AdbWifiCommandFinder

.. autosummary::
   :toctree: api

   AdbWifiCommandFinder
   AdbWifiCommandFinder.__call__

::

    # a tuple of commands to try
    wifi_commands = ("wifi wl iw wpa_cli".split())
    
    

