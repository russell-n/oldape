Rotate Configuration
====================

.. _rotate-configuration:

This explains the `[ROTATE]` section of a configuration file. It assumes that there is a PC connected to the turntable with the `rotate` command installed on it.

Contents:

   * :ref:`Setting up the TEST Section <rotate-configuration-test-section>`

   * :ref:`Setting up the ROTATE Section <rotate-configuration-rotate-section>`

.. _rotate-configuration-test-section:

The TEST Section
----------------

To be included as part of the execution you need to add the `rotate` to one of the TEST fields. The recommended location would be the `setup_test` option (if you put it in `execute_test` option the angle information won't get added to file names). If you wanted to rotate the table and run `iperf`, for instance, you might use::

   [TEST]
   setup_test = rotate
   execute_test = iperf

As always, you can add more things to the options using a comma-separated list. For example, to sleep after every rotation::

   [TEST]
   setup_test = rotate, sleep
   execute_test = iperf

Just remember that everthing added to this section needs a corresponding section later in the configuration file with a capitalized version of the option as a header. For example, this setup will expect ``[SLEEP]``, ``[ROTATE]``, and ``[IPERF]`` sections somewhere in the configuration file.

.. _rotate-configuration-rotate-section:

The ROTATE Section
------------------

An example setup would be::

   [ROTATE]
   hostname = phoridfly
   username = root
   #password = 
   angles = 180,0:50,45,90:100, 270:10


* the `angles` format is angles=<comma-separated list of <angle in degrees>:<angular velocity>

* The <angular velocity> is optional (e.g. angles=0,45,90 or angles=0:100, 45:50, 90)

* Negative numbers rotate clockwise (depending on the table)

* The PC connected to the turntable to control it is assumed to have an SSH connection to it so the first three parameters are to log in to it


The Tables
----------

There are two-tables that this is meant to work with -- a servo-based turntable (currently at Allion Labs) and a motor-based one (Cynthia Lane). 

The servo-based turntable won't rotate as far or with as fine a degree of separation between changes in angle and it uses absolute angles (so there's no such thing as a direction, it will always turn clockwise if the chosen angle is less than the current angle or anti-clockwise if the chosen angle is greater than the current one).

.. warning:: The motor-based turntable has a finer-degree of control and will spin forever. If you are going to run more than one cycle then you should make the first or last angle negative so that it will revolve in the opposite direction. Otherwise whatever sits on the table will continue to rotate in the same direction, likely tangling whatever cables are attached to it.

For example, to rotate the table at 90 degree angles with the default speed::

   [ROTATE]
   hostname = phoridfly
   username = root
   #password = 
   angles = 90, 180, 270, -0

.. note:: The `password` is commented out because I normally use public-key authentication. If this isn't set up un-comment the line and add your login password.
