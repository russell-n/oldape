"""
A builder of Network Radio Switches
"""

from tottest.affectors.ners import NeRS
from basetoolbuilder import BaseToolBuilder, Parameters
from builderenums import BuilderParameterEnums


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
            if not any([p.name == BuilderParameterEnums.nodes for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=BuilderParameterEnums.nodes,
                                                           parameters=self.master.nodes.keys()))
            self._parameters = self.previous_parameters
        return self._parameters
# end class NersBuilder
