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
   enumerations
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

The **Adapters** adapt external libraries for connections to provide a common interface (and are kept with their connections).

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
   sl4aconnection   
   sshconnection
   telnetconnection

   lineproducer

* The `lineproducer` is a utility used to break up lines for connections that only have access to streams (not files). 

Devices
-------

The **Devices** provide a set of standardized method calls to the connections (the devices should all have the same method-names).

.. currentmodule:: tottest.devices

.. autosummary::
   :toctree: devices_api

   basedevice
   sl4adevice

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

Parameters
----------

**Parameters** hold complex parameters for complicated commands. Besides being holders of values, they allow for errors in settings and dynamically generated values.

.. currentmodule:: tottest.parameters

.. autosummary:: 
   :toctree: parameters_api

   iperf_client_parameters
   iperf_common_parameters
   iperf_common_tcp_parameters
   iperf_server_parameters
   iperf_udp_server_parameters

Since the parameters define the behavior of commands, choosing them in many ways declares their behavior, much as the choice and ordering of the tools defines the behavior of the Test Operator. 

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
   getipaddress
   killall
   movefiles
   networktester
   setupiteration
   sleep
   teardowniteration
   timetofailure
   timetorecovery
   timetorecoverytest

The difference between a tool and a command is somewhat obscure right now. The idea is that the tools have a defined singular purpose and so might have one or more commands bundled inside them. If the operator is using it, it should be a tool.

Watchers
--------

The **Watchers** watch logs.

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

