from unittest import TestCase
from mock import MagicMock
from nose.tools import raises

from apetools.lexicographers.sublexicographers import iperflexicographer
from apetools.lexicographers.config_options import ConfigOptions
from apetools.lexicographers.configurationmap import ConfigurationMap
from apetools.commons.enumerations import IperfDefaults
from apetools.commons.errors import ConfigurationError

WINDOW = "112M"
LENGTH = "14700"
PARALLELS = "2"
INTERVAL = "1"
FORMAT = "b"
TIME = "60"


def side_effect(*args, **kwargs):
    section = ConfigOptions.iperf_section    
    if section in args:
        if  ConfigOptions.window_option in args:
            return WINDOW
        if ConfigOptions.length_option in args:
            return LENGTH
        if ConfigOptions.parallel_option in args:
            return PARALLELS
        if ConfigOptions.interval_option in args:
            return INTERVAL
        if ConfigOptions.format_option in args:
            return FORMAT
        if ConfigOptions.time_option in args:
            return TIME

def optional_side_effect(*args, **kwargs):
    section = ConfigOptions.iperf_section    
    if section in args:
        if  ConfigOptions.window_option in args:
            return None
        if ConfigOptions.length_option in args:
            return None
        if ConfigOptions.parallel_option in args:
            return None
        if ConfigOptions.interval_option in args:
            return None
        if ConfigOptions.format_option in args:
            return None
        if ConfigOptions.time_option in args:
            return TIME

class TestIperfLexicographer(TestCase):
    def setUp(self):
        self.section = ConfigOptions.iperf_section
        self.parser = MagicMock()
        self.map = ConfigurationMap("name")
        self.map._parser = self.parser
        self.lexicographer = iperflexicographer.IperfLexicographer(self.map)
        return

    def test_window(self):
        self.parser.get.return_value = None
        self.assertEqual(IperfDefaults.window, self.lexicographer.window)
        self.parser.get.side_effect = side_effect
        self.lexicographer._window = None
        self.assertEqual(WINDOW, self.lexicographer.window)
        return

    def test_length(self):
        self.parser.get.return_value = LENGTH
        self.assertEqual(LENGTH, self.lexicographer.length)
        self.parser.get.return_value = None
        self.lexicographer._length = None
        self.assertEqual(IperfDefaults.length, self.lexicographer.length)
        return
    
    def test_parallels(self):
        self.parser.get.return_value = PARALLELS
        self.assertEqual(PARALLELS, self.lexicographer.parallel)
        self.parser.get.return_value = None
        self.lexicographer._parallel = None
        self.assertEqual(IperfDefaults.parallel, self.lexicographer.parallel)
        return
    
    def test_interval(self):
        self.parser.get.return_value = INTERVAL
        self.assertEqual(INTERVAL, self.lexicographer.interval)
        self.parser.get.return_value = self.lexicographer._interval = None
        self.assertEqual(IperfDefaults.interval, self.lexicographer.interval)
        return
    
    def test_format(self):
        self.parser.get.return_value = FORMAT
        self.assertEqual(FORMAT, self.lexicographer.format)
        self.parser.get.return_value = self.lexicographer._format = None
        self.assertEqual(IperfDefaults.format, self.lexicographer.format)
        return
        
    def test_time(self):
        self.parser.get.return_value = TIME
        self.assertEqual(TIME, self.lexicographer.time)

    @raises(ConfigurationError)
    def test_no_time(self):
        self.parser.get.return_value = self.lexicographer._time = None
        self.lexicographer.time
        return
    
    def test_client_parameters(self):
        self.parser.get.side_effect = side_effect
        parameters = iperflexicographer.IperfClientParameters(window=WINDOW,
                                                              len=LENGTH,
                                                              parallel=PARALLELS,
                                                              interval=INTERVAL,
                                                              format=FORMAT,
                                                              time=TIME)
        self.assertEqual(parameters, self.lexicographer.client_parameters)
        return
    
    def test_default_client_parameters(self):
        parameters = iperflexicographer.IperfClientParameters(window=IperfDefaults.window,
                                                              len=IperfDefaults.length,
                                                              parallel=IperfDefaults.parallel,
                                                              interval=IperfDefaults.interval,
                                                              format=IperfDefaults.format,
                                                              time=TIME)

        self.lexicographer._client_parameters = None
        self.parser.get.side_effect = optional_side_effect

        self.assertEqual(parameters, self.lexicographer.client_parameters)
        return
    
    def test_server_parameters(self):
        self.parser.get.return_value = WINDOW
        parameters = iperflexicographer.IperfServerParameters(window=WINDOW)
        self.assertEqual(parameters, self.lexicographer.server_parameters)
        return
# end class TestIperfLexicographer
