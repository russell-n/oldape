from unittest import TestCase
import nose.tools

raises = nose.tools.raises

from tottest.parameters import iperf_common_tcp_parameters
from tottest.commons import errors

ConfigurationError = errors.ConfigurationError

SPACE = ' '


class IperfCommonTcpParametersTest(TestCase):
    def setUp(self):        
        self.parameters = iperf_common_tcp_parameters.IperfCommonTcpParameters()
        self.expected = ''
        return
    
    def test_mss(self):
        """
        :test: setting the mss
        """
        option = "--mss 10"
        self.expected += option
        self.parameters.mss = 10
        self.assertEqual(option, self.parameters.mss)
        self.assertEqual(self.expected, str(self.parameters))
        return

    @raises(ConfigurationError)
    def test_nodelay_error(self):
        """
        :test: setting a non-boolean for the nodelay
        """
        self.parameters.nodelay = "off"
        return

    def test_nodelay(self):
        """
        :description: Test adding the nodelay flag
        """
        option = "--nodelay"
        self.expected += option
        self.parameters.nodelay = True
        self.assertEqual(option, self.parameters.nodelay)
        self.assertEqual(self.expected, str(self.parameters))
        return

    @raises(ConfigurationError)
    def test_print_mss_failure(self):
        """
        :description: Tests that a non-boolean assignment fails.
        """
        self.parameters.print_mss = "cow"
        return

    def test_print_mss(self):
        """
        :description: Test the setting of the print_mss flag
        """
        option = "--print_mss"
        self.expected += option
        self.parameters.print_mss = True
        self.assertEqual(option, self.parameters.print_mss)
        self.assertEqual(self.expected, str(self.parameters))
        return

    @raises(ConfigurationError)
    def test_broken_window(self):
        """
        :description: Test that a bad window format will fail
        """
        self.parameters.window = '256W'
        return

    def test_window(self):
        """
        :description: Tests setting the window size.
        """
        option = "--window 256K"
        self.expected += option
        self.parameters.window = "256K"
        self.assertEqual(option, self.parameters.window)
        self.assertEqual(self.expected, str(self.parameters))
        return

    @raises(ConfigurationError)
    def test_random_assignment(self):
        """
        :description: Tests that misspellings won't work
        """
        self.parameters.print_msss = True
        return
