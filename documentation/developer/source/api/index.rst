Auto-Generated API
==================

The sections of the *API* correspond to sub-modules within the timetorecovertest package.

.. currentmodule:: apetools

.. autosummary::
   :toctree: base_api

   baseclass
   log_setter
   main

Affectors
---------

The *Affectors* affect the environment (as opposed to impelling devices to change themselves).


Networked Power Supply
~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: apetools.affectors.elexol

.. autosummary::
   :toctree: naxxx_api
   
   elexol
   errors
   naxxx
   networkedpowersupply

The Rotator
~~~~~~~~~~~

.. currentmodule:: apetools.affectors.rotator

.. autosummary::
   :toctree: rotator_api

   rotator

Synaxx
~~~~~~

.. currentmodule:: apetools.affectors.synaxxx

.. autosummary::
   :toctree: synaxxx_api
   
   synaxxx


The Rest
~~~~~~~~

.. currentmodule:: apetools.affectors

.. autosummary::
   :toctree: other_affectors_api

   ners
   apconnect

Builder
-------

The **Builder** builds. It maps the Lexicographer's parameters to objects by calling sub-builders.

.. currentmodule:: apetools.builders

.. autosummary::
   :toctree: builders_api
   
   builder
   

Sub-Builders
~~~~~~~~~~~~

*Sub-Builders* are experts in building their objects, allowing the *Builder* to delegate the burden of knowledge to them.

.. currentmodule:: apetools.builders.subbuilders

.. autosummary::
   :toctree: sub_builders_api
   
   affectorbuilder
   apconnectbuilder
   basedevicebuilder
   baseoperationbuilder
   basetoolbuilder
   builderenums
   commandwatcherbuilder
   connectionbuilder
   devicebuilder
   dumpdevicestatebuilder
   executetestbuilder
   iperfcommandbuilder
   iperfparameterbuilder
   iperfsessionbuilder
   iperftestbuilder
   logwatchersbuilder
   nersbuilder
   nodebuilder
   nodesbuilder
   operationsetupbuilder
   operationteardownbuilder
   oscillatebuilder
   pollerbuilder
   poweroffbuilder
   poweronbuilder
   reportbuilder
   rotatebuilder
   setupiterationbuilder
   setuptestbuilder
   storagepipebuilder
   teardownbuilder
   teardowniterationbuilder
   teardowntestbuilder
   timetorecoverybuilder
   toolbuilder
   tpcdevicebuilder
   watcherbuilder


Commands
--------

The **Commands** bundle specific commands with device connections. It is their responsibility to understand command errors and return validated output.

.. currentmodule:: apetools.commands

.. autosummary::
   :toctree: commands_api

   basecommand
   basewificommand
   changeprompt
   dumpsyswifi
   ifconfig
   ipconfig
   iperfbroadcast
   iperfcommand
   iwcommand
   iwconfig
   netcfg
   netsh
   oscillate
   ping
   poweroff
   poweron
   rotate
   svc
   wificommand
   windowsssindconnect
   winrssi
   wlcommand
   wmic
   wpacli

Commons
-------

The **Commons** is a place to put things that the different sub-modules need to share.

.. currentmodule:: apetools.commons

.. autosummary::
   :toctree: commons_api

   assertions
   broadcaster
   centraltendency
   coroutine
   datacounter
   dummy
   enumerations
   errors
   events
   expressions
   filterer
   generators
   readoutput
   reporter
   storagebroadcaster
   storageoutput
   timestamp

Connections
-----------

The **Connections** provide connectivity to devices. It is their responsibility to send commands to them and to understand connection failure errors.

.. currentmodule:: apetools.connections

.. autosummary::
   :toctree: connections_api

   adbconnection
   localconnection
   nonlocalconnection
   puppetconnection
   serialconnection
   sl4aconnection   
   sshconnection
   telnetconnection

   sharedcounter
   lineproducer
   producer
   
* The `lineproducer` is a utility used to break up lines for connections that only have access to streams (as opposed to file-like objects). 
* `sharedcounter` was created to prevent the subprocess files from prematurely killing the process on deletion (it acts like a non-blocking semaphore)

