"""
A module to hold parameters for a Udp Server
"""
#python
from types import BooleanType

# tottest
from tottest.commons import errors
from iperf_server_parameters import IperfServerParameters


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
