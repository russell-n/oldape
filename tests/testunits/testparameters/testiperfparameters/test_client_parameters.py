# python
from unittest import TestCase

#third party
from nose.tools import raises

# apetools
from apetools.parameters import iperf_client_parameters
from apetools.commons import errors

ConfigurationError = errors.ConfigurationError

SPACE = ' '

client_value = "192.168.20.1"
client_option = "--client " + client_value
dualtest_option =  '--dualtest'
fileinput_value = 'filename'
fileinput_option = "--fileinput " + fileinput_value
listenport_value = "12345"
listenport_option = "--listenport " + listenport_value
num_value = "100K"
num_option = "--num " + num_value
parallel_value = '4'
parallel_option = "--parallel " + parallel_value

time_value_integer = "3600"
time_option_integer = "--time " + time_value_integer
time_value_float = '3600.5 '
time_option_float = "--time " + time_value_float
tradeoff_option = "--tradeoff"
ttl_value = '4'
ttl_option = '--ttl ' + ttl_value

class IperfCommonParametersTest(TestCase):
    def setUp(self):
        self.parameters = iperf_client_parameters.IperfTcpClientParameters()
        return

    def check_parameters(self, option, parameter):
        self.assertEqual(option, parameter)
        self.assertEqual(option, str(self.parameters))
        return
    
    def test_client(self):
        self.parameters.client = client_value
        self.check_parameters(client_option, self.parameters.client)
        return

    @raises(ConfigurationError)
    def test_client_name_with_space(self):
        self.parameters.client = 'elin admin'
        return

    @raises(ConfigurationError)
    def test_client_missing(self):
        self.parameters.client = ''
        return
    
    @raises(ConfigurationError)
    def test_dualtest_non_boolean(self):
        self.parameters.dualtest = "dual"
        return

    def test_dualtest(self):
        self.parameters.dualtest = True
        self.check_parameters(dualtest_option, self.parameters.dualtest)
        return

    @raises(ConfigurationError)
    def check_fileinput_with_space(self):
        self.parameters.fileinput = "file name"
        return

    def test_fileinput(self):
        self.parameters.fileinput = fileinput_value
        self.check_parameters(fileinput_option, self.parameters.fileinput)
        return

    def test_listenport(self):
        self.parameters.listenport = listenport_value
        self.check_parameters(listenport_option, self.parameters.listenport)
        return

    @raises(ConfigurationError)
    def test_non_integer_listenport(self):
        self.parameters.listenport = 'com0'
        return

    @raises(ConfigurationError)
    def test_out_of_range_listenport(self):
        self.parameters.listenport = 0
        return

    def test_parallel(self):
        self.parameters.parallel = parallel_value
        self.check_parameters(parallel_option, self.parameters.parallel)
        return

    @raises(ConfigurationError)
    def test_parallel_failure(self):
        self.parameters.parallel = 'w'
        return
    
    @raises(ConfigurationError)
    def test_invalid_bytes_units(self):
        self.parameters.num = "5 W"
        return

    def test_num_bytes(self):
        self.parameters.num = num_value
        self.check_parameters(num_option, self.parameters.num)
        return

    @raises(ConfigurationError)
    def test_bad_times(self):
        self.parameters.time = "1 hour"
        return
    
    def test_time(self):
        self.parameters.time = time_value_float
        self.check_parameters(time_option_float.rstrip(), self.parameters.time)
        self.parameters.time = time_value_integer
        self.check_parameters(time_option_integer, self.parameters.time)
        return

    @raises(ConfigurationError)
    def test_bad_tradeoff(self):
        self.parameters.tradeoff = "t"
        return

    def test_tradeoff(self):
        self.parameters.tradeoff = True
        self.check_parameters(tradeoff_option, self.parameters.tradeoff)
        return

    def test_ttl(self):
        self.parameters.ttl = ttl_value
        self.check_parameters(ttl_option, self.parameters.ttl)
        return
    
    @raises(ConfigurationError)
    def test_random_assignment(self):
        self.parameters.cow = 'pie'
        return
    
    def test_str(self):
        self.parameters.client = client_value
        self.parameters.dualtest = True
        self.parameters.fileinput = fileinput_value
        self.parameters.listenport = listenport_value
        self.parameters.num = num_value
        self.parameters.parallel = parallel_value
        self.parameters.tradeoff = True
        self.parameters.ttl = ttl_value
        expectation = client_option
        expectation += SPACE + dualtest_option
        expectation += SPACE + fileinput_option
        expectation += SPACE + listenport_option
        expectation += SPACE + num_option
        expectation += SPACE + parallel_option
        expectation += SPACE + tradeoff_option
        expectation += SPACE + ttl_option
        self.assertEqual(expectation, str(self.parameters))
        return

# end class IperfCommonParametersTest
    

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test_bad_bytes()
