The ConnectionBuilder
=====================

A module to build the connections.

* Each expects only a `parameters` named-tuple on initiation.

* Each has a connection parameter

.. module:: apetools.builders.subbuilders.connectionbuilder
   


SSHParameters
-------------

This is a named-tuple to pass parameters to the ssh-connection.

.. autosummary::
   :toctree: api

   SSHParameters

.. uml::

   SSHParameters -|> namedtuple
   SSHParameters : hostname
   SSHParameters : username
   SSHParameters : password
   


.. _connection-builder-base:

ConnectionBuilderBase
---------------------

A base class for connection builders.

.. autosummary::
   :toctree: api

   ConnectionBuilderBase

.. uml::

   ConnectionBuilderBase -|> BaseClass
   ConnectionBuilderBase : abstractproperty connection



DummyConnectionBuilder
----------------------

This is for the odd cases where we need a fake connection that does not actually connect to anything. In particular this was created for the screen-iperf-hack for iPads.

.. autosummary::
   :toctree: api

   DummyConnectionBuilder

.. uml::

   DummyConnectionBuilder -|> ConnectionBuilderBase



AdbShellConnectionBuilder
-------------------------

A builder for a :ref:`local adb-shell connection <adb-shell-connection>`. In this case the connection is a sub-process of the computer running the APE (it is assumed that the android is directly connected to the PC via an ADB USB bridge) so it doesn't use the parameters, but to make the signatures the same across the builders, something is expected (even if it's just None) on construction.

.. autosummary::
   :toctree: api
   
   AdbShellConnectionBuilder
   

.. uml::

   AdbShellConnectionBuilder -|> BaseClass
   AdbShellConnectionBuilder : ADBShellConnection connection
   


SSHConnectionBuilder
--------------------

A Builder of :ref:`SSHConnections <ssh-connection>`.

.. autosummary::
   :toctree: api

   SSHConnectionBuilder

.. uml::

   SSHConnectionBuilder -|> BaseClass
   SSHConnectionBuilder : SSHConnection connection



AdbShellSshConnectionBuilder
----------------------------

A builder of :ref:`remote (SSH-based) connections <adb-shell-ssh-connection>` for an ADB shell.

.. autosummary::
   :toctree: api

   AdbShellSshConnectionBuilder

.. uml::

   AdbShellSshConnectionBuilder -|> SSHConnectionBuilder
   AdbShellSshConnectionBuilder : ADBShellSSHConnection Connection



ConnectionBuilderTypes
----------------------

A holder of string constants for the types of connections that can be built.

.. uml::

   ConnectionBuilderTypes : ssh
   ConnectionBuilderTypes : adbshellssh
   ConnectionBuilderTypes : adbshell
   


ConnectionBuilders
------------------

The connection builders can be retrieved by a dictionary named `connection_builders`.

For example, to retrieve an SSHConnection from this module (connectionbuilder)::

    from connectionbuilder import connection_builders, ConnectionBuilderTypes, SSHParameters
    ssh_builder = connection_builders[ConnectionBuilderTypes.ssh]
    parameters = SSHParameters(hostname='192.168.10.24', username='allion')
    ssh_builder(parameters)
    ssh_connection = ssh_builder.connection

.. note:: The import here assumes you are in the same working directly, a more realistic one would use the package path.

.. csv-table:: connection_builders
   :header: key, value
   
   ConnectionBuilderTypes.adbshell, AdbShellConnectionBuilder
   ConnectionBuilderTypes.adbshellssh, AdbShellSshConnectionBuilder
   ConnectionBuilderTypes.ssh,SSHConnectionBuilder
   ConnectionBuilderTypes.dummy, DummyConnection
   


Testing the Builders
--------------------

.. autosummary::
   :toctree: api

   TestConnectionBuilders.test_valid_keys
   TestDummyConnectionBuilder.test_connection
   TestConnectionBuilderBase.test_parameters
   TestConnectionBuilderBase.test_no_connection




