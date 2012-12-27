Iperf Timestamp Pipeline
========================

Introduction
------------

 * Problem: All the data-files need to be time-stamped by the control-PC in order for the data to be alignable.

 * Question: *Can the* |APE| *be modified so that timestamps are added to the iperf output so that the data-files can be aligned later?*

 * Background: Previously this had been done as a pipeline, however it was never tested with parsed output and edge-conditions where the output begins to fail.

 * Hypothesis: Yes

Possible Solutions
------------------

 * Timestamp the raw-iperf before it is saved

 * Timestamp the parsed iperf before it is saved

 * Use the log to create a time-stamped iperf set after the fact


+-------------------+------------------+--------------------+-----------------------------+
|Solution           |Pros              |Cons                |Fixes                        |
+===================+==================+====================+=============================+
|Timestamp Raw Iperf|* simple change   |* extra files       |* don't save un-timestamped  |
|                   |                  |                    |files                        |
+-------------------+------------------+--------------------+-----------------------------+
|                   |* matches logs    |* won't parse       | * update the iperf-lexer to |
|                   |                  |                    |get timestamps               |
+-------------------+------------------+--------------------+-----------------------------+
|Timestamp Parsed   |* Creates Pipeline|* Most Work         |* Standardize Pipeline       |
+-------------------+------------------+--------------------+-----------------------------+
|                   |* Creates user    |* Edge-cases may    |* test and create driver to  |
|                   |artifact          |break               |fill in NA casese            |
+-------------------+------------------+--------------------+-----------------------------+
|Log-Based          |* Process is      |* Creates single    |* make log-splitter command  |
|                   |generalizable     |file                |                             |
+-------------------+------------------+--------------------+-----------------------------+
|                   |* Can be done with|* No user artifacts |* Make how-to for user to    |
|                   |bash commands     |                    |learn to create              |
+-------------------+------------------+--------------------+-----------------------------+
|                   |* No extra files  |* won't parse       |* Update IperfLexer          |
+-------------------+------------------+--------------------+-----------------------------+
|                   |* Separates       |* Multiple tests    |* Move the log at the end of |
|                   |processing from   |will be in the same |each test                    |
|                   |collecting        |file                |                             |
+-------------------+------------------+--------------------+-----------------------------+

Procedure
---------

+------------------------------+-----+---------------+
|Step                          |State|Completion Date|
+==============================+=====+===============+
|Move Log at end of each test  |     |               |
+------------------------------+-----+---------------+
|Make generic log find/split   |     |               |
|command                       |     |               |
+------------------------------+-----+---------------+
|Update IperfLexer to handle   |     |               |
|time-stamped output           |     |               |
+------------------------------+-----+---------------+
|Create output-pipeline for    |     |               |
|live iperf transforms         |     |               |
+------------------------------+-----+---------------+


Data
----

This is what was observed


Result
------

This illustrates what happened.

Tables
~~~~~~

This is where summary statistics go.

Figures
~~~~~~~

This is where plots, diagrams and illustrations go.

Observations
~~~~~~~~~~~~

This is where a summation of things observed goes.

