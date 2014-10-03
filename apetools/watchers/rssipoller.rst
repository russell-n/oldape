RSSI Poller
===========

An RSSI Poller Polls the device for rssi measurements.
::

    class RssiPollerEnum(object):
        """
        A Holder of rssi-poller constants
        """
        __slots__ = ()
        rssi = 'RSSI'
        rssipoller = 'rssipoller'
    # end class RssiPollerEnum
    
    



.. uml::

   BasePollster <|-- RssiPoller

.. module:: apetools.watchers.rssipoller
.. autosummary::
   :toctree: api

   RssiPoller
   RssiPoller.name
   RssiPoller.expression
   RssiPoller.run

