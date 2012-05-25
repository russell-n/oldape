Auto-Generated API
==================

The Sections correspond to sub-modules within the timetorecovertest package.

.. currentmodule:: timetorecovertest

.. autosummary::
   :toctree: base_api

   baseclass

Commands
--------

The **Commands** bundle specific commands with device connections. It is their responsibility to understand command errors and return validated output.

.. currentmodule:: timetorecovertest.commands

.. autosummary::
   :toctree: commands_api

   ping

Commons
-------

The **Commons** is a place to put things that the different sub-modules need to share.

.. currentmodule:: timetorecovertest.commons

.. autosummary::
   :toctree: commons_api

   errors
   generators
   output
   threads

Config
------

The **Config** is the primary user-interface for the test. It allows the APE to set parameters that need to change between tests. 

.. currentmodule:: timetorecovertest.config

.. autosummary::
   :toctree: config_api

   configfetcher
   configurationmap
   lexicographer
   parametergenerator
   
Connections
-----------

The **Connections** provide connectivity to devices. It is their responsibility to send commands to them and to understand connection failure errors.

.. currentmodule:: timetorecovertest.connections

.. autosummary::
   :toctree: connections_api

   adbconnection
   localconnection
   sl4aconnection

Devices
-------

The **Devices** provide a set of standardized method calls to the connections (the devices should all have the same method-names).

.. currentmodule:: timetorecovertest.devices

.. autosummary::
   :toctree: devices_api

   basedevice
   sl4adevice

Info
----

**Info** is the primary help system for the APE. It is meant to be a reminder system to remind the user how to configure the test and run it.

.. currentmodule:: timetorecovertest.info

.. autosummary::
   :toctree: info_api
   
   helper


Infrastructure
--------------

The **Infrastructure** contains modules to help run the test. It corresponds to the workers (TACOs)  who would run a physical test.

.. currentmodule:: timetorecovertest.infrastructure

.. autosummary::
   :toctree: infrastructure_api

   argumentparser
   builder
   countdowntimer
   crashhandler
   errors
   hortator
   testoperator
   setup
   strategerizer
   teardown

Tools
-----

The **Tools** are bundled commands that the operator uses. By ordering the set of tools, the operator creates the test-algorithm.

.. currentmodule:: timetorecovertest.tools

.. autosummary:: 
   :toctree: tools_api

   setupiteration
   sleep
   timetofailure
   timetorecoverytest


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

