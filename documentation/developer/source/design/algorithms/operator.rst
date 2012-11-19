Operator Algorithms
===================

The operator runs a single test-type. It is the holder of the test algorithm. 

.. _operatorrun:

Operator.run
------------

#. :math:`countdown\_timer.start\_timer()`
#. :math:`\textit{for parameter}\in\textit{parameters.parameters}:`

    #. :math:`setup.run(parameter)`
    #. :math:`test.run(parameter)`
    #. :math:`teardown.run(parameter)`
    #. :math:`logger.info(TIME\_REMAINING.format(t \gets countdown\_timer.remaining\_time))`



