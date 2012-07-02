Use Case 1
==========

This is the base case to get the product line tested.

.. uml::

   APE --> (Test Throughput To DUT) : configuration
   TACO <-- (Test Throughput To DUT) : data

Preconditions
-------------

* The Device Under Test (DUT) is an `Android` device with an ADB connection on the PC Running the test (Control PC)
* The Control PC is running linux
* The DUT is connected to the proper AP
* The Traffic PC (TPC) is connected to the same subnet as the DUT
* Both devices have iperf in their `PATH` variable
* The TPC has an SSH Server running on it 
* The Allion Performance Evaluator (APE) has set the values in the configuration file
* The configuration file is in the directory where the test is started

Main Path
---------

#. The system gets the configuration from the APE:

    * DUT's Test IP Address (or resolvable host name)
    * TPC's Test IP Address
    * TPC's Control IP Address
    * TPC's Username
    * TPC's password (if needed)
    * The duration of the test
    * The base name for the data file
    * The base folder name for the files
    * The number of times to repeat the test

#. The system translates the declared configuration to parameters for the system's components.

#. The system builds the components based on the parameters.

#. The system connects to the devices.

#. The system runs throughput to the DUT.

#. The throughput data is saved to a file.

#. The generated logs are put in the data folder.

Alternate Paths
---------------

2.1. An option error or missing (required) option is detected.

   1. A `ConfigurationError` is raised.
   2. A Crash Report is generated.
   3. The system exits.

4.1. The system is unable to connect to a device.

   1. a `ConnectionError` is raised.
   2. A Crash Report is generated.
   3. The system exits. 

5.1. The test commands detect errors.

   #. A `CommandError` is raised.
   #. The `TestOperator` logs the error

      #. If the error is non-fatal, the operator moves to the next operation
      #. If the error is fatal, an `OperatorError` is raised.

         #. `Hortator` notes the death of the Operator.
         #. The Hortator moves on to exhort the next Operator.
