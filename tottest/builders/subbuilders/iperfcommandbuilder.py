"""
A builder of iperfcommands
"""

from tottest.lexicographers.config_options import ConfigOptions
from iperfparameterbuilders import IperfParametersBuilder
from tottest.commands.iperfcommand import IperfCommand, IperfCommandEnum
from storagepipebuilder import StoragePipeBuilder
from tottest.pipes.storagepipe import StoragePipeEnum

class IperfCommandBuilder(object):
    """
    A builder of IperfCommands
    """
    def __init__(self, config_map):
        """
        :param:

         - `config_map`: A built configuration map
        """
        self.config_map = config_map
        self._parameters = None
        self._client_command = None
        self._server_command = None
        self._filename = None
        self._output = None
        return

    @property
    def filename(self):
        """
        :return: the filename base from the config-file
        """
        if self._filename is None:
            self._filename = self.config_map.get(section=ConfigOptions.test_section,
                                                 option=ConfigOptions.data_file_option,
                                                 default="",
                                                 optional=True)
        return self._filename

    @property
    def output(self):
        """
        :return: a storage pipe.
        """
        if self._output is None:
            self._output = StoragePipeBuilder(config_map=self.config_map,
                                               role=StoragePipeEnum.sink).pipe
        return self._output

    @property
    def parameters(self):
        """
        :return: An Iperf Parameters Builder
        """
        if self._parameters is None:
            self._parameters = IperfParametersBuilder(self.config_map)
        return self._parameters

    @property
    def client_command(self):
        """
        :return: iperf command with client parameters
        """
        if self._client_command is None:
            self._client_command = IperfCommand(parameters=self.parameters.client_parameters,
                                                output=self.output,
                                                role=IperfCommandEnum.client,
                                                base_filename=self.filename)
        return self._client_command

    @property
    def server_command(self):
        """
        :return: iperf command with server parameters
        """
        if self._server_command is None:
            self._server_command = IperfCommand(parameters=self.parameters.server_parameters,
                                                output=self.output,
                                                role=IperfCommandEnum.server,
                                                base_filename=self.filename)
        return self._server_command
# end class IperfCommandBuilder
