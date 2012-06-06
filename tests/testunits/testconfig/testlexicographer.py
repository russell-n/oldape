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
            self.assertEqual('tot.ini', parameters.source_file)
            self.assertEqual(tot.data_file, parameters.data_file)
            self.assertEqual(tot.dut_test_ip_address, parameters.dut_test_ip)
            self.assertEqual(tot.tpc_control_ip_address, parameters.tpc_control_ip)
            self.assertEqual(tot.tpc_test_ip_address, parameters.tpc_test_ip)
            self.assertEqual(tot.tcp_window_size , parameters.iperf.window)
            self.assertEqual(tot.buffer_length, parameters.iperf.len)
            self.assertEqual(tot.parallel_threads, parameters.iperf.parallel)
            self.assertEqual(tot.data_intervals, parameters.iperf.interval)
            self.assertEqual(tot.data_units, parameters.iperf.format)
            self.assertEqual(str(float(tot.test_duration)), parameters.iperf.time)
        return

    
