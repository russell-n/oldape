Device Poller
=============

An Device Poller Polls the device for changing measurements.
::

    class DevicePollerEnum(object):
        """
        A Holder of rssi-poller constants
        """
        __slots__ = ()
        rssi = 'RSSI'
        devicepoller = 'devicepoller'
    # end class DevicePollerEnum
    
    



.. uml::

   BasePollster <|-- DevicePoller

.. module:: apetools.watchers.devicepoller
.. autosummary::
   :toctree: api

   DevicePoller
   DevicePoller.name
   DevicePoller.expression
   DevicePoller.run

