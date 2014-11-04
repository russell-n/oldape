Telnet Connection
=================

A module to hold an Telnet connection.

The TelnetConnection takes the command-line command as a property and the arguments to the command as parameters.

e.g. ::

    sc = TelnetConnection()
    output = sc.ls('-l')
    print output.output

prints the output of the `ls -l` command line command



.. uml::

   NonLocalConnection <|-- TelnetConnection
   TelnetConnection o- TelnetAdapter

.. module:: apetools.connections.telnetconnection
.. autosummary::
   :toctree: api

   TelnetConnection
   TelnetConnection.client
   TelnetConnection._procedure_call
   TelnetConnection.validate

