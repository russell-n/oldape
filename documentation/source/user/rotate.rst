Rotate Configuration
====================

.. _rotate-configuration:

This explains the `[ROTATE]` section of a configuration file. It assumes that there is a PC connected to the turntable with the `rotate` command installed on it.

An example setup would be::

   [ROTATE]
   hostname = phoridfly
   username = root
   #password = 
   angles = 180,0:50,45,90:100, 270:10


* the `angles` format is angles=<comma-separated list of <angle in degrees>:<angular velocity>

* The <angular velocity> is optional (e.g. angles=0,45,90 or angles=0:100, 45:50, 90)

* Negative numbers rotate clockwise (depending on the table)

* The PC connected to the turntable is assumed to have an SSH connection to it so the first three parameters are for it

The Tables
----------

There are two-tables that this is meant to work with -- a servo-based turntable (currently at Allion Labs) and a motor-based one (Cynthia Lane). 

The servo-based turntable won't rotate as far or with as fine a degree of separation between changes in angle and it uses absolute angles (so there's no such thing as a direction, it will always turn clockwise if the chosen angle is less than the current angle or anti-clockwise if the chosen angle is greater than the current one).

The motor-based turntable has a finer-degree of control and will spin forever. Instead of absolute directions it will move always move anti-clockwise unless told to move clockwise, thus if you repeatedly rotate the turn-table it will continue to spin in the same direction until the cabling attached to it breaks or lifts it off the table. To counter this it's helpful to make the last angle a `-0` to reset it. e.g.::

   angles = 90, 180, 270, -0
