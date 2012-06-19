The Test Operator
=================

.. _testoperatoruml:

TestOperator
------------

The `TestOperator` runs a set of tests based on a given set of parameters.

.. uml::

   TestOperator o-- ParameterGenerator
   TestOperator o-- CountdownTimer
   TestOperator o-- SetupIteration
   TestOperator o-- TeardownIteration
   TestOperator o-- IperfTest
   TestOperator o-- TearDownOperation
   TestOperator o-- Watcher
   TestOperator o-- Connection
   TestOperator o-- Sleep
   TestOperator: run()

See :ref:`operatorrun` for the `run` algorithm.

