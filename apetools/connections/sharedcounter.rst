Shared Coounter
===============

A class to provide a simple shared counter that connection can change and check.

This was created for the PopenProducer so that the file objects can know whether
it's safe to kill the parent process.

.. module:: apetools.connections.sharedcounter
.. autosummary::
   :toctree: api

   SharedCounter
   SharedCounter.increment
   SharedCounter.decrement
   SharedCounter.__eq__

