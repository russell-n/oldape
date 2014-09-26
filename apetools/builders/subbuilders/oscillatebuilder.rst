Oscillate Builder
=================

A module to build a rotate object.



The OscillatorConfigurationError
--------------------------------

.. uml::

   ConfigurationError <|-- OscillatorConfigurationError

.. module:: apetools.builders.subbuilders.oscillatebuilder
.. autosummary:: 
   :toctree: api

   OscillatorConfigurationError



The Oscillate Builder
---------------------

.. uml::

   BaseToolBuilder <|-- OscillateBuilder
   OscillateBuilder o- ConfigurationMap
   OscillateBuilder o- SSHConnection
   OscillateBuilder o- Oscillate

.. autosummary::
   :toctree: api

   OscillateBuilder
   OscillateBuilder.semaphore
   OscillateBuilder.block
   OscillateBuilder.get_option
   OscillateBuilder.output
   OscillateBuilder.arguments
   OscillateBuilder.hostname
   OscillateBuilder.username
   OscillateBuilder.password
   OscillateBuilder.connection
   OscillateBuilder.product
   OscillateBuilder.parameters



The Oscillate Stop Builder
--------------------------

.. uml::

   BaseToolBuilder <|-- OscillateStopBuilder
   OscillateStopBuilder o- ConfigurationAdapter
   OscillateStopBuilder o- SSHConnection

.. autosummary::
   :toctree: api

   OscillateStopBuilder
   OscillateStopBuilder.get_option
   OscillateStopBuilder.hostname
   OscillateStopBuilder.username
   OscillateStopBuilder.password
   OscillateStopBuilder.connection
   OscillateStopBuilder.product
   OscillateStopBuilder.parameters   

