Tool Classes
============

Tools are what the operator uses to perform his duties.

SetupIteration
--------------

The `SetupIteration` does whatever needs to be done just prior to the execution of a test repetition.

.. uml::

   SetupIteration: Device device
   SetupIteration: run()

See :ref:`setupiterationrun` for the run algorithm

.. _timetorecoverytestuml:

TimeToRecoveryTest
------------------

The `TimeToRecoveryTest` executes a single TTR test repetition.

.. uml::

   TimeToRecoveryTest: File output
   TimeToRecoveryTest: Device device
   TimeToRecoveryTest: Command time_to_recovery
   TimeToRecoveryTest: run(parameters)
   TimeToRecoveryTest: sleep(sleep_time)
   TimeToRecoveryTest: save_data(elapsed,threshold, repetition)
   TimeToRecoveryTest: log_message(message)

See :ref:`timetorecoverytestalgorithms` for the TimeToRecoveryTest algorithms.

PingCommand
-----------

The `PingCommand` is used as the TTR test-condition.

.. uml::

   PingCommand: String target
   PingCommand: String command
   PingCommand: re ping_match
   PingCommand: wait_for_success(Float timeout)
   PingCommand: run()

See :ref:`pingcommandalgorithms` for the PingCommand algorithms.

