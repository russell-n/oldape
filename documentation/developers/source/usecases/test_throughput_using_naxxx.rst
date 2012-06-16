Test Throughput Using Multiple APs Use Case
===========================================

Narrative Description
---------------------

The |APE| sets up a |CPC|, |DUT|, |TPC|, |NAXXX|, and multiple *Access Points (APs)* attached to the NAXXX. The DUT is associated to each AP so that it will re-connect to each of them automatically if there is only one AP available. After setting up the physical system, the APE will create or alter a configuration file which specifies the parameters for the test. Once the setup is complete, the APE sends the `run` command to the system.

The system translates the configuration file into a set of runtime parameters, builds the necessary components using the parameters, and proceeds to the testing.

The system starts the testing by connecting to the DUT via the CPC and begins capturing the specified logs' output in background processes. It also inserts a message indicating that a test session is starting.

The system starts each individual test (1 per AP) by inserting a message into the DUT's log indicating that a new test is being started. It also inserts a message indicating that the pre-test setup is beginning. The system next identifies the next AP to test the DUT with and enables it via the Naxxx, disabling all of the other APs. The system then waits for the DUT to successfully ping the TPC, inserts a message into the log indicating the time to recover, then proceeds to the throughput tests.

Before running the throughput tests, the system inserts a message into the DUT's log indicating that the throughput tests will be starting. For each direction specified the system starts by killing any pre-existing `iperf` processes on the DUT and TPC. Once the `iperf` processes are dead, the system starts the `iperf` server on the receiving device, sleeps for a brief period while the server starts, then starts the client on the sending device. The system opens a file for each device using names based on the switch identifier, the direction of traffic relative to the DUT, the repetition number, and the protocol (i.e. *tcp* or *udp*). As the traffic is sent between the two devices, the standard output of each is captured in their respective files.

When the traffic is completed, output summarizing the outcome of the test is recorded by the system in the DUT's log. The system then sleeps for a brief recovery period before continuing with the next test.

When all the tests specified in the configuration are completed the system inserts a closing message into the DUT's log, waits for a brief period to allow the logs to complete, then copies the system log and configuration file to the data folder in order to enable reconstructing the test at a later date if it's needed.

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


Preconditions
-------------

* The |APE| has set up a |CPC|
* The |DUT| is connected to the |CPC| via |ADB|
* The |TPC| is on the same subnet as the DUT
* The TPC is on the same subnet as the CPC 
* The |NAXXX| is on the same subnet as the CPC
* The  *Access Points (APs)*  are plugged into the NAXXX. 
* The DUT is associated with each AP so that it will re-connect to each of them automatically if there is only one AP available. 
* A well-formed configuration file specifying the parameters for the test has been created. 

Main Path
---------

.. csv-table:: Main Path
   :header: Action, Requirement

   #. APE sends `run` command to system, |A2|
   #. System translates configuration file into set of runtime parameters, |A1|
   #. System builds necessary components using parameters, |A16|
   #. System precedes testing by connecting to the DUT via the CPC and starting to capture  specified logs' output in background, |A13|
   #. System inserts a message into DUT's log indicating that test session is starting, |A17|
   #. System starts each test (1 per AP) by inserting a message into the DUT's log indicating that a new test is being started, |A17|
   #. System inserts a message indicating that the pre-test setup is beginning, |A17|
   #. System identifies next AP to test  DUT with and enables it via |NAXXX|, |A12|
   #. System uses NAXXX to disable  all of other APs, |A12| 
   #. System waits for DUT to successfully ping TPC, |A14|
   #. System inserts time to recover into DUT log, |A17|
   #. System inserts a message into the DUT's log indicating that throughput tests starting, |A17|
   #. For each traffic direction specified System kills pre-existing `iperf` processes on DUT and TPC, |A5|
   #. System starts `iperf` server on the receiving device, |A18|
   #. System sleeps for a brief period while the server starts, |A22|
   #. System starts the client on the sending device, |A19|
   #. System opens file for each device using names based on switch ID, traffic direction relative to DUT, repetition, and protocol, |A20|
   #. As traffic is sent between devices, standard output of each is captured in their respective files, |A8|
   #. summary of test outcome is recorded by the system in the DUT's log, |A21|, |A17|
   #. System sleeps for brief recovery period before continuing with next test, |A22|
   #. System inserts closing message into  DUT's log, |A17|
   #. System waits for a brief period to allow the logs to complete, |A22|
   #. System  copies its log and configuration file to data folder |A9|, |A10|, |A23|

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
