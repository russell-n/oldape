
The Iperf Command
=================
A module to hold a generic iperf command.

.. currentmodule:: apetools.commands.iperfcommand


Errors Raised
-------------

.. _iperf-error:

IperfError
~~~~~~~~~~

The `IperfError` is raised if a problem with the connection between the client and server is detected.

.. uml::

   IperfError -|> CommandError

.. autosummary::
   :toctree: api

   IperfError



IperfCommandError
~~~~~~~~~~~~~~~~~

The `IperfCommandError` is raised if an error in the command-string is detected.

.. uml::

   IperfCommandError -|> ConfigurationError

.. autosummary::
   :toctree: api

   IperfCommandError



The Iperf Command Enum
----------------------

The `IperfCommandEnum` holds string constants for the :ref:`IperfCommand <iperf-command>`.

.. uml::

   IperfCommandEnum : client
   IperfCommandEnum : server
   IperfCommandEnum : time
   IperfCommandEnum : eof
   IperfCommandEnum : newline
   IperfCommandEnum : udp
   IperfCommandEnum : path
   IperfCommandEnum : iperf




.. _iperf-command:

The Iperf Command
-----------------

The `IperfCommand` executes iperf commands. This is very old code so it is not well-documented.


Daemon Mode
~~~~~~~~~~~

The most recent change is a check for the `--daemon` flag in the parameters. If this is there, then it is assumed that the server will want to start, redirect the output to a file, then close the connection to the device. Another object will then have to kill the iperf process and copy it if the output is wanted. This is being implemented speciffically for the `ipad` running downlink iperf traffic. It probably will not work in other cases.

Because the server is running in a thread, it will set a ``self.last_filename`` property so that users will know where to get the remote file.

.. autosummary::
   :toctree: api

   IperfCommand

.. uml::

   IperfCommand -|> BaseThreadClass
   IperfCommand o-- StoragePipe
   IperfCommand : parameters
   IperfCommand : output
   IperfCommand : role
   IperfCommand : base_filename
   IperfCommand : raw_iperf
   IperfCommand : parser
   IperfCommand : run(device, filename, server)
   IperfCommand : start(device, filename)
   IperfCommand : __call__(device, filename, server)
   IperfCommand : last_filename
   IperfCommand : is_daemon



The `run` Method
----------------

There are two parts to the `IperfCommand.run` method:

   #. Setup
   
   #. Traverse

Setup
~~~~~

The setup involves the following steps:

   #. Add tags to the filename to make it easier to identify::

       filename = self.filename(filename, device.role)

   #. Turn off the output pipeline's screen output so the parser can do it instead::

       self.output.unset_emit()

   #. Open an output file using the updated filename::

       file_output = self.output(filename = filename)

   #. Wait for the connection lock (in case others have the connection) and run the command::

       with device.connection.lock:
           output, error = device.connection.iperf(str(self.parameters))

   #. Calculate start and end times and set the current state to running::

       start_time = time()
       abort_time = start_time + self.max_time
       self.running = True

* The ``self.max_time`` property is used so that a different value can be returned depending on whethe this is a server of client.
       
Traverse
~~~~~~~~

The traversal of the output has three paths:

   #. The main path

   #. The abort (timeout) path

   #. The (external) stop path

The Main Path
+++++++++++++

The main path is a traversal of the output from the command call::

   for line in ValidatingOutput(output, self.validate):
       self.send_line(file_output, line)

The ``send_line`` method traps `StopIteration` exceptions which the would be raised when the output pipeline detects an end-of-file character.

The Abort Path
++++++++++++++

Sometimes devices will stop generating output without quitting and so the `standard-output` will raise a `timeout` forever without reaching an end-of-file character. To prevent this from blocking a timeout is calculated which takes precedence over the end-of-file if it is reached. This is only set for the client, since the server is normally run in a thread.

The abort path is implemented as an extension of the main path (it immediately follows the `send_line` call)::

    if self.now() > abort_time:
        self.send_line(end_of_file)
        raise IperfError("aborting")

This is an abbreviation, the actual error-message is longer. The reason for the ``now`` method is that in the case that this is a server we do not want to actually calculate a real time.

The Stop Path
+++++++++++++

The stop path is reached if an external agent has asked us to stop. Note that for servers if this call is made after all the output has been read then it will be stuck waiting for the next-line and will reach the stop only on the resumption of output. This is probably not the desired outcome. It would be better to kill the iperf process itself, otherwise you will have a condition where you are trying to consume all the output and then setting stop immediately between the last line read and before reaching the top of the loop again.

Experiments with sending control characters to standard-in seem to indicate that it will not kill the server. However, closing the connection will. 

..
    if self.stop:
        # someone has asked us to stop (stop path)
        self.send_line(end_of_file)
        self.stop = False
        self.logger.debug("Aborting")
        break
    
The Cleanup
-----------

After the standard output traversal is completed the `running` state is set to False and standard-error is checked.

.. warning:: If the `abort` or `stop` paths were taken, there is no guarantee that the standard-error is ready to be read. This needs to be made more robust.


The code::

    self.running = False    
    err = error.readline(timeout=1)        
    if len(err):
        self.validate(err)
    

Example Use::

   iperf_client = IperfCommand(client_parameters, output, IperfCommandEnum.client)
   iperf_server = IperfCommand(server_parameters, output, IperfCommandEnum.server)
   iperf_server.start(server_device, 'test_file')
   iperf_client(client_device, 'test_file')
   
Testing The Iperf Command
-------------------------

.. autosummary::
   :toctree: api

   TestIperfCommand.test_daemon
   TestIperfCommand.test_is_daemon
   TestIperfCommand.test_set_parameters








