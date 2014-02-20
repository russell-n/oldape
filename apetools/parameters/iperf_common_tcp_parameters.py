"""
A module to hold common parameters for tcp (common to server and client).
"""
# python
from types import BooleanType
import re

#apetools
from iperf_common_parameters import IperfCommonParameters
from iperf_common_parameters import VALID_BUFFER_LENGTHS as VALID_WINDOW_LENGTHS
from apetools.commons import errors

ConfigurationError = errors.ConfigurationError


class IperfCommonTcpParameters(IperfCommonParameters):
    """
    IperfCommonTcpParameters is a super-set of the IperfCommonParameters for TCP.
    """
    def __init__(self):
        super(IperfCommonTcpParameters, self).__init__()
        self._block_attributes = False
        self._print_mss = None
        self._window = None
        self._mss = None
        self._nodelay = None
        self._block_attributes = True
        return

    @property
    def nodelay(self):
        """
        :return: the nodelay flag
        """
        return self._nodelay

    @nodelay.setter
    def nodelay(self, set_nodelay):
        """
        :param:

         - `set_nodelay`: Boolean which if True sets the nodelay flag
        """
        if type(set_nodelay) is not BooleanType:
            raise ConfigurationError("`set_nodelay` must be a boolean, not {0}".format(set_nodelay))
        if set_nodelay:
            self._nodelay = "--nodelay"
        return
    
    @property
    def print_mss(self):
        """
        :return: The print_mss flag to show the maximum segment size.
        """
        return self._print_mss

    @print_mss.setter
    def print_mss(self, set_print_mss):
        """
        :param:

         - `set_print_mss`: If True, sets the print_mss flag
        """
        if type(set_print_mss) is not BooleanType:
            raise ConfigurationError("set_print_mss should be a Boolean")
        if set_print_mss:
            self._print_mss = "--print_mss"
        return

    @property
    def window(self):
        """
        :return: The window-size parameter
        """
        return self._window

    @window.setter
    def window(self, new_window):
        """
        :param:

         - `new_window`: The window size `n[KM]`
        """
        if not re.match(VALID_WINDOW_LENGTHS, new_window):
            raise ConfigurationError("Invalid Window ({0}) - should be `n[KM]`".format(new_window))
        self._window = "--window {0}".format(new_window)
        return

    @property
    def mss(self):
        """
        :return: Maximum TCP Segment size flag
        """
        return self._mss

    @mss.setter
    def mss(self, new_mss):
        """
        :param:

         - `new_mss`: An integer value (bytes)
        """
        try:
            self._mss = "--mss {0}".format(int(new_mss))
        except ValueError as error:
            self.logger.error(error)
            raise ConfigurationError("mss must be an integer, not {0}".format(new_mss))
# end class IperfCommonTcpParameters
