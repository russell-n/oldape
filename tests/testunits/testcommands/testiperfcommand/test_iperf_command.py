#python
from unittest import TestCase
from StringIO import StringIO
from collections import namedtuple

# third-party
from mock import MagicMock, call
from nose.tools import raises

# tottest
from tottest.commands import iperfcommand
from tottest.parameters import iperf_client_parameters
from tottest.parameters import iperf_server_parameters
from tottest.parameters import iperf_test_parameters
IperfError = iperfcommand.IperfError

#testing
import sample_client
import iperf_failure
import iperf_failure_2
import iperf_server
import iperf_server_failure


class IperfCommandClientTest(TestCase):
    def debug(self):
        import pudb
        pudb.set_trace()
        return
    
    def setUp(self):
        parameters = iperf_client_parameters.IperfTcpClientParameters()
        parameters.client = 'localhost'
        parameters.time = "300"
        parameters.interval = '1'
        parameters.parallel = '4'
        self.parameters = iperf_test_parameters.IperfTestParameters("filename", parameters)
        success_output = StringIO(sample_client.output)
        error_output = MagicMock()
        self.output = MagicMock()
        self.file_output = MagicMock()
        self.output.open.return_value = self.file_output
        self.connection = MagicMock()
        self.connection.iperf.return_value = success_output, error_output
        self.command = iperfcommand.IperfCommand(connection=self.connection, output=self.output, role="client",
                                                 name="TPC",
                                                 parameters=self.parameters)
        return

    def test_client(self):
        self.command.run()
        self.connection.iperf.assert_called_with(str(self.parameters.iperf_parameters))
        parameters = iperf_client_parameters.IperfTcpClientParameters()
        parameters.client = "192.168.20.1"
        parameters.interval = "1"
        parameters.parallel = "3"
        parameters.time = "500"
        new_parameters = iperf_test_parameters.IperfTestParameters("filename", parameters)
        self.command.run(new_parameters)
        self.connection.iperf.assert_called_with(str(new_parameters.iperf_parameters))
        calls = [call(line) for line in StringIO(sample_client.output)]
        self.file_output.write.assert_has_calls(calls)
        return

    def test_filename(self):
        class Parameters(namedtuple("parameters", "filename iperf_parameters")):
            def __str__(self):
                return str(self.iperf_parameters)
        filename = "cow_test"
        parameters = Parameters(filename, self.parameters)
        fixed = "{f}_{r}_{{t}}".format(f=filename, r=self.command.role)
        self.assertEqual("cow_test_client_{t}", fixed)
        self.assertEqual(fixed, self.command.filename(parameters))
        self.command.run(parameters)
        self.output.open.assert_called_with(subdir="raw_iperf",filename=fixed, extension= ".iperf")
        
        param_name = "c_localhost_i_1_P_4"
        filename="{p}_{r}_{{t}}".format(p=param_name, r=self.command.role)
        #self.assertEqual(filename, self.command.filename(self.parameters))
        self.command.run()
        #self.output.open.assert_called_with(filename=filename, extension= ".iperf")
                
        return
    
    @raises(IperfError)
    def test_no_route_to_host(self):
        error_output = StringIO(iperf_failure.output)
        self.connection.iperf.return_value = '', error_output
        self.command.run()
        return

    @raises(IperfError)
    def test_serial_no_route_to_host(self):
        output = StringIO(iperf_failure.output)
        self.connection.iperf.return_value = output, ''
        self.command.run()
        return

    @raises(IperfError)
    def test_no_remote_server(self):
        error_output = StringIO(iperf_failure_2.output)
        self.connection.iperf.return_value = '', error_output
        self.command.run()
        return

    @raises(IperfError)
    def test_serial_no_remote_server(self):
        error_output = StringIO(iperf_failure_2.output)
        self.connection.iperf.return_value = error_output, ''
        self.command.run()
        return
# end class IperfCommandClientTest

class IperfCommandServerTest(TestCase):
    def setUp(self):
        parameters = iperf_server_parameters.IperfServerParameters()
        self.parameters = iperf_test_parameters.IperfTestParameters("filename", parameters)

        success_output = StringIO(iperf_server.output)
        error_output = MagicMock()
        self.output = MagicMock()
        self.file_output = MagicMock()
        self.output.open.return_value = self.file_output
        self.connection = MagicMock()
        self.connection.iperf.return_value = success_output, error_output
        self.command = iperfcommand.IperfCommand(connection=self.connection,
                                                 output=self.output,
                                                 role='server',
                                                 name="DUT",
                                                 parameters = self.parameters)
        return

    def test_server_command(self):
        self.command.run()
        calls = [call(line) for line in StringIO(iperf_server.output)]
        self.file_output.write.assert_has_calls(calls)
        return

    
    def test_duplicate_server(self):
        output = StringIO(iperf_server_failure.output)
        self.connection.iperf.return_value = '', output
        self.command.run()
        return


    
    def test_duplicate_server_over_serial(self):
        output = StringIO(iperf_server_failure.output)
        self.connection.iperf.return_value = output, StringIO('')
        self.command.run()
        return
# end class IperfCommandServerTest
