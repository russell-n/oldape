SetUp
=====

A setup builds the Infrastructure.

.. uml::

   SetUp o-- Lexicographer
   SetUp o-- Builder
   SetUp: args
   SetUp: run()

See :ref:`setuprun` for the run algorithm.


The Main Path
-------------

.. digraph:: setuprun

   rankdir="LR";

   "SetUp.run" -> "Lexicographer" [label="arguments.glob"];
   "Lexicographer" -> "Builder" [label="StaticParameters"];
   "Builder" -> "return" [label="Hortator.run"];

