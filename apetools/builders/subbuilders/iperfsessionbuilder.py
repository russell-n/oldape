"""
A builder of iperf sessions
"""

from apetools.lexicographers.config_options import ConfigOptions
from apetools.tools.iperfsession import IperfSession
from apetools.commons.errors import ConfigurationError

from iperftestbuilder import IperfTestBuilder
from basetoolbuilder import BaseToolBuilder, Parameters
from builderenums import BuilderParameterEnums

class IperfSessionBuilderError(ConfigurationError):
    """
    An error to raise if the config file has an error
    """
# end class IperfSessionBuilderError


class IperfSessionBuilder(BaseToolBuilder):
    """
    A class to build an iperf session
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `master`: The Master Builder
         - `config_map`: a pre-loaded configuration map
        """
        super(IperfSessionBuilder, self).__init__(*args, **kwargs)
        self._test = None
        self._directions = None
        self._filename = None
        return

    @property
    def filename(self):
        """
        :return: the filename given by the user
        """
        if self._filename is None:
            self._filename = self.config_map.get(ConfigOptions.test_section,
                                                 ConfigOptions.output_folder_option,
                                                 default=None,
                                                 optional=True)
        return self._filename

    @property
    def test(self):
        """
        :return: An IperfTest
        """
        if self._test is None:
            self._test = IperfTestBuilder(self.config_map).test
        return self._test

    @property
    def directions(self):
        """
        :return: list of traffic directions
        """
        if self._directions is None:
            self._directions = self.config_map.get_list(ConfigOptions.iperf_section,
                                                  ConfigOptions.directions_option)
            for direction in self._directions:
                if self.product.to_node_expression.search(direction):
                    continue
                if self.product.from_node_expression.search(direction):
                    continue
                raise IperfSessionBuilderError("Unknown Direction: {0}".format(direction))
        return self._directions
    
    @property
    def product(self):
        """
        :return: An Iperf Session
        """
        if self._product is None:
            self._product = IperfSession(iperf_test=self.test,
                                         nodes=self.master.nodes,
                                         tpc=self.master.tpc_device,
                                         filename_base=self.filename)
        return self._product

    @property
    def parameters(self):
        """
        :return: list of namedtuples
        """
        if self._parameters is None:
            if not any([p.name == BuilderParameterEnums.nodes for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=BuilderParameterEnums.nodes,
                                                           parameters=self.master.nodes.keys()))
            if not any([p.name == BuilderParameterEnums.iperf_directions for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=BuilderParameterEnums.iperf_directions,
                                                           parameters=self.directions))
            self._parameters = self.previous_parameters
        return self._parameters
# end class IperfSessionBuilder
