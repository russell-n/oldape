The SSHConnection
=================

Encapsulates the Paramiko `SSHClient <http://www.lag.net/paramiko/docs/paramiko.SSHClient-class.html>`_ to provide a common interface with the other connection types.

Contents:

    * :ref:`SSHClient <ssh-client>`
    * :ref:`SimpleClient <simple-client>`
    * :ref:`SSHConnection <ssh-connection>`
    * :ref:`OutputFile <output-file>`

.. currentmodule:: apetools.connections.sshconnection
   


.. _ssh-client:

SSHClient
---------

This is an extension of paramiko.SSHClient that adds a timeout to the output read attempts. It can be used transparently the same way the paramiko SSHClient is used or with the added ``timeout`` parameter.

.. currentmodule:: apetools.connections.sshconnection
.. autosummary::
   :toctree: api
   
   SSHClient
   SSHClient.exec_command
   SSHClient.invoke_shell
   SSHClient.invoke_shell_rw

.. uml::

   SSHClient -|> paramiko.SSHClient
   SSHClient : exec_command(command, timeout, bufsize, combine_stderr)
   SSHClient : invoke_shell(term, width, Height, timeout, bufsize)
   SSHClient : invoke_shell_rw(term, width, Height, timeout, bufsize)
   


.. _simple-client:

SimpleClient
------------

This is a wrapper around the :ref:`SSHClient <ssh-client>` that sets some flags to avoid host-key errors. The following are (roughly) equivalent.

SSHClient::

   c = SSHClient()
   c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   c.load_system_host_keys()
   c.connect(hostname='192.168.10.24', username='allion')
   stdin, stdout, stderror = c.exec_command('ls')

SimpleClient::

   c = SimpleClient(hostname='192.168.10.24', username='allion')
   stdin, stdout, stderr = c.exec_command('ls')

.. currentmodule:: apetools.connections.sshconnection   
.. autosummary::
   :toctree: api

   SimpleClient
   SimpleClient.exec_command
   SimpleClient.__str__
   SimpleClient.close

.. uml::

   SimpleClient -|> BaseClass
   SimpleClient o-- SSHClient
   SimpleClient : client
   SimpleClient : hostname
   SimpleClient : username
   SimpleClient : password
   SimpleClient : port
   SimpleClient : timeout
   SimpleClient : exec_command(command, timeout)
   SimpleClient : __str__()
   SimpleClient : close()




.. _ssh-connection:

The SSHConnection
-----------------

This class uses the :ref:`SimpleClient <simple-client>` to implement the :ref:`NonLocalConnection <non-local-connection>` interface.

.. currentmodule:: apetools.connections.sshconnection
.. autosummary::
   :toctree: api

   SSHConnection

.. uml::

   SSHConnection -|> NonLocalConnection
   SSHConnection o-- SimpleClient
   SSHConnection : hostname
   SSHConnection : username
   SSHConnection : password
   SSHConnection : port
   SSHConnection : timeout

SimpleClient Example::

   connection = SimpleClient(hostname='192.168.10.24', username='allion')
   stdin, output, error = connection.exec_command('ls -l')
   for line in output:
       print line

   for line in error:
       print line
   
Equivalent SSHConnection Example::
         
    connection = SSHConnection(username="allion", hostname="192.168.10.24")
    output, error = connection.ls('-l')
    for line in output:
        print line

    for line in output:
        print line




.. _output-file:

OutputFile
----------

This acts as a file-like object that traps socket timeouts so that users do not have to know that it contains a networked connection. To prevent blocking the socket-timeout causes it to return a SPACE. 

.. autosummary::
   :toctree: api

   OutputFile

.. uml::

   OutputFile -|> ValidatingOutput
   OutputFile : readline(timeout)



Another Example
---------------

::

    if __name__ == "__main__":
        c = SSHConnection('igor', 'developer')
        o = c.wmic('path win32_networkadapter where netconnectionid="\'Wireless Network Connection\'" call enable')
        for index, line in enumerate(o.output):
            print index, line
    

