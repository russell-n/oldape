The Ping Command
================

A Ping command pings and checks the response.

.. currentmodule:: apetools.commands.ping



The PingData
------------

The `PingData` class is a namedtuple that holds the address that was pinged and the round-trip time for the ping.

.. autosummary::
   :toctree: api

   PingData

.. uml::

   PingData -|> collections.namedtuple
   PingData : target
   PingData : rtt
   PingData : __str__()


                   
PingArguments
-------------

The `PingArguments` class holds string constants for the ping-command.

.. uml::

   PingArguments : arguments

The keys to the `arguments` dictionary are the values in `apetools.commons.enumerations.OperatingSystem`.

Example Use::

   ping_args = PingArguments.arguments['android']  + '192.168.10.12'



The PingCommand
---------------

The `PingCommand` issues the ping command and checks the outcome

.. autosummary::
   :toctree: api

   PingCommand

.. uml::

   PingCommand



Example Use::

    ping = PingCommand('192.168.20.1')
    print str(ping.run())

    connection = SSHConnection('192.168.10.23', 'tester')
    target = "192.168.30.1"
    print str(ping(target, connection))
