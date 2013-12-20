The Non-Local Connection
========================

The Non-Local Connection is a Base for non-local connectionS (e.g. SSH or Telnet).

Calls to a NonLocalConnection takes the command-line command as a property and the arguments to the command as parameters.

.. currentmodule:: apetools.connections.nonlocalconnection
.. autosummary::
   :toctree:

   NonLocalConnection
   DummyConnection



.. _non-local-connection:

The NonLocalConnection
----------------------

.. uml::

   NonLocalConnection -|> BaseThreadClass
   NonLocalConnection : lock
   NonLocalConnection o-- threading.RLock
   NonLocalConnection o-- Queue.Queue
   NonLocalConnection : __getattr__(command)
   NonLocalConnection : __call__(command, arguments)



The DummyConnection
-------------------

.. uml::

   DummyConnection -|> NonLocalConnection
   DummyConnection -|> hostname



Testing the DummyConnection
---------------------------

.. autosummary::
   :toctree: api

   TestDummyConnection.test_constructor
   TestDummyConnection.test_call
   TestDummyConnection.test_dot_notation




