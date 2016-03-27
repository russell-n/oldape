The Non-Local Connection
========================

The Non-Local Connection is a Base for non-local connectionS (e.g. SSH or Telnet).

Calls to a NonLocalConnection takes the command-line command as a property and the arguments to the command as parameters.

.. currentmodule:: apetools.connections.nonlocalconnection
.. autosummary::
   :toctree: api

   NonLocalConnection
   DummyConnection


.. code::

    <class 'ImportError'>
    No module named 'StringIO'
    






.. _non-local-connection:

The NonLocalConnection
----------------------

.. uml::

   NonLocalConnection -|> BaseThreadClass
   NonLocalConnection : command_prefix
   NonLocalConnection : operating_system
   NonLocalConnection: path
   NonLocalConnection : library_path
   NonLocalConnection : lock
   NonLocalConnection o-- threading.RLock
   NonLocalConnection o-- Queue.Queue
   NonLocalConnection : __getattr__(command)
   NonLocalConnection : __call__(command, arguments)


.. code::

    <class 'NameError'>
    name 'BaseThreadClass' is not defined
    



The DummyConnection
-------------------

.. uml::

   DummyConnection -|> NonLocalConnection
   DummyConnection -|> hostname


.. code::

    <class 'NameError'>
    name 'NonLocalConnection' is not defined
    



Testing the DummyConnection
---------------------------

.. autosummary::
   :toctree: api

   TestDummyConnection.test_constructor
   TestDummyConnection.test_call
   TestDummyConnection.test_dot_notation


.. code::

    <class 'ImportError'>
    No module named 'mock'
    







