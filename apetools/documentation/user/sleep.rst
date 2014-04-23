Sleep Configuration
===================

The `[SLEEP]` section setsup a blocking call that does nothing for a set amount of time. It follows the same convention as the other times (like iperf)::

   [SLEEP]
   # this sleeps so that you can insert time for commands that might create race-conditions
   time = 1 Hour


