"""
A module to aggregate the tool-builders
"""

class ToolBuilderEnum(object):
    __slots__ = ()
    ners = "ners"
    apconnect = "apconnect"
    timetorecovery = "timetorecovery"
    dumpdevicestatebuilder = "dumpdevicestatebuilder"
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
        return

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
# end class ToolBuilder
        
#tool_builders = {ToolBuilderEnum.ners:NersBuilder,
#                 ToolBuilderEnum.apconnect:APConnectBuilder,
#                 ToolBuilderEnum.timetorecovery:TimeToRecoveryBuilder}