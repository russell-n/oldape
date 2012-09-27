"""
A builder of AP Connectors
"""

#python
from collections import namedtuple

from tottest.affectors.apconnect import APConnect
from tottest.lexicographers.config_options import ConfigOptions

from basetoolbuilder import BaseToolBuilder


Parameters = namedtuple("Parameters", "name parameters".split())

class APConnectBuilderEnum(object):
    __slots__ = ()
    nodes = "nodes"
    ssids = "ssids"

class APConnectBuilder(BaseToolBuilder):
    """
    A class to build AP Connectors
    """
    def __init__(self, *args, **kwargs):
        super(APConnectBuilder, self).__init__(*args, **kwargs)
        self._ssids = None
        return

    @property
    def ssids(self):
        """
        :return: list of ssids from the config file
        """
        if self._ssids is None:
            self._ssids = self.config_map.get_list(ConfigOptions.apconnect_section,
                                                   ConfigOptions.ssids_option)
        return self._ssids

    @property
    def product(self):
        """
        :return: an APConnect
        """
        if self._product is None:
            self._product = APConnect(self.master.nodes)
        return self._product

    @property
    def parameters(self):
        """
        :return: namedtuple with `name` and `parameters` attribute
        """
        if self._parameters is None:

            if not any([p.name == APConnectBuilderEnum.nodes for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=APConnectBuilderEnum.nodes,
                                                           parameters=self.master.nodes.keys()))

            if not any([p.name == APConnectBuilderEnum.ssids for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=APConnectBuilderEnum.ssids,
                                                           parameters=self.ssids))

            self._parameters = self.previous_parameters
        return self._parameters
# end class NersBuilder
