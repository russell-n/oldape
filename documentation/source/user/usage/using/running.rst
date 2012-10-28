Running a TTR Test
==================

The `ttr` Command
-----------------

When you install the `timetorecovery` library it creates a command called `ttr`. `ttr fetch` was covered in :ref:`configfile` section, here we cover `ttr run`. The basic syntax is::

    ttr run [<file glob>]

The file-glob is optional. By default it will search for any file matching the `*.ini` pattern in a single directory and execute the test declared in it, so in most cases running the test means::

    ttr run

The Glob
~~~~~~~~

If you're not familar with the term `glob` it means that it accepts wildcards in the name (e.g. `*` for 'match anything'). In order to facilitate multiple configurations, the `ttr` will read all the files that match the glob and execute their configurations one at a time. Since the `ttr` copies the config file used to the data folder at the end of the test, the `glob` will only work within a single directory (by default the one you're in when the command is given) rather than searching in sub-directories, to prevent these copied configurations from being executed. If you do have a sub-directory of configuration files, you should be able to pass in the path (relative or fully-qualified), but this hasn't been thoroughly tested.


Screen Output
-------------

There are three levels of output:

    #. Normal
    #. Debug
    #. Silent

.. _normaloutput:

Normal Output
~~~~~~~~~~~~~

The normal level of output will send logging output to the screen if it is at the info, warning, or error levels. This means you should normally only see messages when some event has occurred - e.g. when the radio is enabled, disabled, or the ping has succeeded (there is extra noise for the sleeps between execution in order to let you know the program hasn't hung).

An example output from one test.

.. code-block:: bash

   INFO: [2012-05-24 15:20:41,291] -- Estimated time Remaining: 0:00:13.034415
   INFO: [2012-05-24 15:20:41,292] -- **** ALLION: Starting Repetition 2 of 2 ****
   INFO: [2012-05-24 15:20:41,324] -- Disabling the Radio
   INFO: [2012-05-24 15:20:41,376] -- Waiting for the Device to stop responding
   INFO: [2012-05-24 15:20:42,655] -- Sleeping for 5 seconds
   Sleeping for 5 seconds.
   Sleeping for 4 seconds.
   Sleeping for 3 seconds.
   Sleeping for 2 seconds.
   Sleeping for 1 seconds.
   INFO: [2012-05-24 15:20:47,660] -- Enabling Wifi
   INFO: [2012-05-24 15:20:47,774] -- Waiting for the device to recover
   INFO: [2012-05-24 15:20:50,137] -- Pinged target
   INFO: [2012-05-24 15:20:50,484] -- Time-To-Recover: 2.36312699318
   INFO: [2012-05-24 15:20:50,485] -- Sleeping for 5 seconds
   Sleeping for 5 seconds.
   Sleeping for 4 seconds.
   Sleeping for 3 seconds.
   Sleeping for 2 seconds.
   Sleeping for 1 seconds.

Silent Output
~~~~~~~~~~~~~

If you run it in silent mode::

    ttr -s run

It will suppress all the output except for the `Sleeping for` print statements. Those should probably go away too, but silent is actually a command for the logger, not the program itself.

Debug Output
~~~~~~~~~~~~

If you run it in Debug mode::

    ttr -d run

it will include debug messages intended for use when debugging the program. In this case since the test is relatively simple you'll mostly see a lot of ping messages.

**Note:**

The `-s` and `-d` flags are `ttr` options, not `ttr run` options, so they have to come after the `ttr`. Putting them at the end of the command::

    ttr run -d

will result in an error message.


.. _errorsvscrashing:

Errors versus Crashes
---------------------

Once the program is running (i.e. you got past the command-line syntax) errors are considered cases where something in the test happened that was unexpected by one component of the program but aren't something that should stop execution. A crash is something that happened that was unexpected by the whole program or was caused by something that is interpreted as being fatal to the test. For example, if the `logs` option in the config file is missing, the parser might consider that an error, but because the program as a whole knows it isn't required it isn't considered fatal. If, on the other hand, the ping `target` option is missing or the connection to the device has died, then this is considered a fatal error and the program will crash

It might not seem sensible to let the program crash, but the intention is to bring it to the notice of the |APE| as soon as possible, so that it can be remedied.


What to do if it Crashes
~~~~~~~~~~~~~~~~~~~~~~~~

See if you understand the error message the last line of the crash report.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The following is an example from a test of a JEM device that spontaneously rebooted during testing.

.. literalinclude:: crashreport.log

The last line indicates that the SL4A connection died (but you'll see later that this doesn't mean quite what it seems). This usually indicates a problem with the DUT and isn't recoverable programattically because even if you re-start the server, you can't forward the port inside of a program.

Test the connection
+++++++++++++++++++

As mentioned before, there is a test command that exercises the main points of failure for the program when talking to the DUT. First make sure the radio is on (the crash might have happened during the *disable* phase of the test in which case it won't be on). If the radio is on, run the setup test::

    ttr test

SL4A Problems
`````````````

If it is a problem with SL4A you'll probably see something like this:

.. literalinclude:: sl4acrash.rst

It might seem obscure if you're used to reading stack-traces, but the line near the bottom that ends with `android.py", line 46, in _rpc` is referring to the module that communicates with the SL4A server on the DUT.

The first thing to do is to try to re-forward the ports::

    source source_this_for_sl4a

Then re-test::

    ttr-test

If that doesn't work you can try going into the GUI and killing the server:

    #. Touch the top bar to bring down the notifications window
    #. Tap the `SL4A Server` bar (it usually stands out because it has a white background)
    #. On the screen that comes up, touch the `Server` entry (it will have `127.0.0.1:` followed by a port number in it)

Then try to re-start the server again. 

ADB Problems
````````````
The following is the output after I killed the ADB server.

.. literalinclude:: adbcrash.rst

What you might notice is that it only mentions that there was an SL4A problem, not an adb problem. They telling thing is that there's no mention of `android.py`. This is because if the `adb` connection is dead, `android.py` won't let you use it (whereas if the ADB connection is alive but the SL4A server is dead, it will let you use it, but then it will crash). Still, this is admittedly obscure so before even trying to interpret the output you should test the connections with some kind of adb command::

    adb shell ls

When I tried this the server started itself and then executed the `ls` command, but the `ttr test` still failed because when the ADB server died, so did the port-forwarding of the SL4A server. Re-doing `source source_this_for_sl4a` made it work again.

Other Problems
``````````````

If testing the DUT by hand seems to be working and you think it's a programming problem, zip or tar up everything (especially `crashreport.log`, `timetorecovertest.log`, the config file and the `logcat` log) then post a `bug report <https://bitbucket.org/allion_software_developers/timetorecovery/issues?status=new&status=open>`_ and upload the file. Then go complain to Taka, he likes it when people to that.

