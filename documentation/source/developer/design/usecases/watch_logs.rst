Watch Logs Use Case
===================

The LogWatcher opens a connection to a device and consumer the log stream from the device, sending it to storage.

.. uml::

   left to right direction
   Ape --> (Request Log's Output Be Captured)

Related Requirements
--------------------

|A13|

Preconditions
-------------

* Configuration specifies path to the log source 
* DUT is connected to the CPC via ADB
* If required, DUT is rooted

Postconditions
--------------

* Log output redirected to specified storage.

Failed End Condition
--------------------

* No, partial, or corrupted log output is saved.

Trigger
-------

* TestOperator has started session.

Main Path
---------

#. The log watcher is started in a thread.
#. The watcher cats the specified file (PATH)
#. The watcher sends each line to the specified output as it's produced by the log.

Extension Paths
----------------

2.1. The watcher detects a permission error
2.1.1 The watcher emits an error
2.1.2. The watcher dies

2.2. The watcher detects a path error
2.2.1. The watcher emits an error
2.2.2. The watcher dies

.. uml::

   (*) --> "Acquire Lock"
   "Acquire Lock" --> "Cat File"
   "Cat File" --> "Release Lock"
   "Release Lock" --> "Read Line"
   "Read Line" --> [line] "Write to Output"
   "Write to Output" --> "Read Line"
   if "Detect Error" then
      --> "Emit Error"
   "Emit Error" --> "Kill Self"
   "Kill Self" --> (*)


ADB Device Static Model
-----------------------

.. uml::

   LogWatcher: String Path
   LogWatcher: Connection connection
   LogWatcher: Output output
   LogWatcher: RLock lock
   LogWatcher: run()
   LogWatcher: start()
   LogWatcher <|-- ADBShellConnection

   ADBShellConnection: LocalConnection connection


.. include:: ../requirements_source.rst
