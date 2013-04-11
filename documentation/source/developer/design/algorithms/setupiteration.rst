SetupIteration Algorithms
=========================

.. _setupiterationrun:

SetupIteration.run()
--------------------

#. :math:`info \gets device.get\_wifi\_info()`
#. :math:`logger.debug(info)`
#. :math:`device.wake\_screen()`
#. :math:`device.display(info)`
#. :math:`\textit{if not ttf.run(parameters): raise ToolError}`
#. :math:`device.disable\_wifi()`
#. :math:`sleep(recovery\_time)`
