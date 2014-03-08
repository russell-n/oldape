The Time to Failure Algorithm
=============================

The time to failure algorithm determines when a failure event occurs.

.. _timetofailurealgorithm:

TimeToFailure Algorithm
-----------------------

.. code-block:: python

   def run(parameters):
       start = now()
       time_limit = start + timeout
       failures = 0
       first = None
       while failures < threshold and now() < time_limit:
           if self.pinger.run(target):
              failures = 0
              first = None
           else:
              failures += failures
           if failures == 1:
               first = now()
       if failures == threshold and first is not None:
           return first - start
       return

