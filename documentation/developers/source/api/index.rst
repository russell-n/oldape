Auto-Generated API
==================

The Sections correspond to sub-modules within the timetorecovertest package.

.. currentmodule:: timetorecovertest

.. autosummary::
   :toctree: base_api

   baseclass
   log_setter
   main

Commands
--------

The **Commands** bundle specific commands with device connections. It is their responsibility to understand command errors and return validated output.

.. currentmodule:: tottest.commands

.. autosummary::
   :toctree: commands_api

   changeprompt
   ifconfig
   netcfg
   ping

Commons
-------

The **Commons** is a place to put things that the different sub-modules need to share.

.. currentmodule:: tottest.commons

.. autosummary::
   :toctree: commons_api

   assertions
   errors
   expressions
   generators
   readoutput
   storageoutput

Config
------

The **Config** is the primary user-interface for the test. It allows the APE to set parameters that need to change between tests. 

.. currentmodule:: tottest.config

.. autosummary::
   :toctree: config_api

   configfetcher
   config_options
   configurationmap
   lexicographer
   parametergenerator
   
Adapters
--------

The **Adapters** adapt external libraries for connections to provide a common interface.

.. currentmodule:: tottest.connections

.. autosummary::
   :toctree: adapters_api

   serialadapter
   sshadapter
   telnetadapter


Connections
-----------

The **Connections** provide connectivity to devices. It is their responsibility to send commands to them and to understand connection failure errors.

.. currentmodule:: tottest.connections

.. autosummary::
   :toctree: connections_api

   adbconnection
   localconnection
   serialconnection
   sshconnection
   telnetconnection

Devices
-------

The **Devices** provide a set of standardized method calls to the connections (the devices should all have the same method-names).

.. currentmodule:: tottest.devices

.. autosummary::
   :toctree: devices_api

   basedevice

Info
----

**Info** is the primary help system for the APE. It is meant to be a reminder system to remind the user how to configure the test and run it.

.. currentmodule:: tottest.info

.. autosummary::
   :toctree: info_api
   
   helper


Infrastructure
--------------

The **Infrastructure** contains modules to help run the test. It corresponds to the workers (TACOs)  who would run a physical test.

.. currentmodule:: tottest.infrastructure

.. autosummary::
   :toctree: infrastructure_api

   argumentparser
   builder
   countdowntimer
   crashhandler
   data
   enabledebugging
   errors
   hortator
   setup
   strategerizer
   teardown
   testoperator

Threads
-------

The **Threads** are used by the logwatchers and connections so they don't block execution.

.. currentmodule:: tottest.threads

.. autosummary:: 
   :toctree: threads_api

   barrier
   lock
   semaphore
   threads

Tools
-----

The **Tools** are bundled commands that the operator uses. By ordering the set of tools, the operator creates the test-algorithm.

.. currentmodule:: tottest.tools

.. autosummary:: 
   :toctree: tools_api

   copyfiles
   movefiles
   setupiteration
   sleep
   teardowniteration
   timetofailure
   timetorecovery
   timetorecoverytest

Watchers
--------

The **Watchers** watch logs.x

.. currentmodule:: tottest.watchers

.. autosummary:: 
   :toctree: watchers_api
   
   logcatwatcher
   logwatcher
   thewatcher


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

