Test Throughput From DUT Use Case
=================================

.. uml::

   left to right direction

   actor APE

   skinparam packageStyle rect

   package RunTest{
   APE -> (Test Throughput From DUT)
   (Test Throughput From DUT) ..> (Setup Session) : <<include>>
   (Test Throughput From DUT) ..> (Run Test) : <<include>>
   (Test Throughput From DUT) ..> (Cleanup Session) : <<include>>
   } 
   package RunIperfTraffic{
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
* |A7|
* |A8|

Preconditions
-------------

* The APE has setup a well-formed configuration file
* The |CPC| is connected to the DUT and communicating via ADB
* The |TPC| has a running SSH Server
* The |DUT| is connected to the |AP|
* CPC and TPC are on the same subnet
* The DUT and |TPC| are on the same subnet
* TPC and DUT have `iperf` installed on their `PATH`

Postcondition
-------------

The data from the `iperf` Session is stored in files.

Failed End Condition
--------------------

No, partial, or corrupted data has been saved for the DUT.

Trigger
-------

|APE| requests `iperf` to DUT test.

Main Path
---------

#. (:include: `Setup Session`) The test components are set up.
#. (:include: `Setup Iperf Test`) Iperf Test Preparation completed.
#. (:inlclude: `Run Iperf Traffic From DUT`) Iperf Traffic from DUT is run.
#. (:include: `Cleanup Session`) Log and Configuration files are copied to the data folders.


Alternate Paths
---------------

1.1. System is unable to run Iperf Test Preparation.

   1.1.1. Test exits.

2.1. System is unable to run Traffic from the DUT to the TPC.

   2.1.1. Test exits.

.. include:: ../requirements_source.rst

