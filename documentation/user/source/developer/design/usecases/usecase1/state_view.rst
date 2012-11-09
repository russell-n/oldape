State View Translation of Use Case 1
====================================

1. The system gets the configuration from the APE.

.. digraph:: Configuration

   rankdir = LR
   "Start" -> "Parse Arguments" [label="clargs"] ;
   "Parse Arguments" -> "" [label="args"]; 

2. The System translates the configuration to parameters

.. digraph:: Parse

   rankdir = LR
   start [label=""]
   start -> "Parse Configuration" [label="args"]
   "Parse Configuration" -> "Translate Configuration" [label="parser"]
   "Translate Configuration" -> "" [label="parameter"]

3. The system builds Components baseed on the parameters.

.. digraph:: Build

   rankdir = LR
   start [label = ""]
   end [label=""]
   start -> "Build Components" [label="parameters"]
   "Build Components" -> end [label="component"]

4. The system connects to the devices.

.. digraph:: Connect

   rankdir=LR
   start [label = ""]
   end [label=""]
   start -> "Connect" [label="connector"]
   "Connect" -> end [label="connection"]

5. The system runs throughput to the DUT.

.. digraph:: Throughput

   rankdir=LR
   start [label = ""]
   end [label=""]
   start -> "Run Throughput" [label="test parameter"]
   "Run Throughput" -> end [label="data"]

6. The data is saved to a file.

.. digraph:: Store

   rankdir=LR
   start [label = ""]
   end [label="Files"]
   start -> "Store Data" [label="data"]
   "Store Data" -> end [label="file"]

7. The logs are copied to the data folder.

.. digraph:: Copy

   rankdir=LR
   start [label = ""]
   end [label="Files"]
   start -> "Copy Logs" [label="log"]
   "Copy Logs" -> end [label="log'"]
