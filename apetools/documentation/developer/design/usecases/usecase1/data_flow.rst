Data Flow Model
===============

System Level
------------

.. digraph:: systemdata

   rankdir=LR
   start [label="APE", shape="box"]
   end [label="Files", shape="box"]
   start -> "System" [label="args"]
   "System" -> end [label="file"]

Strategy Level
--------------

This is contained within `SetUp.run(args.glob)`.

.. digraph:: strategydata

   rankdir=LR
   start [label="", shape="box"]
   end [label="", shape="box"]
   start -> "Lexicographer" [label="args.glob"]
   "Lexicographer" -> "Builder" [label="StaticParameters"]
   "Builder" -> end [label="Hortator"]

