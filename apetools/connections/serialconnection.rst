Serial Connection
=================

A module to hold a serial connection.

The SerialConnection takes the command-line command as a property and
the arguments to the command as parameters.

e.g. ::

    sc = SerialConnection()
    output = sc.ls('-l')
    print output.output

prints the output of the `ls -l` command line command



.. uml::

   LocalConnection <|-- SerialConnection

.. module:: apetools.connections.serialconnection
.. autosummary::
   :toctree: api

   SerialConnection
   SerialConnection.client
   SerialConnection.set_timeout
   SerialConnection._procedure_call

