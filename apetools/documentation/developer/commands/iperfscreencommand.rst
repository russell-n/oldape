The Iperf Screen Command
========================

This is a more generalized iPad hack.

Problem
-------

* The iPad only has a WiFi (command-line) interface

* The requirement is to reserve WiFi traffic to testing (while measuring iperf throughput)

* The output of the UDP server has to be preserved (as well as the client-side for TCP)

A Possible Sequence
-------------------

#. Open an SSH Connection to the iPad (via its wireless interface)

#. Use `top` to find any existing `iperf` sessions

#. Use `kill` to kill any `iperf` sessions found

#. Run the `iperf` command on the iPad, re-redirecting the output to a file

#. Close the ssh-connection? 

    * If it's run in screen this doesn't seem necessary

    * Can you just redirect the daemon output and close the connection?

#. Run iperf traffic

#. Open the connection to the iPad

#. Use `top` to find any iperf sessions on the iPad

#. Use `kill` to kill any iperf sessions found

#. Use `scp` to copy the output of the iperf session to the control PC

Components
----------

 * SSHConnection

 * TopCommand

 * KillAll

 * IperfScreenCommand

 * IperfCommand

 * ScpCommand

.. uml::

   IperfScreenCommand : 
