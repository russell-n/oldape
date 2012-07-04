Test Throughput To DUT Use Case
===============================

.. uml::

   left to right direction

   actor APE

   skinparam packageStyle rect

   package RunTest{
   APE -> (Test Throughput To DUT)
   (Test Throughput To DUT) ..> (Setup Session) : <<include>>
   (Test Throughput To DUT) ..> (Run Test) : <<include>>
   (Test Throughput To DUT) ..> (Cleanup Session) : <<include>>
   }
   package RunIperfTraffic{
   (Run Test) ..> (Setup Iperf Test) : <<include>>
   (Run Traffic To DUT) --|> (Run Test)
   }


Related Requirements
--------------------

* |A1|
* |A2|
* |A3| 
* |A4|
* |A5|
* |A6|
* |A8|
* |A9|
* |A10|

Precondition
------------

* The APE has setup a well-formed configuration file
* The |CPC| is connected to the DUT and communicating via ADB
* The |TPC| has a running SSH Server
* CPC and TPC are on the same subnet
* The |DUT| is connected to the |AP|
* The DUT and |TPC| are on the same subnet
* TPC and DUT have `iperf` installed on their `PATH`

Postcondition
-------------

* The data from the `iperf` Session is stored in Files. 
* The configuration file and system log are stored in the data folder.

Failed End Condition
--------------------

No, partial, or corrupted data has been saved for the TPC.

Trigger
-------

|APE| requests `iperf` to DUT test.


Main Path
---------

#. (:include: `Setup Session`) The test components are set up.
#. (:include: `Setup Iperf Test`) Iperf Test Preparation completed.
#. (:include: `Run Iperf Traffic to DUT`) Iperf Traffic to DUT is run.
#. (:include: `Cleanup Session`) Log and Configuration files are copied to the data folders.


Alternate Paths
---------------

1.1. System unable to complete preparation

   1.1.1. The test is exited

2.1. System is unable to complete test

   2.1.1. Test is exited

.. include:: ../requirements_source.rst

