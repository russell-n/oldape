The Dummy Device
================

A Dummy to stand in for a real device.



The Dummy Connection
--------------------

.. uml::

   BaseClass <|-- DummyConnection

.. module:: apetools.devices.dummydevice
.. autosummary::
   :toctree: api

   DummyConnection
   DummyConnection._procedure_call
   DummyConnection.__getattr__



The Dummy Device
----------------

.. uml::

   BaseClass <|-- DummyDevice

.. autosummary::
   :toctree: api

   DummyDevice
   DummyDevice.connection
   DummyDevice.address
   DummyDevice.mac_address
   DummyDevice.bssid
   DummyDevice.wifi_info
   DummyDevice.ssid
   DummyDevice.rssi
   DummyDevice.disable_wifi
   DummyDevice.enable_wifi
   DummyDevice.log
   
