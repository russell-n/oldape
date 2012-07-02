Hortator Algorithms
===================

The Hortator is the driver of the operations. Its role is to run the Operators, handle their crashes, and report the overall time elapsed as well as the time of any crashes.


.. _hortatorrun:

Hortator.run
------------

Main Path
~~~~~~~~~

#. :math:`start \gets clock.now()`
#. :math:`operation \gets 0`
#. :math:`\textit{for operator }\in \textit{ operators}:`

   #. :math:`operation' \gets operation + 1`
   #. :math:`operation\_start \gets clock.now()`
   #. :math:`operator.run()`
   #. :math:`OperatorError \Rightarrow HandleCrash`

#. :math:`end \gets clock.now()`
#. :math:`\textit{for crash }\in\textit{ crash\_times}:`

   #. :math:`\textit{print str(crash)}`

#. :math:`logger.info(end - start)`

`HandleCrash` Path
~~~~~~~~~~~~~~~~~~

#. :math:`crash\_time \gets clock.now()`
#. :math:`logger.error(error)`
#. :math:`crash\_times.append(CrashRecord(operation, operation\_start, crash\_time, error))`


