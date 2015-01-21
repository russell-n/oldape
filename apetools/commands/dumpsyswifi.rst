Dumpsys Wifi
============

A command to query the dumpsys about wifi information.



Dumpsys Wifi Enumerations
-------------------------

::

    class DumpsysWifiEnumerations(object):
        """
        An enumerations object
        """
        __slots__ = ()
        state = "wifistate"
        interface = "interface"
        ssid = "ssid"
        bssid = "bssid"
        mac_address = "mac_address"
        supplicant_state = "supplicant_state"
        rssi = "rssi"
        link_speed = "link_speed"
    # end class DumpsysWifiEnumerations
    
    



Dumpsys WiFi Expressions
------------------------

.. module:: apetools.commands.dumpsyswifi
.. autosummary:: 
   :toctree: api

   DumpsysWifiExpressions
   DumpsysWifiExpressions.state
   DumpsysWifiExpressions.interface
   DumpsysWifiExpressions.ssid
   DumpsysWifiExpressions.bssid
   DumpsysWifiExpressions.mac_address
   DumpsysWifiExpressions.supplicant_state
   DumpsysWifiExpressions.rssi
   DumpsysWifiExpressions.link_speed



DumpsysWifi
-----------

.. uml::

   BaseClass <|-- DumpsysWifi

.. module:: apetools.commands.dumpsyswifi
.. autosummary::
   :toctree: api

   DumpsysWifi
   DumpsysWifi.expressions
   DumpsysWifi.connection
   DumpsysWifi.state
   DumpsysWifi.interface
   DumpsysWifi.ssid
   DumpsysWifi.bssid
   DumpsysWifi.mac_address
   DumpsysWifi.supplicant_state
   DumpsysWifi.rssi
   DumpsysWifi.link_speed
   DumpsysWifi.get_match
   DumpsysWifi.__str__

