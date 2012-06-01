from nose import tools

raises = tools.raises
from tottest.parameters import iperf_server_parameters, iperf_udp_server_parameters
from tottest.commons import errors

ConfigurationError = errors.ConfigurationError
from ..common import assert_equal

parameters = iperf_server_parameters.IperfServerParameters()
uparameters = iperf_udp_server_parameters.IperfUdpServerParameters()

SPACE = ' '

def test_server():
    """
    :test: The server setting
    """
    assert_equal("--server", parameters.server)
    return

@raises(ConfigurationError)
def test_daemon_failure():
    parameters.daemon = "daemon"
    return

def test_daemon():
    """
    :test: the daemon setting
    """
    parameters.daemon = True
    assert_equal("--daemon", parameters.daemon)
    return

@raises(ConfigurationError)
def test_random():
    """
    :test: random attributes can't be assigned
    """
    parameters.demon = True
    return

# Udp
expectation = "--server --udp"
def test_udp_server():
    """
    :test: default udp server setttings
    """
    assert_equal(expectation, str(uparameters))
    return

@raises(ConfigurationError)
def test_single_udp_failure():
    """
    :test: the single udp flag isn't a boolean
    """
    uparameters.single_udp = "True"
    return

def test_single_udp():
    """
    :test: The single-threaded udp flag is set
    """
    global expectation
    option = "--single_udp"
    expectation =  option + SPACE + expectation
    uparameters.single_udp = True
    assert_equal(expectation, str(uparameters))
    assert_equal(option, uparameters.single_udp)
    return

@raises(ConfigurationError)
def test_random_udp():
    """
    :test: That random attributes can't be assigned
    """
    uparameters.daemonic = True
    return

