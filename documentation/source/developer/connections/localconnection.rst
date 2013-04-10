=================
 LocalConnection
=================

A LocalConnection takes a command as a procedure call and sends it to the local shell.

e.g. to get the local `iperf` help string (which gets sent to stderr)::

    lc = LocalConnection()
    outerr = lc.iperf('-h')
    print outerr.error

.. uml::

   LocalConnection: String command_prefix
   LocalConnection: <command>(String arguments, Float timeout)

When you use the command, if you leave the timeout as None (the default), the output will be file-buffered, but 
if you give it some kind of timeout, it will act line-buffered.

LocalNixConnection
------------------

A LocalNixConnection overrides the run() method in the LocalConnection to use pexpect instead of subprocess.
