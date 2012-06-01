from nose.tools import raises

from tottest.parameters import iperf_client_parameters
from tottest.commons import errors

from common import assert_equal

ConfigurationError = errors.ConfigurationError
parameters = iperf_client_parameters.IperfTcpClientParameters()

SPACE = ' '
expectation = "--client"

def test_client():
    """
    :test: the client setting
    """
    global expectation
    option = "--client 192.168.20.1"
    expectation = option
    parameters.client = "192.168.20.1"
    assert_equal(option, parameters.client)
    return

@raises(ConfigurationError)
def test_dualtest_failure():
    """
    :test: dualtest non-boolean failure
    """
    parameters.dualtest = "dual"
    return

def test_dualtest():
    """
    :test: The dualtest setting
    """
    global expectation
    option = '--dualtest'
    expectation += SPACE + option
    parameters.dualtest = True
    assert_equal(option, parameters.dualtest)
    assert_equal(expectation, str(parameters))
    return

def check_parameters(option, expectation, parameter):
    assert_equal(option, parameter)
    assert_equal(expectation, str(parameters))
    return

@raises(ConfigurationError)
def check_bad_fileinput():
    """
    :test: raise error if there are spaces in the name
    """
    parameters.fileinput = "file name"
    return

def test_fileinput():
    """
    :test: The fileinput flag setting
    """
    global expectation
    option = "--fileinput filename"
    expectation += SPACE + option
    parameters.fileinput = 'filename'
    check_parameters(option, expectation, parameters.fileinput)
    return

@raises(ConfigurationError)
def test_bad_bytes():
    """
    :test: A bad num-bytes setting
    """
    parameters.num = "5 W"
    return

def test_num_bytes():
    """
    :test: The number of bytes to send
    """
    global expectation
    option = "--num 100K"
    expectation += SPACE + option
    parameters.num = "100K"
    assert_equal(option, parameters.num)
    assert_equal(expectation, str(parameters))
    return

@raises(ConfigurationError)
def test_bad_times():
    """
    :test: bad time input
    """
    parameters.time = "1 hour"
    return
    
def test_time():
    """
    :test: Assignment of time to run
    """
    global expectation
    parameters.time = '3600.5 '
    assert_equal("--time 3600.5", parameters.time)

    option = "--time 3600"
    expectation += SPACE + option
    parameters.time = "3600"
    assert_equal(option, parameters.time)
    assert_equal(expectation, str(parameters))
    return

@raises(ConfigurationError)
def test_bad_tradeoff():
    """
    :test: A bad tradeoff setting
    """
    parameters.tradeoff = "t"
    return

def test_tradeoff():
    """
    :test: the tradeoff flag is set
    """
    global expectation
    option = "--tradeoff"
    expectation += SPACE + option
    parameters.tradeoff = True
    assert_equal(option, parameters.tradeoff)
    assert_equal(expectation, str(parameters))
    return


if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test_bad_bytes()