Adapters
~~~~~~~~

The **Adapters** adapt external libraries for connections to provide a common interface (and are kept with their connections).

.. currentmodule:: apetools.connections

.. autosummary::
   :toctree: adapters_api

   serialadapter
   sshadapter
   telnetadapter


Devices
-------

The **Devices** provide a set of standardized method calls to the connections (the devices should all have the same method-names).

.. currentmodule:: apetools.devices

.. autosummary::
   :toctree: devices_api

   basedevice
   adbdevice
   dummydevice
   linuxdevice
   sl4adevice
   windowsdevice

Informants
----------

**Informants** provide command-line help system for the APE. It is meant to be a prompting system to remind the user how to configure the test and run it.

.. currentmodule:: apetools.informants

.. autosummary::
   :toctree: info_api
   
   helper


Lexicographers
--------------

The *Config-file* is the primary user-interface for the test. It allows the APE to set parameters that need to change between tests. The **Lexicographer** translate config-files to parameters for the builder(s).

.. currentmodule:: apetools.lexicographers

.. autosummary::
   :toctree: lexicographer_api

   configfetcher
   config_options
   configurationmap
   lexicographer
   parametergenerator
   parametertree
   timeconverter


Operations
----------

`operations` are tool bundlers for the TestOperator.

.. currentmodule:: apetools.operations

.. autosummary::
   :toctree: operations_API

   baseoperation
   executetest
   operationsetup
   operationteardown
   setuptest
   teardowntest

Parameters
----------

**Parameters** hold complex parameters for complicated commands. Besides being holders of values, they check for errors in settings and allow the dynamic generation of values.

.. currentmodule:: apetools.parameters

.. autosummary:: 
   :toctree: parameters_api

   iperf_client_parameters
   iperf_common_parameters
   iperf_common_tcp_parameters
   iperf_server_parameters
   iperf_test_parameters
   iperf_udp_parameters

Since the parameters define the behavior of commands, choosing them declares their behavior, much as the choice and ordering of the tools defines the behavior of the Test Operator. 

Parsers
-------

.. currentmodule:: apetools.parsers

.. autosummary::
   :toctree: parsers_api

   coroutine
   iperfexpressions
   iperfparser
   oatbran
   sumparser
   unitconverter

Pipes
-----

.. currentmodule:: apetools.pipes

.. autosummary::
   :toctree: pipes_api

   commandpipe
   storagepipe

Proletarians
------------

The **Proletarians** contains modules to run the test. They are the civil-servants of the system -- modules that shouldn't change for different types of tests.

.. currentmodule:: apetools.proletarians

.. autosummary::
   :toctree: proletarian_api

   argumentparser
   countdowntimer
   crashhandler
   data
   enabledebugging
   errors
   hortator
   liststrategy
   setuprun
   strategerizer
   teardown
   testoperator

Threads
-------

The **Threads** are used by the logwatchers and connections so they don't block execution (these aren't actually used at run-time, they're for debugging).

.. currentmodule:: apetools.threads

.. autosummary:: 
   :toctree: threads_api

   barrier
   lock
   semaphore
   threads

Tools
-----

The **Tools** are bundled commands that the operator uses. By ordering the set of tools, the operator creates the test-algorithm.

.. currentmodule:: apetools.tools

.. autosummary:: 
   :toctree: tools_api

   copyfiles
   dumpdevicestate
   getipaddress
   iperfsession
   iperftest
   killall
   movefiles
   networktester
   setupiteration
   sleep
   teardowniteration
   testdumpsyswifi
   timetofailure
   timetorecovery
   timetorecoverytest
   wifitool

The difference between a tool and a command is somewhat obscure right now. The idea is that the tools have a defined singular purpose and so might have one or more commands bundled inside them. If the operator is using it, it should be a tool.

Watchers
--------

The **Watchers** watch logs.

.. currentmodule:: apetools.watchers

.. autosummary:: 
   :toctree: watchers_api
   
   basedevicepoller
   commandwatcher
   devicepoller
   logcatwatcher
   logwatcher
   rssipoller
   thewatcher
   tsharkwatcher


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

