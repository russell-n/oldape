"""
An ADB connection sends commands to a local ADB Connection and
interprets errors
"""
# python Libraries
import re
from StringIO import StringIO

# tottest Libraries
from localconnection import LocalNixConnection
from localconnection import OutputError
from localconnection import EOF
from tottest.commons import errors 
from tottest.commons import readoutput 
from tottest.commons import enumerations
from sshconnection import SSHConnection 

ConnectionError = errors.ConnectionError
CommandError = errors.CommandError
ConnectionWarning = errors.ConnectionWarning
ValidatingOutput = readoutput.ValidatingOutput
OperatingSystem = enumerations.OperatingSystem

# Error messages
DEVICE_NOT_FOUND = "error: device not found"
NOT_CONNECTED = "No Android Device Detected by ADB (USB) Connection"

DEVICE_NOT_ROOTED = "adbd cannot run as root in production builds"
NOT_ROOTED = "This Android device isn't rootable."
NOT_FOUND = "not found"

#regular expressions
ALPHA = r'\w'
ONE_OR_MORE = "+"
ZERO_OR_MORE = "*"
SPACE = r"\s"
SPACES = SPACE + ONE_OR_MORE
NAMED = "(?P<{n}>{p})"
COMMAND_GROUP = "command"
ANYTHING = r'.'
EVERYTHING = ANYTHING + ZERO_OR_MORE

class ADBConnection(LocalNixConnection):
    """
    An ADB Connection sends commands to the Android Debug Bridge
    """
    def __init__(self, serial_number=None,*args, **kwargs):
        """
        :param:

         - `serial_number`: An optional serial number to specify the device.
        """
        super(ADBConnection, self).__init__(*args, **kwargs)
        self._logger = None
        self.command_prefix = "adb"
        if serial_number is not None:
            self.command_prefix += " -s " + serial_number
        self._operating_system = None
        return

    @property
    def operating_system(self):
        """
        :return: enumeration for android
        """
        if self._operating_system is None:
            self._operating_system = OperatingSystem.android
        return self._operating_system

    def _rpc(self, command, arguments='', timeout=None):
        """
        Overrides the LocalConnection._rpc to check for errors
        """
        output = self._main(command, arguments, timeout)
        return OutputError(ValidatingOutput(lines=output.output, validate=self.check_errors), StringIO(EOF))


    def check_errors(self, line):
        """
        This is here so that children can override it.
        :param:

         - `output`: OutputError tuple
        """
        self.check_base_errors(line)
        return
    
    def check_base_errors(self, line):
        """
        :param:

         - `line`: A string of output
        """
        if line.startswith(DEVICE_NOT_FOUND):
            self.logger.debug(line)
            raise ConnectionError(NOT_CONNECTED)
        elif line.startswith(DEVICE_NOT_ROOTED):
            self.logger.debug(line)
            raise ConnectionWarning(NOT_ROOTED)
        return
        
# end class ADBConnection

class ADBBlockingConnection(ADBConnection):
    """
    Like the ADBConnection but waits for a device to come online
    """
    def __init__(self, *args, **kwargs):
        super(ADBBlockingConnection, self).__init__(*args, **kwargs)
        self.command_prefix += " wait-for-device"
        return
# end class ADBConnection

class ADBShellConnection(ADBConnection):
    """
    An ADBShellConnection connects to the adb shell.

    If you use a timeout parameter on method calls, the output acts line-buffered.
    If you leave the timeout as None, it acts file-buffered
    """
    def __init__(self, *args, **kwargs):
        super(ADBShellConnection, self).__init__(*args, **kwargs)
        self.command_prefix += " shell"
        self._unknown_command = None
        self._logger = None
        return

    @property
    def unknown_command(self):
        """
        :rtype: SRE_Pattern
        :return: regex to match unknown_command error.
        """
        if self._unknown_command is None:
            self._unknown_command = re.compile(SPACES.join([NAMED.format(n=COMMAND_GROUP, p=ALPHA + ONE_OR_MORE) + ":",
                                                            EVERYTHING, 'not', 'found']))
        return self._unknown_command

    def check_errors(self, line):
        self.check_base_errors(line)
        match = self.unknown_command.search(line)
        if match:
            self.logger.debug(match.group(COMMAND_GROUP))
            raise ConnectionError("Unknown ADB Shell Command: {0}".format(match.group(COMMAND_GROUP)))
        return

    #def __del__(self):
    #    """
    #    :postcondition: kill called on all adb shell processes
    #    """
    #    kill = killall.KillAll(self, name=self.command_prefix,
    #                             operating_system=enumerations.OperatingSystem.android)
    #    kill()
    #    return
        
        
# end class ADBShellConnection

class ADBShellBlockingConnection(ADBShellConnection):
    def __init__(self, *args, **kwargs):
        super(ADBShellBlockingConnection, self).__init__(*args, **kwargs)
        self.command_prefix = "adb wait-for-device shell"
        self._unknown_command = None
        return

class ADBSSHConnection(SSHConnection):
    """
    An ADB Connection sends commands to the Android Debug Bridge
    """
    def __init__(self, serial_number=None,*args, **kwargs):
        """
        :param:

         - `serial_number`: An optional serial number to specify the device.
        """
        super(ADBSSHConnection, self).__init__(*args, **kwargs)
        self._logger = None
        self.command_prefix = "adb"
        if serial_number is not None:
            self.command_prefix += " -s " + serial_number
        self.operating_system = OperatingSystem.android
        return

    def _procedure_call(self, command, arguments="",
                        path='', timeout=10):
        """
        Overrides the SSHConnection._procedure_call to check for errors
        """
        output = self._main(command, arguments, path, timeout)
        return OutputError(ValidatingOutput(lines=output.output, validate=self.check_errors), output.error)


    def check_errors(self, line):
        """
        This is here so that children can override it.
        :param:

         - `line`: a line of output
        """
        self._check_errors(line)
        return
    
    def _check_errors(self, line):
        """
        Checks connection-related errors

        :raise: ConnectionError if the device isn't detected
        :raise: ConnectionWarning if the device isn't rooted
        """
        if line.startswith(DEVICE_NOT_FOUND):
            self.logger.debug(line)
            raise ConnectionError(line)
        elif line.startswith(DEVICE_NOT_ROOTED):
            self.logger.debug(line)
            raise ConnectionWarning(line)
        return
# end class ADBSSHConnection

class ADBShellSSHConnection(ADBSSHConnection):
    """
    A class to talk to the shell, note the adb-server
    """
    def __init__(self, *args, **kwargs):
        """
        :param: (see the ADBSSHConnection)
        """
        super(ADBShellSSHConnection, self).__init__(*args, **kwargs)
        self.command_prefix += " shell "
        return

    def check_errors(self, line):
        """
        :line: line of standard output

        :raise: CommandError if the command issued wasn't recognized
        """
        self._check_errors(line)
        if line.rstrip().endswith(NOT_FOUND):
            raise CommandError(line)                                  
        return
# end class ADBSHellSSHConnection
    
if __name__ == "__main__":
    from tottest.main import watcher
    import sys
    watcher()
    adb = ADBShellSSHConnection(hostname="localhost", username="allion")
    output, error= adb.iw('wlan0 link', timeout=1)
    for line in output:
        sys.stdout.write(line)
    
