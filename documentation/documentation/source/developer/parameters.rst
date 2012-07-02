Parameters
==========

Parameters are objects passed to an object's constructor which contain the parameters that define the initial conditions for the object.

TestOperator Parameters
-----------------------

The :ref:`testoperatoruml` defines two parameters - `OperatorParameters` and `OperatorStaticParameters`.

OperatorParameters
~~~~~~~~~~~~~~~~~~

.. uml::

   OperatorParameters: SetupIteration setup
   OperatorParameters: TeardownIteration teardown
   OperatorParameters: TimeToRecoveryTest test
   OperatorParameters: Device.log device_log

The OperatorParameters contain the objects that the TestOperator needs to call in its run method.

OperatorStaticParameters
~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

   OperatorStaticParameters: OperatorParameters operator_parameters
   OperatorStaticParameters: StaticParameters static_parameters
   OperatorStaticParameters: ParameterGenerator test_parameters

The `operator_parameters` are described in the previous section. `StaticParameters` are the mapping the :ref:`lexicographeruml` creates from the config-file to python-values. the `test_parameters` is a :ref:`parametergeneratoruml` iterator.

Lexicographer Parameters
------------------------

The :ref:`lexicographeruml` generates `StaticParameters`.

.. uml::

   StaticParameters: String output_folder
   StaticParameters: String data_file
   StaticParameters: Integer repetitions
   StaticParameters: Float recovery_time
   StaticParameters: Float timeout
   StaticParameters: Integer threshold
   StaticParameters: String target
   StaticParameters: String wifi_interface

These parameters map to the values declared by the APE when creating the config-file. They are provided to allow the builder to use them in creating objects for the :ref:`testoperatoruml`.

TimeToRecoveryTest Parameters
-----------------------------

The :ref:`timetorecoverytestuml` requires `TimeToRecoveryTestParameters`.

.. uml::

   TimeToRecoveryTestParameters: Device device
   TimeToRecoveryTestParameters: TimeToRecovery time_to_recovery
   TimeToRecoveryTestParameters: FileOutput output

* The `device` is used to enable the radio on the DUT.  

* The `time_to_recovery` returns the amount of time it took for the radio to work

* The output is a writeable file-like object to send the data to.


