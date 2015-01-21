The Sleep Builder
=================

A module to build a sleep object.



The Sleep Configuration Error
-----------------------------

.. uml::

   ConfigurationError <|-- SleepConfigurationError

.. module:: apetools.builders.subbuilders.sleepbuilder
.. autosummary::
   :toctree: api

   SleepConfigurationError



The Sleep Configuration Enum
----------------------------

::

    class SleepConfigurationEnum(object):
        __slots__ = ()
        time = 'time'
    
    



The Sleep Builder
-----------------

.. uml::

   BaseToolBuilder <|-- SleepBuilder

.. autosummary::
   :toctree: api

   SleepBuilder
   SleepBuilder.product
   SleepBuilder.parameters
        
