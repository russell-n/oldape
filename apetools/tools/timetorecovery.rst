Time To Recovery
================

The time to failure pings a target until the pings fail.

::

    class TTRData(namedtuple("TTRData", "ttr rtt")):
        """
        A TTRData holds the TimeToRecovery data
        """
        __slots__ = ()
    
        def __str__(self):
            return "ttr={0},rtt={1}".format(self.ttr, self.rtt)
    
    



.. uml::

   BaseClass <|-- TimeToRecover

.. module:: apetools.tools.timetorecovery
.. autosummary::
   :toctree: api

   TimeToRecovery
   TimeToRecovery.pinger
   TimeToRecovery._unpack_parameters
   TimeToRecovery.run
   TimeToRecovery.__call__

