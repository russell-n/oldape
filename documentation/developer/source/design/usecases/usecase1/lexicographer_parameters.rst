Lexicographer Parameters
========================

The Lexicographer generates `StaticParameter` objects from it's `parameters` attribute.

.. digraph:: parameters

   rankdir=LR
   end [label=""]
   "" -> "Lexicographer.init()" [label="args.glob"]
   "Lexicographer.init()" -> "Lexicographer.parameters" [label="file_name"]
   "Lexicographer.parameters" -> end [label="StaticParameters"]


Static Parameters
-----------------

.. uml::

   StaticParameters: config_file_name
   StaticParameters: output_folder
   StaticParameters: data_file_name
   StaticParameters: repetitions
   StaticParameters: tpc_parameters
   StaticParameters: dut_Parameters
   StaticParameters: iperf_client_parameters
   StaticParameters: iperf_server_parameters
   StaticParameters: String __str__() 

Sub-Parameters
--------------

The attributes of the StaticParameters that have the suffix *parameters* are themselves parameter objects.

Connection Parameters
~~~~~~~~~~~~~~~~~~~~~

The following parameters are meant for information about the Traffic PC (TPC) and the Device Under Test (DUT).

.. uml::

   TpcParameters: hostname
   TpcParameters: test_ip
   TpcParameters: username
   TpcParameters: password
   TpcParameters: String __str__()

The `hostname` is meant to be the IP address or resolvable name used to connect to the TPC (likely on the control network). While the `test_ip` is used by the iperf commands. Since this is downlink only, the `test_ip` is never actually used, but that didn't occur to me until after I set it up.

.. uml::

   DutParameters: test_ip
   DutParameters: String __str__()

Iperf Parameters
~~~~~~~~~~~~~~~~

The following parameters are meant for building a `traffic-to-the-dut` test.

.. uml::

   IperfClientParameters: client
   IperfClientParameters: window
   IperfClientParameters: len
   IperfClientParameters: parallel
   IperfClientParameters: interval
   IperfClientParameters: format
   IperfClientParameters: time
   IperfClientParameters: String __str__()

.. uml::

   IperfServerParameters: window
   IperfServerParameters: String __str__()

