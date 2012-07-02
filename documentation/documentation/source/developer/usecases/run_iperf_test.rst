Run Iperf Test Use Case
=======================

The Run Iperf Test Use Case is an extension of the the `Run Test` use case.

.. uml::

   left to right direction

   actor APE

   skinparam packageStyle rect

   package RunTest{
   APE -> (Test Throughput From DUT)
   (Test Throughput From DUT) ..> (Setup Session) : <<include>>
   (Test Throughput From DUT) ..> (Run Test) : <<include>>
   (Test Throughput From DUT) ..> (Cleanup Session) : <<include>>
   } 
   package RunIperfTraffic{
   (Run Traffic From DUT) --|> (Run Test)
   (Run Traffic To DUT) --|> (Run Test)
   (Run Traffic To and From DUT) --|> (Run Test)
   (Run Test) ..> (Setup Iperf Test) : <<include>>
   }
