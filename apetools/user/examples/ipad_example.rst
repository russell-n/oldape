IPad Throughput Example
=======================

.. _ipad-example:

.. note:: To make it easier to read it will be assumed that there is an ssh-alias setup where `IPAD` is equivalent to `<login>@<address>` for the Ipad (with the correct login and IP address substituted).

Unique Features
---------------

Devices meeting the following conditions should be able to use this example:

 * no control of the device during testing 

 * iperf server started on the device external to the code

Example Cases
~~~~~~~~~~~~~

 * Ipad: only has wifi interface which we want to be reserved for the iperf traffic

 * Embedded Devices: At least one device was shipped to us with an iperf server running continuously on it

The Pre-Requisites
------------------

This assumes that the following are True with regards to the IPad:

   * It has a running ssh-server

   * `iperf` is installed on the non-interactive path. Check the path with::

         ssh IPAD 'echo $PATH'

Additionally it is helpful to have `top` installed on the IPad in case you want to stop the iperf server.

The Process
-----------

The first step might seem a little abstract so see :ref:`the example <example-ipad-config-file>` below.

1. Edit the config file:

   #. The [TEST] section can only have `iperf` or other components that don't interact with the Ipad

   #. The [NODE] option for the ipad need to have `connection:dummy` and `test_address:<ipad address>`

   #. The [IPERF] section can only have `directions = to_dut` or `rx` or any other download equivalent


2. Start the server on the ipad::

      ssh IPAD 'iperf -sD > /dev/null'


3. Run the APE::

      ape run

.. note:: If you find it hard to remember the iperf flags you can also use ``iperf --server --daemon > /dev/null``

.. note:: If you want to save the output replace ``/dev/null`` with a file-name (e.g. ``ssh IPAD 'iperf -sD > ipad.iperf'``)

Killing Iperf
-------------

If you've installed `top` then you should be able to kill it by doing the following:

#. Get the process ID::

      ssh IPAD 'top -l 1' | grep iperf

#. Note the *process ID* (the first number of the line).

#. Kill the process::

      ssh IPAD kill <process id>

.. note:: you could also do this interactively, this is just the way I work

.. _example-ipad-config-file:

Example Config File
-------------------

.. highlight:: ini

To setup a test that only ran traffic to the ipad you could use a configuration like the following::

   [TEST]
   execute_test = iperf
   output_folder = iperf_hack_test_{t}
   repeat = 2
   recovery_time = 1 Second

   [NODES]
   ipad = operating_system:linux,connection:dummy,test_address:192.168.20.53

   [TRAFFIC_PC]
   tpc = operating_system:linux,connection:ssh,test_interface:eth3,hostname:localhost,login:allion

   [IPERF]
   directions = to_dut

   time = 1 Hour 5 Seconds

   protocol = tcp
   window = 256K
   len = 1470
   parallel = 1
   interval = 1
   format = b

.. note:: You can add other components if they don't interact with the |DUT| (e.g. `rotate`). If you get an error saying that it wants the `test_interface` for the |DUT| you likely have a component in the configuration that expects to be able to talk to the device.

.. warning:: Although it might not be intuitive to set the operating-system to **linux** at the moment that's just the one that has been implemented so far. Since we don't interact with the device it doesn't have to be something more sensible.
