Setup Iperf Test Use Case
=========================

.. uml::

   left to right direction

   skinparam packageStyle rect
   APE -> (Test Throughput)

   package TestSession {
   (Test Throughput) ..> (Setup Session) : <<include>>
   (Test Throughput) ..> (Run Test) : <<include>>
   (Test Throughput) ..> (Cleanup Session) : <<include>>
   }
   (Run Test) ..> (Setup Iperf Test) : <<include>>


Related Requirements
--------------------

* |A3| 
* |A4|
* |A5|

Preconditions
-------------

* The |CPC| is connected to the DUT and communicating via ADB
* The |TPC| has a running SSH Server
* CPC and TPC are on the same subnet

Postcondition
-------------

DUT and TPC have no running `iperf` processes.

Trigger
-------

|APE| requests throughput test. 

Main Path
---------

#. The system establishes connection to DUT and TPC
#. The system kills all existing `iperf` processes on the TPC and DUT.

Alternate Paths
---------------

2.1. The system is unable to connect to the DUT or TPC.

   2.1.1. A `ConnectionError` or `ConfigurationError` is raised based on cause.
   2.1.2. The test exits.

3.1. Running `iperf` processes remain on the DUT or TPC.

   3.1.1. A `CommandError` is raised.
   3.1.2. The test exits.

.. include:: ../requirements_source.rst
