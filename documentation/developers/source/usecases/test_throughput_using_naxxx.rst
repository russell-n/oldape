======================================
 Test Throughput Using Naxxx Use Case
======================================

.. uml::

   left to right direction
   APE --> ("Test Throughput Using Multiple APs")
   ("Test Throughput Using Multiple APs") ..> ("Cleanup Session") : <<include>>
   ("Test Throughput Using Multiple APs") ..> ("Setup Session") : <<include>>
   ("Test Throughput Using Multiple APs") ..> ("Run Test") : <<include>>
   ("Run Test") ..> ("Measure Throughput") : <<include>>
   ("Measure Throughput") <|-- ("Run Traffic From DUT") 
   ("Measure Throughput") <|-- ("Run Traffic To DUT")
   ("Measure Throughput") <|-- ("Run Traffic To and From DUT") 
   ("Run Test") ..> ("Setup Iteration") : <<include>>
   ("Setup Iteration") ..> ("Environmental Affector") : <<include>>
   ("Setup Iteration") ..> ("Wait For Device") : <<include>>
   ("Environmental Affector") <|-- ("Naxxx") 
   ("Wait For Device") <|-- ("Time To Recovery") 

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

#. Data from the iperf sessions has been stored to files.
#. Configuration file and logs are saved to the data files.

Main Path
---------

#. (:include: `Setup Session`) The test components are set up.
#. The naxxx enables the participating |AP|.
#. The naxxx disables all non-participating APs.
#. (:include: `Time To Recovery`) The system waits for the DUT to re-join the system.
#. (:include: `Run Iperf Traffic to DUT`) If configured, measure throughput to DUT.
#. (:include: `Run Iperf Traffic from DUT`) If configured, measure throughput from DUT.
#. (:include: `Cleanup Session`) Log and configuration files are copied to the DUT.

Alternative Paths
-----------------

2.1. The Naxxx raises a ConnnectionError.

   2.1.1. The system emits an error

   2.1.2. The system exits.

2.2. The Naxxx raises a NaxxxError.

   2.2.1. The system emits an error

   2.2.2. The current test iteration is exited.

.. uml::

   (*) -right-> "Setup Session"
   "Setup Session" -right-> "Start Test"
   "Start Test" -right-> "Enable AP"
   if "" then
      -right-> "Disable Other APs"
      if "" then
         -right-> "Wait For Dut"
         if "" then
            -right-> "Measure Throughput"
         else
            --> [error] "Emit Error" as emit
         endif
      else
         --> [error] emit
      endif
   else
      --> [error] emit 
      if "ConfigurationError" then
         --> "Start Test"
      else
         --> [NaxxxError] (*)
      endif
   endif
   "Measure Throughput" --> (*)
   
.. include:: ../requirements_source.rst
