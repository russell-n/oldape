The Screen Command
==================

This is an interface to the `GNU screen <http://www.gnu.org/software/screen/>`_ command. Since ``screen`` is meant to be an interactive environment, most of what it can do is beyond what is being used here. The assumption in this case is that there is a device to test that needs to keep a command alive but the connection to the device should be closed. In particular, this is being implemented so that `IOS` devices (e.g the `iPad`) that have an ssh-server can run `iperf` on them, dedicating the wireless interface to the traffic (thus the control computer needs to close its connection to it), and at the same time collect the screen output from the command. 

The main reason for using screen with `iperf`, then is to be able to capture the output. If the output isn't needed an alternative would be to run the server as a daemon.

.. note:: I just tested it and found that unlike ubuntu and android, the ipad will redirect output to a file when iperf is run in `daemon` mode so this is being abandoned for now, as the main use-case has disappeared.


For future reference, the sytax for running screen detached is this::

    screen -d -m bash -c "<command>"

You don't need the extra ``bash -c "<command>"`` in all cases, but when trying to redirect output to a file, the bash interpretern will try and redirect the output of the screen command (and if you just pass `screen` the command in quotes it will try and interpret as a single command, not a command with arguments). 

A concrete example (using ssh to run them on a remote device)::

    ssh tester@ipad screen -d -m bash -c "iperf -s --daemon --udp -i 1 > output.iperf"