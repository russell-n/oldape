"""
A module to hold iperf server parameters
"""
#python
from types import BooleanType

#tottest
from iperf_common_tcp_parameters import IperfCommonTcpParameters
from tottest.commons import errors

ConfigurationError = errors.ConfigurationError

class IperfServerParameters(IperfCommonTcpParameters):
    """
    An IperfServerParameters holds parameters for a Tcp Server
    """
    def __init__(self):
        super(IperfServerParameters, self).__init__()
        self._block_attributes = False
        self.server = "--server"
        self._daemon = None
        self._block_attributes = True
        return

    @property
    def daemon(self):
        """
        :return: The daemon flag
        """
        return self._daemon

    @daemon.setter
    def daemon(self, set_daemon):
        """
        :param:

         - `set_daemon`: Boolean which if True sets daemon flag
        """
        if type(set_daemon) is not BooleanType:
            raise ConfigurationError("set_daemon must be Boolean, not {0}".format(set_daemon))
        if set_daemon:
            self._daemon = "--daemon"
        return

# end class IperfTcpServerParameters
