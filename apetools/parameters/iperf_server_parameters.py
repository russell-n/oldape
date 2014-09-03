"""
A module to hold iperf server parameters
"""
#python
from types import BooleanType

#apetools
from iperf_common_tcp_parameters import IperfCommonTcpParameters
from iperf_common_parameters import IperfParametersEnum
from apetools.commons import errors

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
        Daemon setter (anything other than None, 0 or False will set the flag)
        :param:

         - `set_daemon`: Boolean which if True sets daemon flag
        """
        #if type(set_daemon) is not BooleanType:
        #    raise ConfigurationError("set_daemon must be Boolean, not {0}".format(set_daemon))
        if set_daemon:
            self._daemon = "--daemon"
        return

# end class IperfTcpServerParameters

class IperfUdpServerParameters(IperfServerParameters):
    """
    IperfUdpServerParameters holds parameters for a UDP Server
    """
    def __init__(self):
        super(IperfUdpServerParameters, self).__init__()
        self._block_attributes = False
        self.udp = "--udp"
        self._single_udp = None
        self._block_attributes = True
        return

    @property
    def single_udp(self):
        """
        :return: The single udp thread flag
        """
        return self._single_udp

    @single_udp.setter
    def single_udp(self, set_single_udp):
        """
        :param:

         - `set_single_udp`: Boolen which if True sets the single_udp flag.
        """
        if type(set_single_udp) is not BooleanType:
            raise errors.ConfigurationError("set_single_udp must be Boolean, not {0}".format(set_single_udp))
        if set_single_udp:
            self._single_udp = "--single_udp"
        return
    
# end IperfUdpServerParameters

server_parameters = {IperfParametersEnum.tcp:IperfServerParameters,
                     IperfParametersEnum.udp: IperfUdpServerParameters}
