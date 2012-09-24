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
    name = "ners"

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
        :return: namedtuple with `name` and `parameters` attribute
        """
        if self._parameters is None:            
            self._parameters = Parameters(name=NersBuilderEnum.name,
                                          parameters=[Parameters(name=NersBuilderEnum.name,
                                                                 parameters=[key]) for key in self.master.nodes])
        return self._parameters
# end class NersBuilder
