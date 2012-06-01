import nose.tools

raises = nose.tools.raises

from tottest.parameters import iperf_common_tcp_parameters
from tottest.commons import errors

from ..common import assert_equal


ConfigurationError = errors.ConfigurationError

#def test_constructor():
#    assert_equal('', str(parameters))
#    return

SPACE = ' '

expected = ''

parameters = iperf_common_tcp_parameters.IperfCommonTcpParameters()
    
def test_mss():
    """
    :test: setting the mss
    """
    global expected
    option = "--mss 10"
    expected += option
    parameters.mss = 10
    assert_equal(option, parameters.mss)
    assert_equal(expected, str(parameters))
    return

@raises(ConfigurationError)
def test_nodelay_error():
    """
    :test: setting a non-boolean for the nodelay
    """
    parameters.nodelay = "off"
    return

def test_nodelay():
    """
    :description: Test adding the nodelay flag
    """
    global expected
    option = "--nodelay"
    expected += SPACE + option
    parameters.nodelay = True
    assert_equal(option, parameters.nodelay)
    assert_equal(expected, str(parameters))
    return

@raises(ConfigurationError)
def test_print_mss_failure():
    """
    :description: Tests that a non-boolean assignment fails.
    """
    parameters.print_mss = "cow"
    return

def test_print_mss():
    """
    :description: Test the setting of the print_mss flag
    """
    global expected
    option = "--print_mss"
    expected += SPACE + option
    parameters.print_mss = True
    assert_equal(option, parameters.print_mss)
    assert_equal(expected, str(parameters))
    return

@raises(ConfigurationError)
def test_broken_window():
    """
    :description: Test that a bad window format will fail
    """
    parameters.window = '256W'
    return

def test_window():
    """
    :description: Tests setting the window size.
    """
    global expected
    option = "--window 256K"
    expected += SPACE + option
    parameters.window = "256K"
    assert_equal(option, parameters.window)
    assert_equal(expected, str(parameters))
    return

@raises(ConfigurationError)
def test_random_assignment():
    """
    :description: Tests that misspellings won't work
    """
    parameters.print_msss = True
    return
