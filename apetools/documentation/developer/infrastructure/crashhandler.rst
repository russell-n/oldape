The Crash Handler
=================

A CrashHandler handles Hortator deaths.

.. uml::

   CrashHandler o-- Notifier
   CrashHandler: args
   CrashHandler: run(error)
