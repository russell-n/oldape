"""
A builder of iperf sessions
"""

from tottest.tools.iperfsession import IperfSession
from iperftestbuilder import IperfTestBuilder

class IperfSessionBuilder(object):
    """
    A class to build an iperf session
    """
    def __init__(self, master, config_map):
        """
        :param:

         - `master`: The Master Builder
         - `config_map`: a pre-loaded configuration map
        """
        self.master = master
        self.config_map = config_map
        self._test = None
        self._product = None
        return

    @property
    def test(self):
        """
        :return: An IperfTest
        """
        if self._test is None:
            self._test = IperfTestBuilder(self.config_map).test
        return self._test

    @property
    def product(self):
        """
        :return: An Iperf Session
        """
        if self._product is None:
            self._product = IperfSession(iperf_test=self.test,
                                         nodes=self.master.nodes,
                                         tpc=self.master.tpc_device)
        return self._product
# end class IperfSessionBuilder
