Test Operator
=============

An operator operates tests.

For each configuration-file found an operator is created.

::

    OperatorStaticTestParameters = namedtuple("OperatorStaticTestParameters",
                                              ['operator_parameters',
                                               'static_parameters',
                                               'test_parameters'])
    
    

::

    TEST_TAG = "**** {tag}: {s} Test {r} of {t} ****"
    
    TEST_POSTAMBLE = "**** {tag}: Ending test - elapsed time = {t} ****"
    TEST_RESULT = "**** {tag}: Test Result = {r} ****"
    
    



.. uml::

   BaseClass <|-- TestOperator

.. module:: apetools.proletarians.testoperator
.. autosummary::
   :toctree: api

   TestOperator
   TestOperator.countdown_timer
   TestOperator.sub_logger
   TestOperator.sleep
   TestOperator.one_repetition
   TestOperator.log_info
   TestOperator.__call__
   TestOperator.keyboard_interrupt_intercept

