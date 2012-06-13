======================================
 Test Throughput Using Naxxx Use Case
======================================

.. uml::

   left to right direction
   APE --> ("Test Throughput Using Naxxx")
   ("Test Throughput Using Naxxx") ..> ("Cleanup Session") : <<include>>
   ("Test Throughput Using Naxxx") ..> ("Setup Session") : <<include>>
   ("Test Throughput Using Naxxx") ..> ("Run Test") : <<include>>
   ("Run Traffic From DUT") --|> ("Run Test")
   ("Run Traffic To DUT") --|> ("Run Test")
   ("Run Test") ..> ("Setup Iperf Test") : <<include>>
   ("Setup Iperf Test") ..> ("Environmental Affector") : <<include>>
   ("Naxxx") --|> ("Environmental Affector")

Related Requirements
--------------------

* |A11|
* |A12|

Preconditions
-------------

#. The APE has created a well-formed configuration file.
#. The naxxx is on the same subnet as the control pc.
#. The AP's are plugged into the naxxx.
#. The AP's have been previously connected to the DUT.
#. The DUT has been confirmed to roam to AP's.
#. The Control PC is connected to the DUT and communicating via ADB.
#. The TPC has a running SSH Server.
#. CPC and TPC are on the same (control) subnet.
#. DUT, AP, and TPC are on the same (test) subnet.
#. TPC and DUT have iperf installed on their `PATH`.

Postconditions
--------------

#. Data from the iperf sessions has been stored to Files.
#. Configuration file and logs are saved to the data files.

Main Path
---------

#. The System converts the 

