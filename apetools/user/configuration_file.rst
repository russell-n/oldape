The Configuration File
======================

.. _configuration-file:

The configuration file is how a particular test or set of test is run. When the `run` sub-command is given::

    ape run

The program will look for any file that matches the file-glob (`*.ini` by default) and execute them in lexicographic order. The configuration files use the `INI <http://en.wikipedia.org/wiki/INI_file>`_ file format.

A sample:

.. toctree::

   Sample <sample_configuration>


The Test Section
----------------

The configuration file is broken into sections, some of which are required, some of which are required only when needed. The first required section is the `[TEST]` section. This is where the parts of the test that will be executed are declared.

The TEST Options
~~~~~~~~~~~~~~~~

There are five option that declare the order that the test-components are run:

    * `operation_setup`

    * `setup_test`

    * `execute_test`

    * `teardown_test`

    * `operation_teardown`

Each of these options takes a comma-separated list that corresponds to a component. See the following sections for examples. If you don't want to use a particular option, comment it out or remove it. 

For example, the following would only run `iperf`::

    [TEST]
    #operation_setup = watchlogs,oscillate
    execute_test = iperf


Operation Setup
+++++++++++++++

The `operation_setup` option is run once per test (conceptually a configuration file corresponds to a single test, so these components will only be run once per file-setup). An example use of this option is to run the `watchlogs` component which captures various logs from devices::

    [TEST]
    operation_setup = watchlogs

Because this component is declared there needs to be a corresponding [WATCHLOGS] section somewhere in the configuration file for this to be a valid setup. The reason for putting `watchlogs` in the `operation_setup` is that the parts of the code that collect the logs run in the background continuously and so don't need to be started with every repetition.

The Setup Test Option
+++++++++++++++++++++

The next option is `setup_test`. Components declared here will be run once for every test repetition. This is more of a conceptual-distinction, as you could put them in the test section. An example would be if you are using a power switch to turn on AP's and want the code to wait until the device has connected to the AP::

    setup_test = poweron,timetorecovery,dumpdevicestate

The `poweron` component will be executed first (and will expect a `[POWERON]` section in the configuration), the `timetorecovery` will ping until there is a connection (or a timeout) and the `dumpdevicestate` will dump whatever information about the state of the device's connection that it can get to the screen and a log-file.

The Execute Test Options
++++++++++++++++++++++++

This is the section where components to actually run the test should go. The most common thing here would be `iperf`::

    execute_test = iperf

As with the previous options, there will need to be an `[IPERF]` section for this to be a valid configuration.

The Teardown Options
--------------------

I think you get the idea for these sections -- `teardown_test` gets run after each `execute_test` and `operation_teardown` gets run after everything else is done.

The Leftover Options
~~~~~~~~~~~~~~~~~~~~

There are also some remaining options in the `[TEST]` section that don't declare components:

   * `output_folder`

   * `repeat`
 
   * `tag`

   * `recovery_time`

   * `no_cleanup`

Output Folder Option
++++++++++++++++++++

Hopefully this is fairly intuitive. The only thing that might not be is the time-stamping option. Anywhere in the string that there's a `{t}` a timestamp will be inserted. For example::

   output_folder = tate_cisco_1250_{t}

Might produce a folder with the name `tate_cisco_1250_2013_04_08`. 

Repeat Option
+++++++++++++

The `repeat` option is how many times to repeat the setup in this configuration file (so the `setup_test`, `execute_test`, and `teardown_test` will be repeated however many times the `repeat` is set to).

Tag Option
++++++++++

The `tag` is a string that will be inserted into the log at the start and end of a test. It's mainly used to decompose the log afterwards via string matching.

Recovery Time
+++++++++++++

This is the number of seconds to rest between tests. This is sort of vestigial at this point.

No Cleanup Option
+++++++++++++++++

If this is chosen the code will exit immediately upon receiving a keyboard interrupt (control-c) without trying to clean up after itself. This is generally not a good thing.

.. _node-configuration:

The Nodes
---------

The next required section is [NODES]. This is where devices that are to be tested are declared. Each device gets its own line. For example::

    [NODES]

    tate = hostname:phoridfly,login:root,operating_system:android,connection:adbshellssh,test_interface:wlan0

The left-hand-side term (`tate` in this case) is only an identifier to make it easier to recognize what's being tested, it doesn't need to be any particular value.

The node options:

   * hostname -- The IP address or resolvable name for the node
   * login -- The user-login name 
   * operating_system -- the OS of the node (see below for valid types)
   * connection -- the way the Control PC connects to the Node
   * test_interface -- the name of the testing interface (used to get the test IP)

The general form for the node declarations are::

    <identifier> = hostname:<ip or name>,login:<user login>,operating_system:<OS>,
        connection:<type>,test_interface:<interface name>

The connection type is one of: 

   * ssh
   * adbshellssh
   * local
   * telnet
   * adblocal
   * serial

The `hostname`, and `login` aren't needed if the connection isn't a remote one.

The operating system is one of: 

   * linux
   * android
   * windows
   * mac

If other options are neede by the connection, add with <name>:<value> format. The only extra option at the moment is `password:<login password>` which is only needed if the public-keys aren't set up between the PC running the code and the Node.

As a rule of thumb, prefer *ssh* over *telnet*, *telnet* over *serial* or *local*.

A MacBook Sample::

   [NODES]
   hostname:macbook,login:allion,password:testlabs,operating_system:mac, connection:ssh, test_interface:en1

.. _traffic-pc:

The Traffic PC
--------------

The next required section is the `[TRAFFIC_PC]`. It uses the same format as the nodes but is used only for the other side of an iperf session.

For example::

   [TRAFFIC_PC]
   tpc = operating_system:linux,connection:ssh,test_interface:eth3,hostname:lancet,login:allion


The Remaining Sections
----------------------

Any other section needed will correspond to one declared in the `[TEST]` section. See specific examples:

.. toctree::
   :maxdepth: 1

   Iperf <iperf>
   Rotate <rotate>
   Watchlogs <watchlogs>
   Sleep <sleep>
   PowerOn <poweron>
   
