BusyBox Wget Builder
====================

A builder of busybox wget sessions.



.. uml::

   ConfigurationError <|-- WgetSessionBuilderError

.. module:: apetools.builder.subbuilders.busyboxwgetbuilder
.. autosummary::
   :toctree: api

   WgetSessionBuilderError



.. uml::

   BaseToolBuilder <|-- BusyboxWgetBuilder

.. autosummary::
   :toctree: api

   BusyboxWgetBuilder
   BusyboxWgetBuilder.data_file
   BusyboxWgetBuilder.url
   BusyboxWgetBuilder.connection
   BusyboxWgetBuilder.storage
   BusyboxWgetBuilder.repetitions
   BusyboxWgetBuilder.max_time
   BusyboxWgetBuilder.product
   BusyboxWgetBuilder.parameters


