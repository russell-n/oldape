"""
A module to aggregate the tool-builders
"""

from nersbuilder import NersBuilder
from apconnectbuilder import APConnectBuilder
from timetorecoverybuilder import TimeToRecoveryBuilder

class ToolBuilderEnum(object):
    __slots__ = ()
    ners = "ners"
    apconnect = "apconnect"
    timetorecovery = "timetorecovery"
# end class ToolBuilderEnum

tool_builders = {ToolBuilderEnum.ners:NersBuilder,
                 ToolBuilderEnum.apconnect:APConnectBuilder,
                 ToolBuilderEnum.timetorecovery:TimeToRecoveryBuilder}
