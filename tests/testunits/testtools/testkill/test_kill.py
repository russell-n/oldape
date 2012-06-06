"""
Tests the killall module
"""
from StringIO import StringIO
from mock import MagicMock
import mock
import nose

from tottest.tools import killall
from tottest.commons import enumerations, expressions, errors

from ..common import assert_equal
from pse_sample import PSE_LINUX, PSE_LINUX_NO_FIREFOX

def test_defaults():
    """
    :description:  test the default os
    :assert: the os is linux
    """
    killer = killall.KillAll(None, None)
    assert_equal(enumerations.OperatingSystem.linux,
                 killer.operating_system)
    return

def test_expression():
    """
    :description: test that the regular expression parses the ps output
    :assert: 'kworker/3:0'  is the process in the given line
    """
    killer = killall.KillAll(None, None)
    line = '27957 ?        00:00:00 kworker/3:0'
    match = killer.expression.search(line)
    assert_equal(match.group(expressions.PROCESS_NAME),
                 'kworker/3:0')
    return

@nose.tools.raises(errors.CommandError)
def test_kill_failure():
    """
    :description: if the process remains on the second ps check, an exception is raised

    :assert: killall calls connection.kill('firefox')
    :assert: raises CommandError
    """
    connection = MagicMock()
    connection.ps.return_value = PSE_LINUX, StringIO("")
    connection.kill = MagicMock()
    killer = killall.KillAll(connection, "firefox")
    killer.run()
    return

def test_kill_success():
    """
    :description: The connection's output should remove all 'firefox' instances

    :assert: killall calls connection.kill with pid '209' followed by pid '7660'
    :assert: connection calls ps with '-e'
    """
    process = 'firefox'
    pid_1 = "209"
    pid_2 = '7660'



    # setup the changing outputs
    output = [PSE_LINUX, PSE_LINUX_NO_FIREFOX]
    def outputs(*args, **kwargs):
        return output.pop(0), StringIO('')
    
    connection = MagicMock()
    connection.ps.side_effect = outputs
    connection.kill = MagicMock()
    killer = killall.KillAll(connection, process)
    killer.run()
    expected_args = [mock.call(pid_1), mock.call(pid_2)]
    actual_args = connection.kill.call_args_list
    assert_equal(expected_args, actual_args)
    connection.ps.assert_called_with("-e")
    return

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test_kill_success()
