PowerOn Configuration
=====================

.. _poweron-configuration:

The `[POWERON]` section setsup control of a (synacces) networked power supply, used currently to turn AP's on or off. It expects the installation of the `poweron` command on the control PC.:

   [POWERON]
   wndr3700 = hostname:synaxxx,switch:1, sleep:5
   
The left-hand-side is only an identifier (that will be added to the output file) so you know what was turned on. The `hostname` is the IP address of the power switch, the `switch` is the number of the power outlet on the switch and the `sleep` is the number of seconds to sleep between commands. This last parameter was added because some of the switches raise errors if you don't wait for them to finish. To queue a set of power-on commands you would add more options::

   [POWERON]
   wndr3700_center = hostname:synaxxx_center,switch:1, sleep:5
   wndr3700_middle = hostname:synaxxx_middle,switch:1, sleep:5
   wndr3700_edge = hostname:synaxxx_edge,switch:1, sleep:5

This will cycle through the switches for testing, turning off all but one switch at a time.
