The Base Command
================


A base for certain (simple) commands.



The BaseThreadedCommand
-----------------------

This is an abstract base class for threaded commands. Children of it will raise an exception on instantiation if the `run` and `stop` methods are not defined. The main interface to it is the `__call__` which will pass in any arguments given to the `run_thread` method (inherited from the `BaseThreadClass`).

.. autosummary::
   :toctree: api

   BaseThreadedCommand

.. uml::

   BaseThreadedCommand -|> BaseThreadClass
   BaseThreadedCommand : logger
   BaseThreadedCommand : stopped
   BaseThreadedCommand : thread
   BaseThreadedCommand : run()
   BaseThreadedCommand : stop()
   BaseThreadedCommand : __call__(*args, **kwargs)

* To understand the `run_thread` see :ref:`BaseThreadClass <base-thread-class>`.   

