===============
 ADBConnection
===============

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
