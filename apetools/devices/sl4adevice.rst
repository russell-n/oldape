SL4A Device
===========

An SL4a Device provides the common device-methods using an SL4a connection.



.. uml::

   BaseDevice <|-- SL4ADevice
   SL4ADevice o- SL4AConnection

.. module:: apetools.devices.sl4adevice
.. autosummary::
   :toctree: api

   SL4ADevice
   SL4ADevice.connection
   SL4Device.wake_screen
   SL4ADevice.display
   SL4ADevice.disable_wifi
   SL4ADevice.enable_wifi
   SL4ADevice.log
   SL4ADevice.get_wifi_info

