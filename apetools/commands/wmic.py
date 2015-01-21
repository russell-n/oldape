
# python standard library
import re

# this package
from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError
from apetools.parsers import oatbran


NEWLINE = "\n"


class WmicEnumeration(object):
    __slots__ = ()
    code = "code"
# class WmicEnumeration


class WmicWin32NetworkAdapter(BaseClass):
    """
    Window's wmic win32_networkadapter command (wifi only).
    """
    def __init__(self, connection=None, enable_wifi_command="enable",
                 disable_wifi_command="disable",
                 command_base="path Win32_NetworkAdapter where NetConnectionID='\"{i}\"' call {{c}}",
                 interface_name = "Wireless Network Connection",
                 passing_code="0"):
        """
        :param:

         - `connection`: a connection to the device (creates `ADBShellConnection` if not given)
         - `enable_wifi_command`: command to send to svc to enable radio
         - `disable_wifi_command`: command to send to svc to disable radio
         - `command_base`: the call command to add enable or disable to before sending to wmic
         - `interface_name`: The Name of the wireless interface
        """
        super(WmicWin32NetworkAdapter, self).__init__()
        self.connection = connection
        self.enable_wifi_command = enable_wifi_command
        self.disable_wifi_command = disable_wifi_command
        self.command_base = command_base
        self.interface_name = interface_name
        self.passing_code = passing_code
        self._return_expression = None
        self._base_command = None
        return

    @property
    def base_command(self):
        """
        :return: command-strisg without enable/disable
        """
        if self._base_command is None:
            self._base_command = self.command_base.format(i=self.interface_name)
        return self._base_command

    @property
    def return_expression(self):
        """
        :return: compiled regular expression to check the return code        
        """
        if self._return_expression is None:
            expression = (oatbran.SPACES + "ReturnValue" + oatbran.SPACES + "=" + oatbran.SPACES +
                          oatbran.NAMED(n=WmicEnumeration.code, e=oatbran.DIGIT))
            self._return_expression = re.compile(expression)
        return self._return_expression

    def enable_wifi(self):
        """
        Enable the WiFi radio
        """
        self.call_wmic(self.enable_wifi_command)
        return

    def disable_wifi(self):
        """
        Disable the wifi radio
        """
        self.call_wmic(self.disable_wifi_command)
        return

    def call_wmic(self, command):
        """
        :param:

         - `command`: the command to add to the command_base
        """
        output = self.connection.wmic(self.base_command.format(c=command))
        self.validate(output.output, command)
        return
        

    def validate(self, output, subcommand):
        """
        :raise: CommandError if there is an error in the output
        """
        for line in output:
            match = self.return_expression.search(line)
            if match and match.groupdict()[WmicEnumeration.code] != self.passing_code:
                self.logger.error(line)
                raise CommandError("Wmic was unable to change the state of the wireless interface: '{0}'".format(line))
            elif "No Instance(s) Available." in line:
                self.logger.error(line)
                raise CommandError("Unknown Interface: {0}".format(self.interface_name))
            elif "ReturnValue = 0;" in line:
                self.logger.info("WMIC command succesful.")
                return
            self.logger.debug(line.rstrip(NEWLINE))
            
        return
# end class WmicWin32NetworkAdapter
