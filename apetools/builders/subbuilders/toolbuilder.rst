Tool Builder
============

A module to aggregate the tool-builders.

.. note:: This will eventually be replaced by the importer class(es)

The Tool Builder Enum
---------------------

::

    class ToolBuilderEnum(object):
        __slots__ = ()
        ners = "ners"
        apconnect = "apconnect"
        timetorecovery = "timetorecovery"
        dumpdevicestatebuilder = "dumpdevicestatebuilder"
        iperf = "iperf"
        rotate = 'rotate'
        poweron = 'poweron'
        oscillate = 'oscillate'
        oscillatestop = 'oscillatestop'
        sleep = 'sleep'
        naxxx = 'naxxx'
        busyboxwget = 'busiboxwget'
    # end class ToolBuilderEnum
    
    



The Tool Builder
----------------

.. module:: apetools.builders.subbuilders.toolbuilder
.. autosummary:: 
   :toctree: api

   ToolBuilder
   ToolBuilder.busyboxwget
   ToolBuilder.sleep
   ToolBuilder.watchlogs
   ToolBuilder.oscillatestop
   ToolBuilder.oscillate
   ToolBuilder.commandwatch
   ToolBuilder.rotate
   ToolBuilder.poweron
   ToolBuilder.poweroff
   ToolBuilder.ners
   ToolBuilder.apconnect
   ToolBuilder.timetorecovery
   ToolBuilder.dumpdevicestate
   ToolBuilder.iperf
   ToolBuilder.naxxx

