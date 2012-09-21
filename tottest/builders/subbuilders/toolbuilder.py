"""
A module to aggregate the tool-builders
"""

from nersbuilder import NersBuilder

class ToolBuilderEnum(object):
    __slots__ = ()
    ners = "ners"
# end class ToolBuilderEnum

tool_builders = {ToolBuilderEnum.ners:NersBuilder}
