"""
A builder of Iperf Parameters
"""
from apetools.commons.errors import ConfigurationError
from apetools.lexicographers.config_options import ConfigOptions
from apetools.parameters.iperf_common_parameters import IperfParametersEnum
from apetools.parameters.iperf_client_parameters import client_parameters
from apetools.parameters.iperf_server_parameters import server_parameters



class IperfParametersError(ConfigurationError):
    """
    An exception to raise for invalid parameters
    """
# end class IperfParametersError

class IperfParametersBuilder(object):
    """
    A builder of IperfParameters
    """
    def __init__(self, config_map):
        """
        :param:

         - `config_map`: a loaded configuration map
        """
        self.config_map = config_map
        self._client_parameters = None
        self._server_parameters = None
        self._protocol = None
        self._options = None
        return

    @property
    def options(self):
        """
        :return: the configuration-file options for the iperf section
        """
        if self._options is None:
            self._options = self.config_map.options(ConfigOptions.iperf_section)
        return self._options
    
    @property
    def protocol(self):
        """
        :return: tcp or udp (default is tcp)
        """
        if self._protocol is None:
            self._protocol = self.config_map.get(section=ConfigOptions.iperf_section,
                                                 option=ConfigOptions.protocol_option,
                                                 default="tcp",
                                                 optional=True).lower()
            
            if self._protocol not in (IperfParametersEnum.udp, IperfParametersEnum.tcp):
                raise IperfParametersError("Unkown protocol: {0}".format(self._protocol))
        return self._protocol

    @property
    def client_parameters(self):
        """
        :return: Iperf Client Parameters based on the config_map
        """
        if self._client_parameters is None:

            self._client_parameters = client_parameters[self.protocol]()
            for option in self.options:
                if option == "time":
                    self._client_parameters.time = self.config_map.get_time(ConfigOptions.iperf_section,
                                                                            option)
                elif option in self._client_parameters.parameter_names:
                    setattr(self._client_parameters, option, self.config_map.get(ConfigOptions.iperf_section,
                                                                         option))
        return self._client_parameters

    @property
    def server_parameters(self):
        """
        :return: the Iperf Server Parameters based on the config_map
        """
        if self._server_parameters is None:
            self._server_parameters = server_parameters[self.protocol]()
            for option in self.options:
                if option in self._server_parameters.parameter_names:
                    setattr(self._server_parameters, option, self.config_map.get(ConfigOptions.iperf_section,
                                                                         option))

        return self._server_parameters
# end class IperfParametersBuilder
