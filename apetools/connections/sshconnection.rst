The SSHConnection
=================

Encapsulates the Paramiko `SSHClient <http://www.lag.net/paramiko/docs/paramiko.SSHClient-class.html>`_ to provide a common interface with the other connection types.

Example Use::
         
    connection = SSHConnection("allion","192.168.10.24")
    output = connection.ls('-l')
    for line in output.output:
        print line

    for line in output.error:
        print line

* prints the output of the `ls -l` command line command

.. currentmodule:: apetools.connections.sshconnection
.. autosummary::
   :toctree: api

   SSHConnection
   SimpleClient
   SSHClient
   OutputFile

   
.. uml::

   SSHConnection -|> NonLocalConnection
   SSHConnection o-- SimpleClient
   SSHConnection : hostname
   SSHConnection : username
   SSHConnection : password
   SSHConnection : port
   SSHConnection : timeout

.. uml::

   SSHClient -|> paramiko.SSHClient
   SSHClient : exec_command(command, timeout, bufsize, combine_stderr)
   SSHClient : invoke_shell(term, width, Height, timeout, bufsize)
   SSHClient : invoke_shell_rw(term, width, Height, timeout, bufsize)

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
    

