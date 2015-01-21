The BaseClass
=============

This is a module for base classes that have common methods to inherit.



The BaseClass
-------------

The `BaseClass` sets up a logger for its children so that the module and class names are printed in the logging information.

.. module:: apetools.baseclass
.. autosummary::
   :toctree: api

   BaseClass
   BaseClass.logger
   


The BaseThreadClass
-------------------

The `BaseThreadClass` extends the `BaseClass` by adding a `run_thread` method that calls (an as yet undefined) `run` method and catches any exceptions and logs the traceback. This way if the `run_thread` method is run in a thread and it crashes there will be more information in the logging (hopefully). This probably could be done with a decorator as well.

.. uml::

   BaseClass <|-- BaseThreadClass

.. autosummary::
   :toctree: api

   BaseThreadClass
   BaseThreadClass.run_thread
   
