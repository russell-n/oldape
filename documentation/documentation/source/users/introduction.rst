Introduction
============

Who Is This For?
----------------

This documentation is intended to for Allion Performance Evaluators who need to run a time-to-recovery (ttr) test on a device under test (DUT) using:

    #. toggling of the wifi-radio's state as the failure and recovery
    #. a software interface as the control-element for the wifi-radio

This is also secondarily for developers, as it addresses the intended use of the `ttr`, but there is a developer-specific set of documentation in the mercurial repository along with the source code which can be built (via `Sphinx`) for more detail about how things work, as opposed to how to use this.

What Is This?
-------------

As noted above, this isn't a developers document, this is intended to cover the expected use-cases for the time-to-recovery test. It will cover:

   #. Installation and setup
   #. Using the `ttr` command
   #. The help-system

TTR?
----

In general
~~~~~~~~~~

The Time-To-Recovery is the amount of a device takes to recover from a failure. The mean-time-to-recovery (MTTR) is the average (if the distribution is normal) time to recover after a failure. In this case we are artificially inducing a `failure` by turning the radio off, so it isn't a strictly accurate term, but I wanted a short name to use on the command-line.

How it's used here
~~~~~~~~~~~~~~~~~~

In this case it involves:

   #. Connecting the device to an Access Point (AP)
   #. Disabling the Radio on the DUT
   #. Enabling the Radio on the DUT
   #. Pinging a target from the DUT
   #. Recording how long it takes for the DUT to successfully ping the target (the Point of Recovery)
   
This produces two main data sets:

   #. The times to recovery
   #. The logged events that happened during the recovery

Something to keep in mind
~~~~~~~~~~~~~~~~~~~~~~~~~

The process for the recovery spans multiple layers of the `OSI Model <http://en.wikipedia.org/wiki/OSI_model>`_ and it's sometimes useful to keep the key events and where they sit in the model in mind in order to form a consistent mental picture of what's happening.

802.11 sits at the Physical Layer (Layer 1) and you can track the re-enabling of the radio to the point of association with the AP using the kernel-logs (and usually the system-logs).

`ping` sits at the Network Layer (Layer 3), but if you don't have a static IP address on the DUT you will need to use DHCP to get an address and DHCP sits on the Application Layer (Layer 7). So our collected times using pings encompass more than the time of the DUT's association with the Access Point, they include other parts as well. However if you keep the logs, you can extract the time-to-association separately if you need to.
