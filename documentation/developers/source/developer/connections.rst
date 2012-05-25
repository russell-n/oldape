Connection Classes
==================

LocalConnection
---------------

A LocalConnection takes a command as a procedure call and sends it to the local shell.

e.g. to get the local `iperf` help string (which gets sent to stderr)::

    lc = LocalConnection()
    outerr = lc.iperf('-h')
    print outerr.error

.. uml::

   LocalConnection: String command_prefix
   LocalConnection: <command>(String arguments, Float timeout)

When you use the command, if you leave the timeout as None (the default), the output will be file-buffered, but 
if you give it some kind of timeout, it will act line-buffered.

LocalNixConnection
------------------

A LocalNixConnection overrides the run() method in the LocalConnection to use pexpect instead of subprocess.


ADBConnection
-------------

An ADBConnection extends the LocalConnection to check for ADB connection errors.

.. uml::

   LocalConnection <|-- ADBConnection

   ADBConnection: String serial_number

**Raises:** `ConnectionError` if the device can't be connected to.

**Raises:** `ConnectionWarning` if you try to do something that doesn't work (like root an unrootable device).

ADBBlockingConnection
---------------------

The `ADBBlockingConnection` waits until the device comes online (so it will block forever).

.. uml::

   ADBConnection <|-- ADBBlockingConnection

ADBShellConnection
------------------

The `ADBShellConnection` passes the commands sent to the Android's shell.

.. uml::

   ADBConnection <|-- ADBShellConnection

**Raises:** `ConnectionError` if the command isn't known.

SL4AConnection
--------------

The `SL4AConnection` is android.Android but it raises a CommandError if SL4a returns an error. 

