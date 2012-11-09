Cleanup Session Use Case
========================

The Cleanup Session Use Case is an included use case within the `Test Throughput` use case.

.. uml::

   left to right direction
   skinparam packageStyle rect   

   actor APE

   APE -> (Test Throughput) 
   package TestSession {
   (Test Throughput) ..> (Setup Session) : <<include>>
   (Test Throughput) ..> (Run Test) : <<include>>
   (Test Throughput) ..> (Cleanup Session) : <<include>>
   }

Related Requirements
--------------------

* |A9|
* |A10|

Preconditions
-------------

* Test has completed
* Data folder specified in configuration

Postcondition
-------------

Copies of configuration file and log are in data folder.

Failed End Condition
--------------------

File and log not copied to data folder.

Trigger
-------

The |APE| has requested a throughput test be run.

Main Path
---------

#. Copy log file to data folder.
#. Copy configuration file to data folder.

Alternate Paths
---------------

1.1 The log file fails to be copied.

   1.1.1. A `ConfigurationError` is raised.

2.1. The configuration file fails to be copied.

   2.1.1. A `ConfigurationError` is raised.
   

.. include:: ../requirements_source.rst
