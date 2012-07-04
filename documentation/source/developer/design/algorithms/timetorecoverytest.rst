TimeToRecoveryTest Algorithms
=============================

The TimeToRecoveryTest contains the algorithm for a single test to determine the length of time it takes for a device to recover its connection.

.. _timetorecoverytestalgorithms:

The TimeToRecoveryTest Algorithms
---------------------------------

TimeToRecoveryTest.run(parameters)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. :math:`device.enable\_wifi()`
#. :math:`elapsed\_time \gets time\_to\_recovery.run()`
#. :math:`save\_data(elapsed\_time, failure\_threshold, repetition)`


TimeToRecoveryTest.save_data(elapsed, threshold, repetition)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. :math:`\textit{if }(elapsed > threshold) \vee (\textit{elapsed is None}):`

    #. :math:`log\_message(FAIL\_MESSAGE.format(repetition,elapsed,threshold))`

#. :math:`log\_message(TTR\_MESSAGE.format(elapsed))`
#. :math:`output.write(elapsed)`

.. uml::

   (*) --> if "failed" then
       ->[True] "log failure"
       --> "record TTR"

       else
           -->[False] "record TTR"
           --> (*)
       endif

   

TimeToRecoveryTest.log_message(message)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. :math:`device.log(message)`
#. :math:`logger.log(message)`

