Setting up the TTR Test
=======================

System Topology
---------------

Assuming everything is installed and the ADB connection is up and running your system should look something like the `Puppeteer Topology` (I made that up, but I think it seems appropriate).

.. graph:: topology

   rankdir="LR";
   P -- D [style="dashed"];
   D -- A [style="dotted"];
   A -- T;
   
.. csv-table:: Graph Key
   :header: Key, Meaning
   
   P, Puppet PC (attached ADB Control)
   D, DUT
   A, Access Point
   T, Target of ping
   \- \-, USB Connection
   . ., Wireless Connection


Setting up the Hardware
-----------------------

#. Start the ADB Server and root it::

    sudo adb start-server; adb wait-for-device root

#. Start the SL4A server.

    * do it the `manual way <http://code.google.com/p/android-scripting/wiki/RemoteControl>`_
    * or you can use a convenience script::

        ttr fetch
        source source_this_for_sl4a

#. Connect the DUT to the AP via the GUI

#. Set the DUT to not sleep (via Applications -> Developer if available, otherwise use the Display settings to keep the screen on)

    * If you use the Display Settings to keep the screen on, it might help the battery to dim the screen fully.

See the next section for more explanation of the `ttr fetch` sub-command.

.. _configfile:

The Config File
---------------

The config file is the main interface between the Performance Evaluator and the `ttr` program (it is in some respects a declarative program that alters the `ttr` at runtime). To get a sample config-file you use the `fetch` subcommand::

    ttr fetch

This will place four files in your current working directory.

.. csv-table:: The Four Files
   :header: Name, Description

   `ttr.ini`, The configuration file for the test.
   `source_this_for_sl4a`, A file to start the server and forward the port (see the previous section)
   `readme_useme_loveme`, A file to help you remember what the `source_this_for_sl4a file` is for.
   `timetorecovertest.log`, An artifact of the running `ttr` program. At this point it shouldn't have anything interesting.

ttr.ini
~~~~~~~

The config file uses the `ini <http://code.google.com/p/android-scripting/wiki/RemoteControl>`_ file formatting - sections are placed in square brackest (`[SECTION_NAME]`) and values are set using the syntax `name = value`. Python also allows you to use a colon (`:`) instead of an equals sign (`=`) but I'll stick to the equals-sign here. You could probably get away with not changing anything (assuming you're on the 192.168.20 subnet), and hopefully understanding the intent of the test makes the configuration settings self-explanatory, but I'll go over them to clarify what they are.

[TEST]
++++++

The test section holds values to specify the running of the test.

.. csv-table:: The Test-Section Options
   :header: Option, Meaning

   `output_folder` , The sub-folder where the data files and logs will be placed.
   `data_file` , The name of the file with the time-to-recovery data in it (it will automatically get a `_data.csv` suffix to indicate which file it is
   `repeat`, The number of times to repeat the test
   `recovery_time`, The time to wait after disabling the radio and after the test is done to let the device settle down.
   `timeout` , The maximum amount of time to try and ping the target before giving up and running the next test (the data file will get `None` as the time-to-recovery entry)
   `threshold`, The number of consecutive pings to consider a true change in state (the first ping's time is kept, but all the pings have to go through for it to be reported).
   `criteria` , If this time is reached a `Failure` message is inserted into the `Logcat` log to make identifying the failed tests a little easier.
   `target`, The address to ping

[DUT]
+++++

This isn't used as much for this test as it is in other tests. It's primarily used by the `ttr test` sub-command to check the IP address of the DUT:

.. csv-table:: The Dut-Section Options
   :header: Option, Meaning

   `wifi_interface`,The name of the interface as recognized by `ifconfig` on the DUT

[LOGWATCHER]
++++++++++++

This is where you identify the log-file to watch. Since it's set up for the `/proc/kmsg` file, it assumes the file will block when it's read, rather than returning an end-of-file character. By commenting out the option (e.g. `#logs =/proc/kmsg`)  -- not the section header - that will raise an error -- you can disable this feature. The ability to disable it was added because on an `AirPad` that was tested the watching of the log was creating log-entries in the `kmsg` files as a side-effect, making the log ineffective (and really big).

.. csv-table:: The Logwatcher-Section Options
   :header: Option, Meaning

   `logs`, The name(s) of the log(s) to watch.

If there is another log file to cat, you can specify the value as a comma-separated list::

    logs = /proc/kmsg, /dev/log

[LOGCATWATCHER]
+++++++++++++++

This is where the particular logcat buffers to be watched can be specified. If the value is commented out (e.g. `#logs = events, main, radio, system`), the watcher will still run but it will read all the logs listed in the `/dev/log` folder on the android. This option was added because `Lab126` added a couple of logs that need root access to them and this will allow semi-rooted devices to be tested (the original *kindle* allowed installing side-loaded applications, but didn't give full-root priviileges by default).

.. csv-table:: The Logcatwatcher-Section Options
   :header: Option, Meaning

   `logs`, The logcat buffers to watch.

Notes on the Syntax
~~~~~~~~~~~~~~~~~~~

Case-sensitivity
++++++++++++++++

The section and option names are case-sensitive, the values may or may not be, depending on what they are (e.g. if it's the name of the wifi interface it is, if it's the time units, it isn't).

Time Units
++++++++++

For things requiring times, there are four available units:

    #. Days
    #. Hours
    #. Minutes
    #. Seconds

Seconds is the default value so you could leave off the units all-together if you're only giving seconds. The units can be combined (e.g. timeout = 2 Days 5 Hours) but this isn't used often for this test so I haven't rigorously tested all the possible combinations - stick to one and you're safe, use `timeout = 4 Minutes 2 Minutes` and I don't guarantee it will work.

Lists
+++++

You may have noticed that the TEST option `repeat` seems kind of awkward as a name -- `repetitions` seems more natural, given the declarative rather than imperative nature of the configuration file -- but I've adopted a naming convention where plural names mean plural settings are allowed (as comma-separated lists - as with the `logs` options), but singular names mean you can only specify one value.

Testing Your Setup
------------------

Once you've started the servers (adb and SL4A) and have associated the DUT with an AP, you should run the test command.

    `ttr test`

This will try to get the IP address through the adb connection, query the SL4A connection for its wifi address and then ping the target given in the config file (so you have to be in the directory with the config). 

A sample output.

.. literalinclude:: ttrtest.rst

Note that the ping sometimes fails on the first try for some reason. Re-run the test again if it does and if it doesn't ping do a sanity check::

    adb shell ping <target ip>

Where the `<target ip`> is whatever you put in the config file.

