"""
A module to aggregate the tool-builders
"""

from nersbuilder import NersBuilder
from apconnectbuilder import APConnectBuilder

class ToolBuilderEnum(object):
    __slots__ = ()
    ners = "ners"
    apconnect = "apconnect"
# end class ToolBuilderEnum

tool_builders = {ToolBuilderEnum.ners:NersBuilder,
                 ToolBuilderEnum.apconnect:APConnectBuilder}
