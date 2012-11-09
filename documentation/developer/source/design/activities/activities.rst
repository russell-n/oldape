Activity Diagrams
=================

System Level
------------

.. uml::

   left to right direction

   (*) --> "Setup Session"
   "Setup Session" --> "Run Session"
   "Run Session" --> "Teardown Session"
   "Teardown Session" --> (*)

Setup Session
-----------

.. uml::

   left to right direction   
   skinParam packageStyle rect

   partition SetupSession {
   (*) --> [args.glob] "Translate Configuration"
   "Translate Configuration" --> [parameters] "Build Components"
   }
   "Build Components" --> [TestOperators] "Run Session"
   "Run Session" --> "Teardown Session"
   "Teardown Session" --> (*)

Parse Configuration
-------------------

.. uml::

   left to right direction   
   skinParam packageStyle rect
   
   partition SetupSession {
   (*) --> [args.glob] "Parse Configuration File"
   "Parse Configuration File" --> [Configuration Map Parser] "Build Test Parameters"
   "Build Test Parameters" --> [configuration parameters] "Build Components"
   }

Build Components
----------------

.. uml::

   skinParam packageStyle rect
   
   partition SetupSession {
   (*) --> [args.glob] "Translate Configuration File"
   "Translate Configuration File" --> [configuration parameters] "Build Components"
   "Build Components" --> ===B1===
   ===B1=== --> [parameters.dut] "Build DUT Connection" 
   "Build DUT Connection" --> [DUT Connection] ===B2===
   ===B1=== --> [parameters.tpc] "Build TPC Connection"
   "Build TPC Connection" --> [TPC Connection] ===B2===
   ===B1=== --> [parameters] "Build Test Parameters"
   "Build Test Parameters" --> [test_parameters] ===B3===
   ===B2=== --> [parameters.directions] "Build Iperf Tests"
   "Build Iperf Tests" --> [IperfTests] ===B3===
   ===B3=== --> "Build Test Operators"
   }
   "Build Test Operators" --> [Test Operators] "Run Session"

Run Session
-----------

.. uml::

   left to right direction
   skinParam packageStyle rect

   (*) --> "Setup Session"

   partition RunSession {
   "Setup Session" --> [TestOperators] "Setup Test"
   "Setup Test" --> "Run Test"
   "Run Test" --> "Teardown Test"
   "Teardown Test" --> "Setup Test"
   }
   "Teardown Test" --> "Teardown Session"
   "Teardown Session" --> (*)


Setup Test
----------

.. uml::

   left to right direction
   skinParam packageStyle rect

   (*) --> "Setup Session"
   partition SetupTest {
   "Setup Session" --> [parameters.test_id] "Get Test"
   }
   "Get Test" --> [test] "Run Test"
   "Run Test" --> "Teardown Session" 
   "Teardown Session" --> (*)

Run Test
--------

.. uml::

   skinParam packageStyle rect

   (*) --> "Setup Session"
   "Setup Session" --> [parameters] "Setup Test"

   partition RunTest {
   "Setup Test" --> "Kill All Iperf Processes"
   "Kill All Iperf Processes" --> ===B1===
   ===B1=== --> [parameters.IperfServerParameters] "Start Iperf Server"
   ===B1=== --> [parameters.time_to_recover] "Wait"
   "Wait" --> [parameters.IperfClientParameters] "Run Iperf Client"
   "Run Iperf Client" --> ===B2===
   "Start Iperf Server" --> ===B2===
   }
   ===B2=== --> "Teardown Session" 
   "Teardown Session" --> (*)

Teardown Session
----------------

.. uml::

   skinParam packageStyle rect

   (*) --> "Setup Session"
   "Setup Session" --> "Run Session"
   
   partition TeardownSession {
   "Run Session" --> "Copy Configuration"
   "Copy Configuration" --> "Copy Log"
   }
   "Copy Log" --> (*)
