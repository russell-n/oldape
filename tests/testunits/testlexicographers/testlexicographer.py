from unittest import TestCase
from ConfigParser import SafeConfigParser
from StringIO import StringIO

from mock import MagicMock
from tottest.lexicographers import lexicographer
from tottest.lexicographers import configurationmap
from tottest.commons import errors

ConfigurationError = errors.ConfigurationError
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

    #def test_test_section(self):
    #    for parameters in self.lexicographer.parameters:
    #        self.assertEqual(tot.output_folder, parameters.output_folder)
            #self.assertEqual('tot.ini', parameters.config_file_name)
            #self.assertEqual(tot.dut_test_ip_address, parameters.dut_parameters.test_ip)
            #self.assertEqual(tot.tpc_control_ip_address, parameters.tpc_parameters.hostname)
            #self.assertEqual(tot.tpc_test_ip_address, parameters.tpc_parameters.test_ip)
            #self.assertEqual(tot.tcp_window_size , parameters.iperf_client_parameters.window)
            #self.assertEqual(tot.tcp_window_size, parameters.iperf_server_parameters.window)
            #self.assertEqual(tot.buffer_length, parameters.iperf_client_parameters.len)
            #self.assertEqual(tot.parallel_threads, parameters.iperf_client_parameters.parallel)
            #self.assertEqual(tot.data_intervals, parameters.iperf_client_parameters.interval)
            #self.assertEqual(tot.data_units, parameters.iperf_client_parameters.format)
            #self.assertEqual(str(float(tot.test_duration)), parameters.iperf_client_parameters.time)
     #   return

    def test_naxxx_section(self):
        switches = '1 2 3 4 5'.split()
        def side_effect(section, switch):
            if switch in switches:
                return switches.pop(0)
            raise ConfigurationError()
        
        lex = lexicographer.Lexicographer('tot.ini')
        parser = MagicMock()        
        parser.get_ranges.return_value = [1,2,3,4,5]
        parser.get_optional.return_value = "192.168.12.60"
        parser.get.side_effect=side_effect
        parameters = lex.naxxx_section(parser)
        self.assertEqual('1 2 3 4 5'.split(), [parameter.switch for parameter in parameters.parameters])
        self.assertEqual("192.168.12.60", parameters.hostname)
        return
