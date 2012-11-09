"""
A module to aggregate the tool-builders

This will eventually be replaced by the importer class(es)
"""

class ToolBuilderEnum(object):
    __slots__ = ()
    ners = "ners"
    apconnect = "apconnect"
    timetorecovery = "timetorecovery"
    dumpdevicestatebuilder = "dumpdevicestatebuilder"
    iperf = "iperf"
    rotate = 'rotate'
# end class ToolBuilderEnum

class ToolBuilder(object):
    """
    An aggregator of tool builders
    """
    def __init__(self):
        self._ners = None
        self._apconnect = None
        self._timetorecovery = None
        self._dumpdevicestate = None
        self._iperf = None
        self._rotate = None
        return

    @property
    def rotate(self):
        from rotatebuilder import RotateBuilder
        return RotateBuilder
    
    @property
    def ners(self):
        from nersbuilder import NersBuilder
        return NersBuilder

    @property
    def apconnect(self):
        from apconnectbuilder import APConnectBuilder
        return APConnectBuilder

    @property
    def timetorecovery(self):
        from timetorecoverybuilder import TimeToRecoveryBuilder
        return TimeToRecoveryBuilder

    @property
    def dumpdevicestate(self):
        from dumpdevicestatebuilder import DumpDeviceStateBuilder
        return DumpDeviceStateBuilder

    @property
    def iperf(self):
        from iperfsessionbuilder import IperfSessionBuilder
        return IperfSessionBuilder
# end class ToolBuilder
        
#tool_builders = {ToolBuilderEnum.ners:NersBuilder,
#                 ToolBuilderEnum.apconnect:APConnectBuilder,
#                 ToolBuilderEnum.timetorecovery:TimeToRecoveryBuilder}
