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



Base Process Command
--------------------

This is a base-class for commands that retrieve process-information.

.. autosummary::
   :toctree: api

   BaseProcessCommand

.. uml::

   BaseProcessCommand -|> BaseClass
   BaseProcessCommand : field
   BaseProcessCommand : error_expression
   BaseProcessCommand : error_messages
   BaseProcessCommand : command
   BaseProcessCommand : check_errors(line)
   BaseProcessCommand : run()
   BaseProcessCommand : __str__()
   BaseProcessCommand : process
   BaseProcessCommand : __call__()

   TopCommand -|> BaseProcessCommand
   PsCommand -|> BaseProcessCommand
   
Subclasses
~~~~~~~~~~

 * TopCommand
 * PsCommand

Responsibilities
~~~~~~~~~~~~~~~~

 * Sends the command over its connection

 * Traverses the output

 * Interprets errors

 * Yields output

Collaborators
~~~~~~~~~~~~~

 * Connections

This is an Abstract Class that should not be instantiated.



The BaseProcessGrep
-------------------

A base class to search for processes in the output of the BaseProcessCommand children.

