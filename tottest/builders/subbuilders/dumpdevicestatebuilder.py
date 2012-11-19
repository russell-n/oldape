"""
A builder of device-state dumpers
"""

#python
from collections import namedtuple

from tottest.tools.dumpdevicestate import DumpDeviceState
from basetoolbuilder import BaseToolBuilder, Parameters


class DumpDeviceStateBuilderEnum(object):
    __slots__ = ()
    name = "nodes"

class DumpDeviceStateBuilder(BaseToolBuilder):
    """
    A class to build device-state dumpers
    """
    def __init__(self, target=None, *args, **kwargs):
        super(DumpDeviceStateBuilder, self).__init__(*args, **kwargs)
        self.target = target
        return

    @property
    def product(self):
        """
        :return: a DumpDeviceState
        """
        if self._product is None:
            self._product = DumpDeviceState(self.master.nodes, self.target)
        return self._product

    @property
    def parameters(self):
        """
        :return: list of namedtuples with `name` and `parameters` attribute
        """
        if self._parameters is None:
            # needs to add `nodes` to the `previous_parameters`
            if not any([p.name == DumpDeviceStateBuilderEnum.name for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=DumpDeviceStateBuilderEnum.name,
                                                           parameters=self.master.nodes.keys()))
            self._parameters = self.previous_parameters
        return self._parameters
# end class DumpDeviceStateBuilder
