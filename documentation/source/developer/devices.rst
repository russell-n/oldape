Devices
=======

Devices provide a standard set of methods to talk to devices.


BaseDevice
----------

The abstract base class for the devices.

.. uml::

   BaseDevice: Connection connection
   BaseDevice: wake_screen()
   BaseDevice: display(StringType message)
   BaseDevice: disable_wifi()
   BaseDevice: enable_wifi()
   BaseDevice: StringType get_wifi_info()
   BaseDevice: log(StringType message)

SL4ADevice
----------

The SL4ADevice wraps and SL4AConnection

.. uml:: 

   SL4ADevice --|> BaseDevice
   SL4ADevice: SL4AConnection connection



