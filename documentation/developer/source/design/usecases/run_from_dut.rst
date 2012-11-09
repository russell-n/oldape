Run Traffic From Dut
====================

.. uml::

   left to right direction

   actor APE

   skinparam packageStyle rect

   package RunTest{
   APE -> (Test Throughput From DUT)
   (Test Throughput From DUT) ..> (Run Test) : <<include>>
   } 
   package RunIperfTraffic{
   (Run Traffic From DUT) --|> (Run Test)
   }

Related Requirements
--------------------

* |A7|
* |A8|

Preconditions
-------------

* The |DUT| is connected to the |AP|
* The DUT and |TPC| are on the same subnet
* TPC and DUT have `iperf` installed on their `PATH`

Postcondition
-------------

The data from the `iperf` Session is stored in Files.

Failed End Condition
--------------------

No, partial, or corrupted data has been saved for the DUT.

Trigger
-------

|APE| requests `iperf` to DUT test.

Main Path
---------

#. System starts an `iperf` server on the TPC.
#. System waits for the server to start.
#. System imples the TPC to send traffic to the DUT.
#. System saves the standard output of the DUT and TPC as it is generated during test.

Alternate Paths
---------------

2.1. System is unable to start the `iperf` server.

   2.1.1. `CommandError` or `ConnectionError` is rased based on cause.

   2.1.2. The test exits.

4.1. System is unable to impel the DUT to send traffic.

   4.1.1. A `CommandError`, `ConfigurationError`, or `ConnectionError` is raised based on cause.

   4.1.2 The test exits.

.. include:: ../requirements_source.rst

