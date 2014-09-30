Base Device
===========

The Abstract Base for devices



BaseDevice Constants
--------------------

::

    class BaseDeviceEnum(object):
        __slots__ = ()
        tpc = "tpc"
        node = "node"
    # end class BaseDeviceEnum
    
    

::

    CSV_OUTPUT = "{ssid},{bssid},{channel},{ip},{mac},{rssi},{noise}\n"
    HUMAN_OUTPUT = """
    SSID        = {ssid}
    BSSID       = {bssid}
    Channel     = {channel}
    IP Address  = {ip}
    MAC Address = {mac}
    RSSI        = {rssi}
    Noise       = {noise}
    """
    
    



The Base Device
---------------

.. uml::

   BaseClass <|-- BaseDevice

.. module:: apetools.devices.basedevice
.. autosummary::
   :toctree: api

   BaseDevice
   BaseDevice.connection
   BaseDevice.bitrate
   BaseDevice.disable_wifi
   BaseDevice.enable_wifi
   BaseDevice.wifi_info
   BaseDevice.address
   BaseDevice.ssid
   BaseDevice.bssid
   BaseDevice.channel
   BaseDevice.noise
   BaseDevice.mac_address
   BaseDevice.rssi
   BaseDevice.log
   BaseDevice.poll
   BaseDevice.__str__     

