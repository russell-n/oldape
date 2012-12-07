from unittest import TestCase

from nose.tools import raises

from apetools.commons import errors
from apetools.parameters import iperf_client_parameters

SPACE = ' '
bandwidth_value = '5M'
bandwidth_option = "--bandwidth " + bandwidth_value


class IperfUdpClientParametersTest(TestCase):
    def setUp(self):
        self.parameters = iperf_client_parameters.IperfUdpClientParameters()
        self.suffix = '--udp'
        return

    def check_parameters(self, option, parameter):
        self.assertEqual(option, parameter)
        self.assertEqual(option + SPACE + self.suffix, str(self.parameters))
        return
    
    @raises(errors.ConfigurationError)
    def test_random_assignment(self):
        self.parameters.cow = "pie"
        return

    def test_bandwidth(self):
        self.parameters.bandwidth = bandwidth_value
        self.check_parameters(bandwidth_option, self.parameters.bandwidth)
        return

    @raises(errors.ConfigurationError)
    def test_bad_bandwidth_units(self):
        self.parameters.bandwidth = "5H"
        return
# end class IperfUdpClientParametersTest
