from unittest import TestCase
from ConfigParser import SafeConfigParser
from StringIO import StringIO

from mock import MagicMock
from tottest.config import lexicographer
from tottest.config import configurationmap

import tot


class LexicographerTest(TestCase):
    def setUp(self):
        parser = configurationmap.ConfigurationMap("tot.ini")
        parser._parser = SafeConfigParser()
        parser._parser.readfp(StringIO(tot.output))
        self.lexicographer = lexicographer.Lexicographer("tot.ini")
        get_parser = MagicMock()
        get_parser.return_value = parser

        filename_generator = MagicMock()
        filename_generator.return_value = ['tot.ini']
        self.lexicographer.get_parser = get_parser
        self.lexicographer.filenames = filename_generator
        
        return

    def test_test_section(self):
        for parameters in self.lexicographer.parameters:
            self.assertEqual(tot.output_folder, parameters.output_folder)
            self.assertEqual('tot.ini', parameters.config_file_name)
            self.assertEqual(tot.dut_test_ip_address, parameters.dut_parameters.test_ip)
            self.assertEqual(tot.tpc_control_ip_address, parameters.tpc_parameters.hostname)
            self.assertEqual(tot.tpc_test_ip_address, parameters.tpc_parameters.test_ip)
            self.assertEqual(tot.tcp_window_size , parameters.iperf_client_parameters.window)
            self.assertEqual(tot.tcp_window_size, parameters.iperf_server_parameters.window)
            self.assertEqual(tot.buffer_length, parameters.iperf_client_parameters.len)
            self.assertEqual(tot.parallel_threads, parameters.iperf_client_parameters.parallel)
            self.assertEqual(tot.data_intervals, parameters.iperf_client_parameters.interval)
            self.assertEqual(tot.data_units, parameters.iperf_client_parameters.format)
            self.assertEqual(str(float(tot.test_duration)), parameters.iperf_client_parameters.time)
        return
