Netsh
=====

A class to make inquiries of the wlan via `netsh`.


Nesh Wlan Expressions
---------------------

.. module:: apetools.commands.netsh
.. autosummary:: 
   :toctree: api

   NetshWlanExpressions
   NetshWlanExpressions.authentication
   NetshWlanExpressions.bssid
   NetshWlanExpressions.channel
   NetshWlanExpressions.cipher
   NetshWlanExpressions.connection_state
   NetshWlanExpressions.description
   NetshWlanExpressions.mac_address
   NetshWlanExpressions.name
   NetshWlanExpressions.radio_type
   NetshWlanExpressions.receive_rate
   NetshWlanExpressions.signal
   NetshWlanExpressions.ssid
   NetshWlanExpressions.transmit_rate
   NetshWlanExpressions.get_expression



Netsh Wlan Keys
---------------

::

    class NetshWlanKeys(object):
        __slots__ = ()
        authentication = "Authentication"
        bssid = "BSSID"
        channel = "Channel"
        cipher = "Cipher"
        connection_state = "State"
        description = "Description"
        mac_address = "Physical"
        name = "Name"
        radio_type = "Radio"
        receive_rate = "Receive"
        signal = "Signal"
        ssid = "SSID"
        transmit_rate = "Transmit"
    # end class NetshWlanExpressions
    
    



Netsh Wlan
----------

.. uml::

   BaseClass <|-- NetshWlan

.. autosummary::
   :toctree: api

   NetshWlan
   NetshWlan.signal
   NetshWlan.output
   NetshWlan.expressions        
   NetshWlan.get_value
   NetshWlan.check_errors
   NetshWlan.reset
   NetshWlan.__getattr__

