Wget Session
============
.. module:: apetools.tools.wgetsession

The Wget Session repeatedly calls the `wget` command and monitors the outcome. The initial implementation will be for the :ref:`BusyboxWget <busybox-wget>` because it is being created for an emergency android-based project.


.. _busybox-wget-session:

BusyboxWget Session
-------------------

For the constructor, if only one of `max_time` or `repetitions` is given then that will be used to decide when to stop. If both are given, whichever is reached first will cause the session to end.

.. uml::

   BusyboxWgetSession -|> BaseClass

.. autosummary::
   :toctree: api

   BusyboxWgetSession
   BusyboxWgetSession.wget
   BusyboxWgetSession.data_file
   BusyboxWgetSession.time_remains
   BusyboxWgetSession.start_timer
   BusyboxWgetSession.__call__
   
