Timestamps
==========

A module to store common timestamp formats.


Timestamp Format Constants
--------------------------
::

    class TimestampFormatEnums(object):
        """
        A class to hold the format names
        """
        __slots__ = ()
        iperf = "iperf"
        log = 'log'
    # end class TimestampFormatEnums
    
    formats = {TimestampFormatEnums.iperf:"%Y%m%d%H%M%S",
               TimestampFormatEnums.log:LOG_TIMESTAMP}
    
    



Timestamp Format
----------------

.. module:: apetools.commons.timestamp
.. autosummary::
   :toctree: api

   TimestampFormat
   TimestampFormat.format
   TimestampFormat.now
   TimestampFormat.convert
   TimestampFormat.__call__

