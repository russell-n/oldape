The ADB Connections
===================


An ADB connection sends commands to a local ADB Connection and interprets errors



Errors
------

The ADBConnections raise two types of errors and a warning if predictable but incorrect behavior is detected.

.. currentmodule:: apetools.connections.adbconnection
.. autosummary::
   :toctree: api

   ADBConnectionError
   ADBCommandError
   ADBConnectionWarning

.. uml::

   ADBConnectionError -|> ConnectionError

.. uml::   
   ADBCommandError -|> CommandError

.. uml::   
   ADBConnectionWarning -|> ConnectionWarning
   


.. _adb-connection:

ADBConnection
-------------

Creates a local connection to the device over ADB. This differs from the :ref:`ADBShellConnection <adb-shell-connection>` in that it talks to the server, not to the shell on the device. It would be used, for instance, when pushing files to the device.

.. autosummary::
   :toctree: api

   ADBConnection

.. uml::

   ADBConnection -|> LocalNixConnection
   ADBConnection : serial_number



.. _adb-blocking-connection

ADBBlockingConnection
---------------------

This is the same as the :ref:`ADBConnection <adb-connection>` but will wait for the ADB server if it is not on-line yet. It was created for the somewhat obscure case where the device is rebooted.

.. autosummary::
   :toctree: api

   ADBBlockingConnection

.. uml::

   ADBBlockingConnection -|> ADBConnection



ADBShellConnection
------------------

This creates a local connection to talk to the shell on an android over ADB.

.. autosummary::
   :toctree: api

   ADBShellConnection

.. uml::

   ADBShellConnection -|> ADBConnection



ADBShellBlockingConnection
--------------------------

This is like the :ref:`ADBBlockingConnection <adb-blocking-connection>` except that waits until the ADB server is online then issues commands to the shell.

.. autosummary::
   :toctree: api

   ADBShellBlockingConnection

.. uml::

   ADBShellBlockingConnection -|> ADBShellConnection



ADBSSHConnection
----------------

Connects to the remote PC connected to the Android and issues ADB commands (this should be preferred to the :ref:`ADBConnection <adb-connection>`).

.. autosummary::
   :toctree: api

.. uml::

   ADBSSHConnection -|> SSHConnection
   ADBSSHConnection : serial_number

   


ADBShellSSHConnection
---------------------

Issues ADB-shell commands to a remote PC (via SSH) which is connected to the Android via ADB. This should be preferred to :ref:`ADBShellConnection <adb-shell-connection>`.

.. autosummary::
   :toctree: 1

   ADBShellSSHConnection

.. uml::

   ADBShellSSHConnection -|> ADBSSHConnection



A Usage Example
---------------

::

    if __name__ == "__main__":
        from apetools.main import watcher
        import sys
        watcher()
        adb = ADBShellSSHConnection(hostname="lancet", username="allion")
        output, error= adb.iw('wlan0 link', timeout=1)
        for line in output:
            sys.stdout.write(line)
        
    

