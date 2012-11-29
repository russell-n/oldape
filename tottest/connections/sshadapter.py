"""
An alternate client using Paramiko's SSHClient
"""

# python libraries
import socket

# third-party libraries
import paramiko

#tottest libraries
from tottest.baseclass import BaseClass
from tottest.commons import errors

ConnectionError = errors.ConnectionError
DOT_JOIN = "{0}.{1}"
NEWLINE = "\n"


class SSHClient(paramiko.SSHClient):
    """
    Subclasses paramiko's SSHClient to add a timeout.
    """
    def exec_command(self, command, timeout=None, bufsize=-1, combine_stderr=False):
        """
        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.
         - `combine_stderr`: Sets the paramiko flag so there's only one stream

        :rtype: tuple
        :return: stdin, stdout, stderr
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.exec_command(command)
        stdin = channel.makefile('wb', bufsize)
        stdout = channel.makefile('rb', bufsize)
        if combine_stderr:
            channel.set_combine_stderr(combine_stderr)
            stderr = stdout
        else:
            stderr = channel.makefile_stderr('rb', bufsize)
        return stdin, stdout, stderr

    def invoke_shell(self, term='vt100', width=80, height=24, timeout=None, bufsize=-1):
        """
        :param:

         - `term`: Terminal to emulate.
         - `width`: Screen width
         - `height`: Screen Height.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.

        :rtype: tuple
        :return: stdin, stdout, stderr
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.get_pty(term, width, height)
        channel.invoke_shell()
        stdin = channel.makefile('wb', bufsize)
        stdout = channel.makefile('rb', bufsize)
        stderr = channel.makefile_stderr('rb', bufsize)
        return stdin, stdout, stderr

    def invoke_shell_rw(self, term='vt100', width=80, height=24, timeout=None, bufsize=-1):
        """
        :param:

         - `term`: Terminal to emulate.
         - `width`: Screen width
         - `height`: Screen Height.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.

        :rtype: tuple
        :return: i/o
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.set_combine_stderr(True)
        channel.get_pty(term, width, height)
        channel.invoke_shell()

        shell = channel.makefile('r+b', bufsize)

        return shell

#end class SSHClient

class SimpleClient(BaseClass):
    """
    A simple wrapper around paramiko's SSHClient.

    The only intended public interface is exec_command.
    """
    def __init__(self, hostname, username, password=None, port=22, timeout=5):
        """
        :param:

         - `hostname`: ip address or resolvable hostname.
         - `username`: the login name.
         - `password`: optional if ssh-keys are set up.
         - `port`: The port for the ssh process.
         - `timeout`: Time to give the client to connect
        """
        super(SimpleClient, self).__init__()
        self._logger = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self._client = None
        return

    def exec_command(self, command, timeout=10):
        """
        A pass-through to the SSHClient's exec_command.

        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.

        :rtype: tuple
        :return: stdin, stdout, stderr

        :raise: ConnectionError for paramiko or socket exceptions
        """
        if not command.endswith(NEWLINE):
            command += NEWLINE
        try:
            return self.client.exec_command(command, timeout)

        except paramiko.SSHException as error:
            self._client = None
            self.logger.error(error)
            raise ConnectionError("There is a problem with the ssh-connection to:\n {0}".format(self))
        except paramiko.PasswordRequiredException as error:
            self.logger.error(error)
            self.logger.error("Private Keys Not Set Up, Password Required.")
            raise ConnectionError("SSH Key Error :\n {0}".format(self))
        except socket.error as error:
            self.logger.error(error)
            if 'Connection refused' in error: 
                raise ConnectionError("SSH Server Not responding: check setup:\n {0}".format(self))
            raise ConnectionError("Problem with:\n {0}".format(self))
        return
        
    @property
    def client(self):
        """
        :rtype: paramiko.SSHClient
        :return: An instance of SSHClient connected to remote host.
        :raise: ClientError if the connection fails.
        """
        if self._client is None:
            self._client = SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.load_system_host_keys()
            try:
                self._client.connect(hostname=self.hostname,
                                     port=self.port,
                                     username=self.username,
                                     password=self.password,
                                     timeout=self.timeout)
            except paramiko.AuthenticationException as error:
                self.logger.error(error)
                raise ConnectionError("There is a problem with the ssh-keys or password for \n{0}".format(self))
            except socket.timeout as error:
                self.logger.error(error)
                raise ConnectionError("Paramiko is unable to connect to \n{0}".format(self))
        return self._client

    def __str__(self):
        """
        :return: username, hostname, port, password in string
        """
        user = "Username: {0}".format(self.username)
        host = "Hostname: {0}".format(self.hostname)
        port = "Port: {0}".format(self.port)
        password = "Password: {0}".format(self.password)
        return NEWLINE.join([user, host, port, password])

    def close(self):
        """
        :postcondition: client's connection is closed
        """
        self.client.close()
        return
# class SimpleClient
    
