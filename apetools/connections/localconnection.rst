Local Connection
================

a module to hold a local connection.

The LocalConnection takes the command-line command as a property and
the arguments to the command as parameters.

e.g. ::

    lc = LocalConnection()
    output = lc.ls('-l')
    print output.output

prints the output of the `ls -l` command line command

This is using subprocess so anything with lots of iperf runs the risk of
causing the output to block (i.e. it is file-buffered, not line or character buffered).

In most cases it's better to use the LocalNixConnection instead which uses Pexpect to avoid the block.

.. '

::

    SPACER = '{0} {1} '
    UNKNOWN = "Unknown command: "
    EOF = ''
    SPACE = " "
    
    OutputError = namedtuple("OutputError", 'output error')
    
    



LocalConnection
---------------

.. uml::

   BaseClass <|-- LocalConnection

.. module:: apetools.connections.localconnection
.. autosummary::
   :toctree: api

   LocalConnection
   LocalConnection.queue
   LocalConnection._procedure_call
   LocalConnection._main
   LocalConnection.__getattr__
   


LocalNixConnection
------------------

Uses `pexpect` instead of sub-process.

.. uml::

   LocalConnection <|-- LocalNixConnection

.. autosummary::
   :toctree: api

   LocalNixConnection
   LocalNixConnection.run

