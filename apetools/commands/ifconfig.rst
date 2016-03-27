IFConfig
========

A module to query the device for interface information.







The Ifconfig Error
------------------

.. uml::

   ConfigurationError <|-- IfconfigError

.. module:: apetools.commands.ifconfig
.. autosummary::
   :toctree: api

   IfconfigError




The Ifconfig Command
--------------------

.. uml::

   BaseClass <|-- IfconfigCommand

.. autosummary:: 
   :toctree: api

   IfconfigCommand
   IfconfigCommand.operating_system
   IfconfigCommand.ip_address
   IfconfigCommand.ip_expression
   IfconfigCommand.mac_address
   IfconfigCommand.output
   IfconfigCommand._match



