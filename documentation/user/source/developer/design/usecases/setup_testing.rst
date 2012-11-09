Setup Session
=============

`Setup Session` is an included use case within the `Test Throughput` case.

.. uml::

   left to right direction
   (Test Throughput) ..> (Setup Session) : <<include>>

Related Requirements
--------------------

* |A1|
* |A2|

Precondition
------------

The APE has setup a well-formed configuration file

Postcondition
-------------

The system is ready to start a Test

Failed Condition
----------------

The system has exited without starting a test.

Trigger
-------

The |APE| has executed the `tot run` subcommand.

Main Path
---------

#. The System converts the config file to runtime parameters.
#. The System builds runtime components based on the parameters.

1.1. The System detects a misconfigured or missing required option.

   1.1.1. The System raises a `ConfigurationError`

   1.1.2. The System exits.

.. include:: ../requirements_source.rst
