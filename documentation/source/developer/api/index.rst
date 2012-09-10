Auto-Generated API
==================

The sections of the *API* correspond to sub-modules within the timetorecovertest package.

.. currentmodule:: tottest

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

.. currentmodule:: tottest.affectors.elexol

.. autosummary::
   :toctree: affectors_api
   
   elexol
   errors
   naxxx
   networkedpowersupply


Builder
-------

The **Builder** builds. It maps the Lexicographer's parameters to objects by calling sub-builders.

.. currentmodule:: tottest.builders

.. autosummary::
   :toctree: builders_api
   
   builder
   

Sub-Builders
~~~~~~~~~~~~

*Sub-Builders* are experts in building their objects, allowing the *Builder* to delegate the burden of knowledge to them.

.. currentmodule:: tottest.builders.subbuilders

.. autosummary::
   :toctree: sub_builders_api
   
   affectorbuilder
   connectionbuilder
   devicebuilder
   setupiterationbuilder
   teardownbuilder
   teardowniterationbuilder
   testbuilder
   timetorecoverybuilder
   watchersbuilder


Commands
--------

The **Commands** bundle specific commands with device connections. It is their responsibility to understand command errors and return validated output.

.. currentmodule:: tottest.commands

.. autosummary::
   :toctree: commands_api

   changeprompt
   dumpsyswifi
   ifconfig
   iperfbroadcast
   iperfcommand
   iwcommand
   netcfg
   ping
   svc
   wmic
   wpacli

Commons
-------

The **Commons** is a place to put things that the different sub-modules need to share.

.. currentmodule:: tottest.commons

.. autosummary::
   :toctree: commons_api

   assertions
   broadcaster
   centraltendency
   datacounter
   dummy
   enumerations
   errors
   expressions
   filterer
   generators
   readoutput
   reporter
   storagebroadcaster
   storageoutput

   
Connections
-----------

The **Connections** provide connectivity to devices. It is their responsibility to send commands to them and to understand connection failure errors.

.. currentmodule:: tottest.connections

.. autosummary::
   :toctree: connections_api

   adbconnection
   localconnection
   nonlocalconnection
   producer
   puppetconnection
   serialconnection
   sl4aconnection   
   sshconnection
   telnetconnection

   sharedcounter
   lineproducer
   
* The `lineproducer` is a utility used to break up lines for connections that only have access to streams (as opposed to file-like objects). 
* `sharedcounter` was created to prevent the subprocess files from prematurely killing the process on deletion (it acts like a non-blocking semaphore)

Adapters
~~~~~~~~

The **Adapters** adapt external libraries for connections to provide a common interface (and are kept with their connections).

.. currentmodule:: tottest.connections

.. autosummary::
   :toctree: adapters_api

   serialadapter
   sshadapter
   telnetadapter


Devices
-------

The **Devices** provide a set of standardized method calls to the connections (the devices should all have the same method-names).

.. currentmodule:: tottest.devices

.. autosummary::
   :toctree: devices_api

   basedevice
   adbdevice
   sl4adevice

Informants
----------

**Informants** provide command-line help system for the APE. It is meant to be a prompting system to remind the user how to configure the test and run it.

.. currentmodule:: tottest.informants

.. autosummary::
   :toctree: info_api
   
   helper


Lexicographers
--------------

The *Config-file* is the primary user-interface for the test. It allows the APE to set parameters that need to change between tests. The **Lexicographer** translate config-files to parameters for the builder(s).

.. currentmodule:: tottest.lexicographers

.. autosummary::
   :toctree: lexicographer_api

   configfetcher
   config_options
   configurationmap
   lexicographer
   parametergenerator

Sub-Lexicographers
~~~~~~~~~~~~~~~~~~

**Sub-Lexicographers** know how to translate specific sections of the config-file, alleviating the translational burden of the main *Lexicographer*.

.. currentmodule:: tottest.lexicographers.sublexicographers

.. autosummary::
   :toctree: sub_lexicographer_api
   
   devicelexicographer
   naxxxlexicographer


Parameters
----------

**Parameters** hold complex parameters for complicated commands. Besides being holders of values, they check for errors in settings and allow the dynamic generation of values.

.. currentmodule:: tottest.parameters

.. autosummary:: 
   :toctree: parameters_api

   iperf_client_parameters
   iperf_common_parameters
   iperf_common_tcp_parameters
   iperf_server_parameters

Since the parameters define the behavior of commands, choosing them declares their behavior, much as the choice and ordering of the tools defines the behavior of the Test Operator. 

Parsers
-------

.. currentmodule:: tottest.parsers

.. autosummary::
   :toctree: parsers_api

   iperfexpressions
   iperfparser
   oatbran
   sumparser
   unitconverter

Proletarians
------------

The **Proletarians** contains modules to run the test. They are the civil-servants of the system -- modules that shouldn't change for different types of tests.

.. currentmodule:: tottest.proletarians

.. autosummary::
   :toctree: proletarian_api

   argumentparser
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

The **Threads** are used by the logwatchers and connections so they don't block execution (these aren't actually used at run-time, they're for debugging).

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

