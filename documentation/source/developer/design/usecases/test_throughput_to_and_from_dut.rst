Test Throughput To and From DUT Use Case
========================================

.. uml::

   left to right direction

   actor APE

   skinparam packageStyle rect

   package RunTest{
   APE -> (Test Throughput To and From DUT)
   (Test Throughput To and From DUT) ..> (Setup Session) : <<include>>
   (Test Throughput To and From DUT) ..> (Run Test) : <<include>>
   (Test Throughput To and From DUT) ..> (Cleanup Session) : <<include>>
   } 
   package RunIperfTraffic{
   (Run Traffic To DUT) --|> (Run Test)
   (Run Traffic From DUT) --|> (Run Test)
   (Run Test) ..> (Setup Iperf Test) : <<include>>
   }

Related Requirements
--------------------

* |A1|
* |A2|
* |A3| 
* |A4|
* |A5|
* |A6|
* |A7|
* |A8|
* |A9|
* |A10|

Preconditions
-------------

* The APE has setup a well-formed configuration file
* The |CPC| is connected to the DUT and communicating via ADB
* The |TPC| has a running SSH Server
* The |DUT| is connected to the |AP|
* CPC and TPC are on the same subnet
* The DUT and |TPC| are on the same subnet
* TPC and DUT have `iperf` installed on their `PATH`

Postconditions
--------------

* The data from the `iperf` Session is stored in files. 
* The configuration file and system log are stored in the data folder.

Failed End Condition
--------------------

No, partial, or corrupted data has been saved for either sending devices.

Trigger
-------

|APE| requests `iperf` to and from DUT test.

Main Path
---------

#. (:include: `Setup Session`) The test components are set up.
#. (:include: `Run Iperf Traffic to DUT`) Traffic is run to the DUT.
#. (:include: `Run Iperf Traffic from DUT`) Traffic is run from the DUT.
#. (:include: `Cleanup Session`) Log and Configuration files are copied to the data folders.

Alternate Paths
---------------
1.1. A `CommandError`, `ConfigurationError` or `ConnectionError` is raised.

   1.1.1. The test exits.


2.1. A `CommandError`, `ConfigurationError` or `ConnectionError` is raised.

   2.1.1. The test exits.

.. include:: ../requirements_source.rst

