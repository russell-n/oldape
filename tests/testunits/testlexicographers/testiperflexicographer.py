from unittest import TestCase
from mock import MagicMock

from tottest.lexicographers.sublexicographers import iperflexicographer
from tottest.lexicographers.config_options import ConfigOptions
from tottest.commons.enumerations import IperfDefaults

WINDOW = "112M"
LENGTH = "14700"
PARALLELS = "2"
INTERVAL = "1"
FORMAT = "b"
TIME = "60"


def get_optional_side_effect(*args, **kwargs):
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


def get_time_side_effect(*args, **kwargs):
    if ConfigOptions.iperf_section in args:
        if ConfigOptions.time_option in args:
            return TIME

def get_optional_side_effect_nones(*args, **kwargs):
    section = ConfigOptions.iperf_section
    if section in args:
        return kwargs["default"]


class TestIperfLexicographer(TestCase):
    def setUp(self):
        self.section = ConfigOptions.iperf_section
        self.parser = MagicMock()
        self.lexicographer = iperflexicographer.IperfLexicographer(self.parser)
        self.parser.get_optional.side_effect = get_optional_side_effect
        self.parser.get_time.side_effect = get_time_side_effect
        return

    def test_window(self):
        self.assertEqual(WINDOW, self.lexicographer.window)
        return

    def test_length(self):
        self.assertEqual(LENGTH, self.lexicographer.length)
        return

    def test_parallels(self):
        self.assertEqual(PARALLELS, self.lexicographer.parallel)
        return

    def test_interval(self):
        self.assertEqual(INTERVAL, self.lexicographer.interval)
        return

    def test_format(self):
        self.assertEqual(FORMAT, self.lexicographer.format)
        return
        
    def test_time(self):
        self.assertEqual(TIME, self.lexicographer.time)
        return

    def test_client_parameters(self):
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
        parser = MagicMock()
        parser.get_time.side_effect = get_time_side_effect
        parser.get_optional.side_effect = get_optional_side_effect_nones
        lexicographer = iperflexicographer.IperfLexicographer(parser)
        self.assertEqual(parameters, lexicographer.client_parameters)
        return

    def test_server_parameters(self):
        parameters = iperflexicographer.IperfServerParameters(window=WINDOW)
        self.assertEqual(parameters, self.lexicographer.server_parameters)
        return
