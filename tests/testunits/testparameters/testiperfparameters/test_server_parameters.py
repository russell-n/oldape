from unittest import TestCase

from nose import tools

raises = tools.raises
from apetools.parameters import iperf_server_parameters, iperf_udp_server_parameters
from apetools.commons import errors

ConfigurationError = errors.ConfigurationError





SPACE = ' '

class IperfServerParametersTest(TestCase):
    def setUp(self):
        self.parameters = iperf_server_parameters.IperfServerParameters()
        return
    
    def test_server(self):
        """
        :test: The server setting
        """
        self.assertEqual("--server", self.parameters.server)
        return

    @raises(ConfigurationError)
    def test_daemon_failure(self):
        self.parameters.daemon = "daemon"
        return

    def test_daemon(self):
        """
        :test: the daemon setting
        """
        self.parameters.daemon = True
        self.assertEqual("--daemon", self.parameters.daemon)
        return

    @raises(ConfigurationError)
    def test_random(self):
        """
        :test: random attributes can't be assigned
        """
        self.parameters.demon = True
        return

# Udp
class IperfUdpServerParametersTest(TestCase):
    def setUp(self):
        self.uparameters = iperf_udp_server_parameters.IperfUdpServerParameters()
        self.expectation  = "--server --udp"
        return

    def test_udp_server(self):
        """
        :test: default udp server setttings
        """
        self.assertEqual(self.expectation, str(self.uparameters))
        return

    @raises(ConfigurationError)
    def test_single_udp_failure(self):
        """
        :test: the single udp flag isn't a boolean
        """
        self.uparameters.single_udp = "True"
        return

    def test_single_udp(self):
        """
        :test: The single-threaded udp flag is set
        """
        option = "--single_udp"
        self.expectation =  option + SPACE + self.expectation
        self.uparameters.single_udp = True
        self.assertEqual(self.expectation, str(self.uparameters))
        self.assertEqual(option, self.uparameters.single_udp)
        return

    @raises(ConfigurationError)
    def test_random_udp(self):
        """
        :test: That random attributes can't be assigned
        """
        self.uparameters.daemonic = True
        return

