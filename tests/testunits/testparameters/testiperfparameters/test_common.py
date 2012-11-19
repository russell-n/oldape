import nose

raises = nose.tools.raises
from tottest.commons import errors
from tottest.parameters import iperf_common_parameters

from common import assert_equal

parameters = iperf_common_parameters.IperfCommonParameters()
ConfigurationError = errors.ConfigurationError

def test_bind():
    """
    :description: Tests that the bind hostname is set
    """
    HOSTNAME = "192.168.20.51"
    parameters.bind = HOSTNAME
    assert_equal( '--bind {0}'.format(HOSTNAME), parameters.bind)

expected = "--bind 192.168.20.51"

def test_bind_string():
    """
    :description: Tests the casting of the parameters to a single string
    """
    assert_equal(expected, str(parameters))
    return

def test_compatibility():
    """
    :description: Tests that True will set the compatability flag
    """
    parameters.compatibility = True
    assert_equal( "--compatibility", parameters.compatibility)
    return
    
def test_compatibility_string():
    """
    :description: Test adding compatability string
    """
    global expected
    expected += " --compatibility"
    assert_equal(expected, str(parameters))

def test_format():
    """
    :description: Test that the format is valid
    """
    FORMAT = 'b'
    parameters.format = FORMAT
    assert_equal("--format " + FORMAT, parameters.format)
    return

def test_format_string():
    """
    :description: test the string after a format is added
    """
    global expected
    expected += ' --format b'
    assert_equal(expected, str(parameters))


def test_interval():
    """
    :description: Tests that the interval is valid
    """
    INTERVAL = '1'
    parameters.interval = INTERVAL
    assert_equal('--interval ' + INTERVAL, parameters.interval)
    parameters.interval = float(INTERVAL)
    assert_equal('--interval {0:.1f}'.format(float(INTERVAL)), parameters.interval)
    return

def test_interval_string():
    """
    :description: test the string after the interval is set
    """
    global expected
    expected += " --interval 1.0" 
    assert_equal(expected, str(parameters))    
    return

def test_ipv6_version():
    """
    :description: Tests that True will set the IPv6Version flag.
    """
    parameters.ipv6version = True
    assert_equal("--IPv6Version", parameters.ipv6version)

@raises(ConfigurationError)
def test_invalid_ipv6_version():
    parameters.ipv6version = 'True'
    return

def test_ipv6_version_string():
    """
    :description: test the string after the ipv6 version is set
    """
    global expected
    expected += " --IPv6Version"
    assert_equal(expected, str(parameters))
    
def test_buffer_length():
    """
    :description: Tests that valid buffer-lengths are accepted.
    """
    parameters.len = 256
    assert_equal('--len {0}'.format(256), parameters.len)

    BUFFER_LENGTH = "256K"
    parameters.len = BUFFER_LENGTH
    assert_equal('--len {0}'.format(BUFFER_LENGTH), parameters.len)
    return

def test_buffer_length_string():
    """
    :description: test the string after the buffer length is added
    """
    global expected
    expected += " --len 256K"
    assert_equal(expected, str(parameters))
    return

@raises(ConfigurationError)
def test_output_failure():
    """
    :description: tests that the output can't have spaces
    """
    parameters.output = "some file"
    return

def test_output():
    """
    :description: Tests that valid output-file names are accepted
    """
    OUTPUT = "some_file"
    parameters.output = OUTPUT
    assert_equal("--output {0}".format(OUTPUT), parameters.output)
    return

def test_output_string():
    """
    :description: Test the output string after it is added.
    """
    global expected
    expected += " --output some_file"
    assert_equal(expected, str(parameters))
    return

def test_port():
    """
    :description: Tests that valid ports are accepted
                  Tests that ports < 1024 raise a warning
    """
    PORT = "4081"
    parameters.port = 2
    parameters.port = PORT
    assert_equal( '--port {0}'.format(PORT), parameters.port,)
    return

def test_port_string():
    """
    :description: Tests that the string changes when the port is set
    """
    global expected
    expected += " --port 4081"
    assert_equal(expected, str(parameters))
    return


def test_reportexclude():
    """
    :description: Tests that valid reportexclude flags are set.
    """
    parameters.reportexclude = "CMSV"
    assert_equal("--reportexclude CMSV", parameters.reportexclude)
    return

def test_reportexclude_string():
    """
    :description: test the string for the reportexclude addition
    """
    global expected
    expected += " --reportexclude CMSV"
    assert_equal(expected, str(parameters))
    return

@raises(ConfigurationError)
def test_invalid_exclude():
    """
    :description: tests setting a flag other than those in CDMSV
    """
    parameters.reportexclude = 'cow'
    return

def test_report_style():
    """
    :description: Tests that setting the report style work
    """
    parameters.reportstyle = 'c'
    assert_equal('--reportstyle c', parameters.reportstyle)
    return


@raises(ConfigurationError)
def test_invalid_report_style():
    """
    :description: Tests that anything but c or C fails
    """
    parameters.reportstyle = 'v'
    return

@nose.tools.raises(errors.ConfigurationError)
def test_case_2():
    """
    :description: test that the parameters are invalid
    """
    parameters.format = 'q'
    return

@nose.tools.raises(errors.ConfigurationError)
def test_case_3():
    """
    :description: Test that only a single character is allowed
    """
    parameters.format = 'bk'
    return

@nose.tools.raises(ConfigurationError)
def test_case_4():
    parameters.interval = 'ted'
    return

@nose.tools.raises(ConfigurationError)
def test_case_5():
    parameters.len = '24P'
    return

@raises(ConfigurationError)
def test_low_port():
    parameters.port = 0
    return

@raises(ConfigurationError)
def test_high_port():
    parameters.port = 10**20
    return

@raises(ConfigurationError)
def test_incompatibility():
    parameters.compatibility = 0
    return

@raises(ConfigurationError)
def test_fake_parameter():
    """
    :description: Tests that trying to set an unknown attribute raises an error
    """
    parameters.length = "256K"
    return






def test_reportexclude_string():
    """
    :description: Test the string after reportinclude is inserted
    """
if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test_output_failure()
