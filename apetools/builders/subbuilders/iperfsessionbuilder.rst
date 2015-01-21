Iperf Session Builder
=====================



.. module:: apetools.builders.subbuilders.iperfsessionbuilder
.. autosummary::
   :toctree: api

   IperfSessionBuilderError

.. uml::

   ConfigurationError <|-- IperfSessionBuilderError



.. autosummary::
   :toctree: api

   IperfSessionBuilder
   IperfSessionBuilder.filename
   IperfSessionBuilder.test
   IperfSessionBuilder.directions
   IperfSessionBuilder.product
   IperfSessionBuilder.parameters  

.. uml::

   BaseToolBuilder <|-- IperfSessionBuilder
   IperfSessionBuilder o- MasterBuilder
   IperfSessionBuilder o- ConfigurationMap
   IperfSessionBuilder o- IperfTestBuilder
   IperfSessionBuilder o- IperfSession

