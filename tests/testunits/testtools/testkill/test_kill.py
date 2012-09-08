"""
Tests the killall module
"""
from unittest import TestCase
from StringIO import StringIO
from mock import MagicMock
import mock
import nose

from tottest.tools import killall
from tottest.commons import enumerations, expressions, errors


from pse_sample import PSE_LINUX, PSE_LINUX_NO_FIREFOX
import ps_android

class KillAllLinuxTest(TestCase):
    def setUp(self):
        connection = MagicMock()
        connection.operating_system = enumerations.OperatingSystem.linux
        self.killer = killall.KillAll(connection, None)
        self.pre_kill_output = PSE_LINUX
        self.post_kill_output = PSE_LINUX_NO_FIREFOX
        self.process = 'firefox'
        self.pid_1 = '209'
        self.pid_2 = '7660'
        self.arguments = '-e'
        return

    def test_expression(self):
        """
        :description: test that the regular expression parses the ps output
        :assert: 'kworker/3:0'  is the process in the given line
        """
        line = '27957 ?        00:00:00 kworker/3:0'
        match = self.killer.expression.search(line)
        self.assertEqual(match.group(expressions.PROCESS_NAME),
                         'kworker/3:0')
        return

    @nose.tools.raises(errors.CommandError)
    def test_kill_failure(self):
        """
        :description: if the process remains on the second ps check, an exception is raised
        
        :assert: killall calls connection.kill('firefox')
        :assert: raises CommandError
        """
        connection = MagicMock()
        connection.ps.return_value = self.pre_kill_output, StringIO("")
        connection.kill = MagicMock()
        killer = killall.KillAll(connection, self.process)
        killer.run(time_to_sleep=0)
        return

    def test_kill_success(self):
        """
        :description: The connection's output should remove all process instances
        
        :assert: killall calls connection.kill with pid '209' followed by pid '7660'
        :assert: connection calls ps with '-e'
        """
        # setup the changing outputs
        output = [self.pre_kill_output, self.post_kill_output]
    
        def outputs(*args, **kwargs):
            return output.pop(0), StringIO('')
    
        connection = MagicMock()
        connection.ps.side_effect = outputs
        connection.kill = MagicMock()
        connection.operating_system = enumerations.OperatingSystem.linux
        killer = killall.KillAll(connection, self.process, enumerations.OperatingSystem.linux)
        killer.run(time_to_sleep=0)
        self.assertEqual(enumerations.OperatingSystem.linux, killer.operating_system)
        expected_args = [mock.call(" -9 " + self.pid_1), mock.call(" -9 " + self.pid_2)]
        actual_args = connection.kill.call_args_list
        self.assertEqual(expected_args, actual_args)
        connection.ps.assert_called_with(self.arguments)
        return
# end class KillAllLinuxTest

class KillAllAndroidTest(TestCase):
    def setUp(self):        
        self.killer = killall.KillAll(None, operating_system=enumerations.OperatingSystem.android)
        self.pre_kill_output = ps_android.output
        self.post_kill_output = ps_android.output_2
        self.process = ps_android.name
        self.pid_1 = ps_android.pid_1
        self.pid_2 = ps_android.pid_2
        self.arguments = ''
        return

    def test_kill_success(self):
        """
        :description: The connection's output should remove all process instances
        
        :assert: killall calls connection.kill with pid '209' followed by pid '7660'
        :assert: connection calls ps with '-e'
        """
        # setup the changing outputs
        output = [self.pre_kill_output, self.post_kill_output]
        
        def outputs(*args, **kwargs):
            return output.pop(0), StringIO('')

        connection = MagicMock()
        connection.ps.side_effect = outputs
        connection.kill = MagicMock()
        killer = killall.KillAll(connection, self.process, enumerations.OperatingSystem.android)
        killer.run(time_to_sleep=0)
        expected_args = [mock.call(" -9 " + self.pid_1), mock.call(" -9 " + self.pid_2)]
        actual_args = connection.kill.call_args_list
        self.assertEqual(expected_args, actual_args)
        connection.ps.assert_called_with(self.arguments)
        return

    def test_expression(self):
        """
        :description: test that the regular expression parses the ps output
        :assert: 'kworker/3:0'  is the process in the given line
        """
        match = self.killer.expression.search(ps_android.line)
        self.assertEqual(match.group(expressions.PROCESS_NAME),
                         ps_android.name)
        return

    @nose.tools.raises(errors.CommandError)
    def test_kill_failure(self):
        """
        :description: if the process remains on the second ps check, an exception is raised
        
        :assert: killall calls connection.kill('firefox')
        :assert: raises CommandError
        """
        connection = MagicMock()
        connection.ps.return_value = self.pre_kill_output, StringIO("")
        connection.kill = MagicMock()
        killer = killall.KillAll(connection, self.process, enumerations.OperatingSystem.android)
        killer.run(time_to_sleep=0)
        return

if __name__ == "__main__":
    import pudb;pudb.set_trace()
    output = [PSE_LINUX, PSE_LINUX_NO_FIREFOX]
    
    
    def outputs(*args, **kwargs):
        return output.pop(0), StringIO('')
    
    connection = MagicMock()
    connection.ps.side_effect = outputs
    connection.kill = MagicMock()
    killer = killall.KillAll(connection, 'firefox', operating_system=enumerations.OperatingSystem.linux)
    killer.run()
    expected_args = [mock.call('209'), mock.call('7660')]
    actual_args = connection.kill.call_args_list
    connection.ps.assert_called_with('-e')

