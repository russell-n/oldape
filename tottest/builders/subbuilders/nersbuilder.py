"""
A builder of Network Radio Switches
"""

#python
from collections import namedtuple

from tottest.affectors.ners import NeRS
from basetoolbuilder import BaseToolBuilder

Parameters = namedtuple("Parameters", "name parameters".split())

class NersBuilderEnum(object):
    __slots__ = ()
    name = "nodes"

class NersBuilder(BaseToolBuilder):
    """
    A class to build NeRS's
    """
    def __init__(self, *args, **kwargs):
        super(NersBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        :return: a Ners
        """
        if self._product is None:
            self._product = NeRS(self.master.nodes)
        return self._product

    @property
    def parameters(self):
        """
        :return: list of namedtuples with `name` and `parameters` attribute
        """
        if self._parameters is None:
            # needs to add `nodes` to the `previous_parameters`
            if not any([p.name == NersBuilderEnum.name for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=NersBuilderEnum.name,
                                                           parameters=self.master.nodes.keys()))
            self._parameters = self.previous_parameters
        return self._parameters
# end class NersBuilder
