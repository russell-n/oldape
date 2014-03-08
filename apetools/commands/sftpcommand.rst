The SFTP Command
================

Since the paramiko :ref:`SSHClient <ssh-client>` is somewhat buried within the :ref:`SSHConnection <ssh-connection>` this class was created to hide the need to pull it out and work with it directly. It is a convenience class to create the `SFTPClient` from the connection and only provides a sub-set of the client commands, the rest if desired would need to be passed to the client itself.

.. currentmodule:: apetools.commands.sftpcommand

.. autosummary::
   :toctree: api

   SftpCommand

.. uml::

   SftpCommand -|> BaseClass
   SftpCommand o-- SSHConnection 
   SftpCommand o-- SSHClient
   SftpCommand o-- paramiko.SftpClient 
   SftpCommand : SSHConnection connection
   SftpCommand : SSHClient ssh
   SftpCommand : SftpClient sftp
   SftpCommand : __init__(connection)
   SftpCommand : close()
   SftpCommand : getcwd()
   SftpCommand : listdir(path)
   SftpCommand : mkdir(path, mode)
   SftpCommand : get(remote, local)
   SftpCommand : put(local, remote)



Example Use::

   connection = SSHConnection(hostname='192.168.10.24', username='tester')
   sftp = SftpCommand(connection=connection)
   sftp.get('data.txt', 'remote_data.txt')

Testing the SftpCommand
-----------------------

.. autosummary::
   :toctree: api

   TestSftpCommand.test_ssh
   TestSftpCommand.test_sftp
   TestSftpCommand.test_close
   TestSftpCommand.test_getcwd
   TestSftpCommand.test_listdir
   TestSftpCommand.test_mkdir
   TestSftpCommand.test_get
   TestSftpCommand.test_put
   TestSftpCommand.test_connection_builder
   TestSftpCommand.test_connection_setter






