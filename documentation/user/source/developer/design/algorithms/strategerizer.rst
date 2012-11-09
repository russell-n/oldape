Strategerizer Algorithms
========================

.. _strategerizerrun:

The `run` strategy
------------------

Main Path
~~~~~~~~~

#. :math:`setup \gets SetUp(args)`
#. :math:`setup.run()`

    #. :math:`Exception \Rightarrow Crash Path`

#. :math:`teardown \gets TearDown(setup)`
#. :math:`teardown.run()`

Crash Path
~~~~~~~~~~

#. Log the error
#. :math:`crash\_handler \gets CrashHandler(args)`
#. :math:`crash\_handler.run()`

Here the assumption is that something might have gone wrong in either the setup or the running of the test so it gets started all over.
