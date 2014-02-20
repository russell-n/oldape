IPad UDP Example
================

This documents how to run UDP or TCP traffic to an iPad (it doesn't support *uplink* yet). 

What it Does
------------

#. Starts an `iperf server daemon` on the iPad

#. Closes the SSH-connection to the iPad

#. Runs traffic to the iPad

#. Kills the iperf daemon on the iPad

#. Copies the server output from the iPad to the `raw_iperf` sub-directory

Requirements
------------

To do the above procedure the ipad needs to be rooted and have the following executables installed in the (non-interacive) path:

   * an ssh-server

   * iperf

   * top (to find the iperf process id for the `kill` command)

Setting Up the APE
------------------

As always, the configuration-file is the means to set up the *APE*

   * The `watchlogs` components and other components that interact with the DUT throughout the test should be removed

   * The Iperf directions should be limited to downlink only::

        directions = to_dut

   * The node's ipaddress should be set::

        test_address: 192.168.10.55

   * The node's operating system should change::

        operating_system: ios

   * The Iperf section should have the `daemon` flag set::

        daemon = True

.. warning:: The actual value of the daemon flag isn't checked, the fact that it's declared means it's set to True. This will also set the daemon flag::

   daemon = False

Example Configuration
---------------------

.. highlight:: ini

The following is a minimal example::

    [TEST]
    setup_test = timetorecovery,dumpdevicestate
    execute_test = iperf
    output_folder = ipad_test_{t}
    repeat = 20
    tag = IPADTEST
    recovery_time = 1 Second

    [NODES]
    ipad = hostname:ipad,login:root,operating_system:ios,connection:ssh,test_address:ipad

    [TRAFFIC_PC]
    tpc = operating_system:linux,connection:ssh,test_interface:wlan0,hostname:localhost,login:fakeuser
    
    [IPERF]
    directions = to_dut

    time = 10 Minutes

    protocol = udp
    bandwidth = 100M
    daemon = True

    len = 1470
    parallel = 1
    interval = 1
    format = b


.. note:: The `dumpdevicestate` won't actually return much useful since I couldn't find an `iwconfig` equivalent for `ipad`. If someone finds one it might prove more useful.
