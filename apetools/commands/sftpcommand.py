
from apetools.baseclass import BaseClass
from apetools.connections.sshconnection import SSHConnection


class SftpCommand(BaseClass):
    """
    An interface to the SftpCommand
    """
    def __init__(self, connection=None, hostname=None,
                 password=None, username=None, port=22, timeout=10):
        """
        Sftp Command Constructor

         * `connection` is the intended parameter, others are for building a connection if none given

        :param:

         - `connection`: An SSHConnection
         - `hostname`: address of remote host
         - `password`: password of remote host
         - `username: user login to remote host
         - `port`:  ssh server port number
         - `timeout`: login timeout
        """
        self._connection = None
        self.connection = connection
        self.hostname = hostname
        self.password = password
        self.username = username
        self.port = port
        self.timeout = timeout

        self._ssh = None
        self._sftp = None
        return

    @property
    def connection(self):
        """
        The SSHConnection
        """
        if self._connection is None:
            self._connection = SSHConnection(hostname=self.hostname,
                                             port=self.port,
                                             username=self.username,
                                             password=self.password)
        return self._connection

    @connection.setter
    def connection(self, connection):
        """
        Sets the SSH connection and resets the .ssh and .sftp attributes

        :param:

         - `connection`: A built SSHConnection

        :postcondition: self.ssh and self.sftp are None
        :postcondition: self.connection is connection
        """
        self._connection = connection
        self._ssh = None
        self._sftp = None        
        return

    @property
    def ssh(self):
        """
        The Paramiko client extracted from the connection.
        """
        if self._ssh is None:
            self._ssh = self.connection._client._client
        return self._ssh

    @property
    def sftp(self):
        """
        Sftp Client from the SSH client
        """
        if self._sftp is None:
            self._sftp = self.ssh.open_sftp()
        return self._sftp

    def close(self):
        """
        Closes the sftp connection (not the ssh connection)
        """
        self.sftp.close()
        return

    def getcwd(self):
        """
        Returns the remote current-working-directory
        """
        return self.sftp.getcwd()

    def listdir(self, path='.'):
        """
        Returns list of files
        """
        return self.sftp.listdir(path=path)

    def mkdir(self, path, mode=511):
        """
        Makes the directory on the remote host
        """
        return self.sftp.mkdir(path=path, mode=mode)

    def get(self, remote, local):
        """
        Get the remote file and put it in the local location

        :param:

         - `remote`: path to file on remote host
         - `local`: path to create file on local host
        """
        return self.sftp.get(remotepath=remote, localpath=local)

    def put(self, local, remote):
        """
        Put the local file on the remote host

        :param:

         - `local`: path to a local file
         - `remote`: path to put file on remote host
        """
        return self.sftp.put(localpath=local, remotepath=remote)
        


#python standard library
import unittest

#third party
from mock import MagicMock, patch


class TestSftpCommand(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = SftpCommand(connection=self.connection)
        self.sftp = MagicMock()
        self.ssh = MagicMock()
        return

    def test_ssh(self):
        """
        Does the ssh property return the paramiko client?
        """
        client = MagicMock()
        self.connection._client._client = client
        self.assertEqual(self.command.ssh, client)
        return

    def test_sftp(self):
        """
        Does the sftp property return the output of an open_sftp() call?
        """
        self.command._ssh = self.ssh
        self.ssh.open_sftp.return_value = self.sftp
        self.assertEqual(self.command.sftp, self.sftp)
        return

    def test_close(self):
        """
        Does close() call on the sftp-client's close?
        """
        self.command._sftp = self.sftp
        self.command.close()
        self.sftp.close.assert_called_with()
        return

    def test_getcwd(self):
        """
        Does the getcwd call return the output of the sftp getcwd()?
        """
        expected = 'right here'
        self.command._sftp = self.sftp        
        self.sftp.getcwd.return_value = expected
        cwd = self.command.getcwd()
        self.assertEqual(expected, cwd)
        return

    def test_listdir(self):
        """
        Does the listdir method call the sftp method and return its output?
        """
        filenames = 'a b c d e'.split()
        path = '/home/land'
        self.command._sftp = self.sftp
        self.sftp.listdir.return_value = filenames
        outcome = self.command.listdir(path=path)
        self.assertEqual(outcome, filenames)
        self.sftp.listdir.assert_called_with(path=path)
        return

    def test_mkdir(self):
        """
        Does the `mkdir` properly call the sftp `mkdir`?
        """
        self.command._sftp = self.sftp
        path = 'here'
        mode = 420
        self.command.mkdir(path=path, mode=mode)
        self.sftp.mkdir.assert_called_with(path=path, mode=mode)
        return

    def test_get(self):
        """
        Does the get call the sftp-get?
        """
        source = '/home/test.iperf'
        target = 'test.iperf'
        self.command._sftp = self.sftp
        self.command.get(remote=source, local=target)
        self.sftp.get.assert_called_with(remotepath=source, localpath=target)
        return

    def test_put(self):
        """
        Does the `put` method call the sftp `put` method?
        """
        source = 'here'
        target = 'there'
        self.command._sftp = self.sftp
        self.command.put(local=source, remote=target)
        self.sftp.put.assert_called_with(localpath=source, remotepath=target)
        return

    def test_connection_builder(self):
        """
        Does the sftp create an SSHConnection if given the right parameters?
        """
        connection = MagicMock()
        def fake_init(self, hostname, username, password, port=None):
            self.hostname=hostname
            self.username=username
            self.password=password
            self.port=port
            self._connection=None
            return
        with patch('apetools.commands.sftpcommand.SftpCommand.__init__', new=fake_init):
            command = SftpCommand(hostname='a', username='b', password='c', port=52686)
            connection = command.connection
            self.assertEqual(connection.hostname, 'a')
            self.assertEqual(connection.username, 'b')
            self.assertEqual(connection.password, 'c')
            self.assertEqual(connection.port, 52686)
            self.assertIsInstance(connection, SSHConnection)
        return

    def test_connection_setter(self):
        """
        Does setting the connection re-set the sftp and ssh?
        """
        self.command._ssh = self.ssh
        self.command._sftp = self.sftp

        self.assertEqual(self.command.ssh, self.ssh)
        self.assertEqual(self.command.sftp, self.sftp)        
        
        connection = MagicMock()
        self.command.connection = connection
        self.assertEqual(self.command.connection, connection)
        self.assertIsNone(self.command._ssh)
        self.assertIsNone(self.command._sftp)
        return
