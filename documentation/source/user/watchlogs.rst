Watchlogs Configuration
=======================

The `[WATCHLOGS]` section is used to watch device logs. An example would be::

   [WATCHLOGS]
   logcat = type:adblogcat, buffers:all
   kmsg = type:logcat,command:cat,arguments:/proc/kmsg
   battery = type:battery,name:/sys/class/power_supply/bq27541/uevent
   proc = type:procnetdev,interface:wlan0
   device = type:device
   cpu = type:cpu

* The left-hand-side value is only to make them unique (so they can be anything)

* The type is what decides their type

* The remaining parameters depend on the type

The Types
---------

Since most of the testing has been focused on android-based devices the current log-watchers are based around it, but outside of the `adb-logcat` should work on any linux-based device that supports them.

`adblogcat`
~~~~~~~~~~~

As you might infer, this watches the adb logs. The only parameter it takes is `buffers` to specify with buffers to watch. These are listed in the `/dev/log` folder on the device. To find them use::

    adb shell ls /dev/log

Using `all` as the value (as in the example above) will pull from all the buffers.

`kmsg`
~~~~~~

This pulls the messages from the `/proc/kmsg` file. The proc-file system is available for most linux-based systems (and possibly cygwin) but isn't used on MacOS devices. It also can't be used by default on certain systems unless you login as root (you can use `sudo` in an interactive session but that doesn't work so well when running code).

`battery`
~~~~~~~~~

This records the battery level once a second (ish). This is currently only implemented for androids. The name will change depending on the battery.

`procnetdev`
~~~~~~~~~~~~

This records the `/proc/net/dev` statistics every second. 

`device`
~~~~~~~~

This just pulls whatever the device can give. Typically it grabs `rssi`, and `bitrate`.

