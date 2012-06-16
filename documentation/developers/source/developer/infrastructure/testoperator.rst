The Test Operator
=================

.. _testoperatoruml:

TestOperator
------------

The `TestOperator` runs a set of tests based on a given set of parameters.

.. uml::

   Operator o-- TestParameters
   Operator o-- OperatorParameters
   Operator o-- CountdownTimer
   Operator: OperatorParameters parameters
   Operator: ParameterGenerator test_parameters
   Operator: run()

See :ref:`operatorrun` for the `run` algorithm.

