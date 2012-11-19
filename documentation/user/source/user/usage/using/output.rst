The Expected Output
===================

Screen Output
-------------

An example of normal output was given in :ref:`normaloutput` but here I'll go over a little more detail of what you're seeing.

Log Output
~~~~~~~~~~

An example of a line from a logging statement would be::

   INFO: [2012-05-24 15:20:41,324] -- Disabling the Radio

There are three main parts to it the screen output:

.. csv-table:: Log Lines
   :header: Description, Meaning
   
   Level, One of INFO or WARNING or Error
   Timestamp, the date and time 
   Message, A string describing what the event was or some learned information

The purpose of the output is primarily to give the |APE| feedback as to what the running program is doing. If you look in the `timetorecovertest.log` file you'll see that it's much noisier. Looking at the example given above in the log you'll find::

    INFO,timetorecovertest.tools.setupiteration.SetupIteration,MainThread,run,Line: 44,2012-05-24:15:20:41,Disabling the Radio

Print Statements
~~~~~~~~~~~~~~~~

The only print statements right now are the sleep countdown statements::

   Sleeping for 5 seconds.

Which are there just to assure you that something is going on.

Crashes
~~~~~~~

We also looked at this output in :ref:`crashing` but I thought I'd cover how to interpret the lines.

The first line::

    Traceback (most recent call last):

Indicates that all the indented lines that follow are the actual commands that were executed up to the point of the crash. Each command gets two lines:

    #. The location of the file where the code exists, the line number in the file, and the name of the function (method)
    #. the actual line of code that was executed.

Since python is an interpreted language these stack-traces are often a good indicator of what was going on in the program at the time of the crash. This might seem something only the programmer would be interested in, but since we're doing systems-work, often the causes of the crash will be external to the program and getting to recognize the correllations betweeen the points of failure and the behavior of the device can be helpful in building a mental model of its behavior.

The last line::

    ConnectionError: Unable to create an SL4A connection: [Errno 111] Connection refused

Is the error that killed the program. If you look at the stack-trace you'll notice that the last thing called was the command to emit this error. This is because it was created by me in the program itself. If an external library or the python interpreter had raised the error, then the last line of the stack-trace would instead be the call that caused the error.

File Output
-----------

While the screen output is important for the operator of the `ttr`, the actual purpose of the test is to provide data for customer. This is accomplished by creating two sets of files:

    * data files
    * log-files

Data
~~~~

In the case of the `ttr` the only data being reported is the time from the enabling of the radio until the first of a specified set of pings. The prefix to the file is set in the config file, but to make it easier to find when searching, the suffix is standardized to `_data.csv` (so the full name would have the form `<prefix>_data.csv`).

Logs
~~~~

Although there is the option to turn off logging, it would be a bad idea to do so. While the request from the customer is generally to find the summary-statistic that represents the represents performance (e.g. the median of the `_data.csv` column), correllation between behavior and the data can only be provided by the logs.

kmsg
++++

The kmsg log is the `kernel-message` log. It provides the logging messages that kernel-modules produce, and thus gives low-level information about the hardware. The timestamps are given as the time from the kernel startup, so they're difficult to map to the time of day. Interestingly, though, you can see the logcat logs being started::

    <6>[    1.932922] logger: created 64K log 'log_main'
    <6>[    1.937713] logger: created 256K log 'log_events'
    <6>[    1.942810] logger: created 128K log 'log_radio'
    <6>[    1.947814] logger: created 64K log 'log_system'
    <6>[    1.954711] logger: created 128K log 'log_metrics'
    <6>[    1.961029] logger: created 64K log 'log_amazon_main'

So you could get some idea of the times being referenced by looking at the logcat timestamps and using an offset (perhaps, I don't know this for sure).

Logcat
++++++

You can read about adb in general and the logcat buffers in particular at google's `android developers <http://developer.android.com/guide/developing/tools/adb.html#logcatoptions>`_ website. The logcat includes both system and application logging (as well as time-of-day timestamps) so can provide a fairly useful picture of what the android is doing during the test. To make it easier to find relevant section, the `ttr` injects messages into the logcat log.

The start of a test::

    05-24 16:01:58.527 V/SCRIPT  (20904): **** ALLION: Starting Repetition 1 of 2 ****

The end of a single test::

    05-24 18:01:59.331 V/SCRIPT  (11154): **** ALLION: Time to Ping = 2.68113303185 ****

The end of a test cycle (i.e. all the repetitions)::

    05-24 16:02:26.933 V/SCRIPT  (20904): **** ALLION: Ending test - elapsed time = 0:00:28.582029 ****

The `elapsed time` is how long all the repetitions took to complete (it's also at the end of the `timetorecovertest.log` file) and is meant to help in estimating how long these tests will take with a given device.

timetorecovertest.log
+++++++++++++++++++++

This is meant to help with debugging the program, but it also contains the data we record (time to ping, time for the entire test, etc.) as well as information about what the adb shell is outputting in response to our requests and so can also be used to build a picture of what happened, or to reconstruct the data file if necessary. The following would extract all the ping times::

    grep Time-To-Recover timetorecovertest.log



