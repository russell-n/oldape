Example Uses
============

.. _ipad-example:

IPad Throughput Example
-----------------------

.. note:: To make it easier to read it will be assumed that there is an ssh-alias setup where `IPAD` is equivalent to `<login>@<address>` for the Ipad (with the correct login and IP address substituted).

Description
~~~~~~~~~~~

This is called the IPad example but it is really for any situation where you can only have one interface to the device and need to stop interacting with it during testing. It can also be used in the cases where you have no control over the iperf server (as has occasionally been the case with embedded devices).

The Pre-Requisites
~~~~~~~~~~~~~~~~~~

This assumes that the following are True with regards to the IPad:

   * It has a running ssh-server

   * `iperf` is installed on the non-interactive path. Check the path with::

         ssh IPAD 'echo $PATH'

Additionally it is helpful to have `top` installed on the IPad in case you want to stop the iperf server.

The Process
~~~~~~~~~~~

The first step might seem a little abstract so see :ref:`the example <example-ipad-config-file>` below.

1. Edit the config file:

   #. The [TEST] section can only have `iperf` or other components that don't interact with the Ipad

   #. The [NODE] option for the ipad need to have `connection:dummy` and `test_address:<ipad address>`

   #. The [IPERF] section can only have `directions = to_dut` or `rx` or any other download equivalent


2. Start the server on the ipad::

      ssh IPAD 'iperf -sD > /dev/null'


3. Run the APE::

      ape run

.. note:: If you forget the iperf flags you can also use ``iperf --server --daemon > /dev/null``

.. note:: If you want to save the output replace ``/dev/null`` with a filename

Killing Iperf
~~~~~~~~~~~~~

If you've installed `top` then you should be able to kill it by doing the following:

#. Get the process ID::

      ssh IPAD 'top -l 1' | grep iperf

#. Note the *process ID* (the first number of the line).

#. Kill the process::

      ssh IPAD kill <process id>

.. note:: you could also do this interactively, this is just the way I work

.. _example-ipad-config-file:

Example Config File
~~~~~~~~~~~~~~~~~~~

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

.. warning:: Although it might not be intuitive to set the operating-system to **linux** at the moment that's just the one that has been implemented so far. Since we don't interact with the device it doesn't have to be something more sensible.
