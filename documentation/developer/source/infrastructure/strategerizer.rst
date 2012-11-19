Strategerizer
=============

The Strategerizer holds the strategies that decide the path of execution.

.. uml::

   Strategerizer o-- ConfigFetcher
   Strategerizer o-- SetUp
   Strategerizer o-- TearDown
   Strategerizer o-- CrashHandler
   Strategerizer o-- Helper
   Strategerizer: fetch(args)
   Strategerizer: run(args)
   Strategerizer: help(args)
   Strategerizer: test(args)

The `run` method expects `args` to have a `glob` attribute, the help message expects `args` to have a `topic` attribute.

See :ref:`strategerizerrun` for run algorithm.
