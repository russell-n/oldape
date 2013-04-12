Iperf Configuration
===================

The Iperf Configuration section begins with the `[IPERF]` header (case-sensitive) and generally uses the long-parameter names for iperf as the names of the options. For example, to set the target ip you might use::

   iperf --client 192.168.10.25

This would correspond to an option::

    client = 192.168.10.25

The only non-iperf options are the `directions`::

   directions = from_dut, to_dut

Only the first letter is checked (except for `t` as it's ambiguous) so you can use whatever mnemonics help (e.g. 'receive' will only be read as 'r').

This means that traffic from the TPC -> DUT can start with one of:

   * to
   * d
   * r  

(e.g `to_dut`, `downlink`, `receive`, `rx` will all do the same thing.)

Traffic from the DUT -> TPC can start with one of:

    * f
    * u
    * tr
    * tx
    * s  

(e.g. `from_dut`, `uplink`, `transmit`, `tx`, `send` are all equivalente).

This is a plural property so you can have more than one if you use comma-separation (e.g. 'tx, rx', will run traffic from the Node to the Traffic PC then reverse directions).

The Common Options
------------------

Most tests at Allion use a common subset of options:

..

   time = <time>

The default here is seconds, but you can use suffixes to change it (days, hours, minutes, or seconds). e.g. to run it for 2 days, 3 hours and 22 minutes you could use::

   time = 2 days 3 hours 22 minutes

..

   protocol = tcp
   window = 256K
   len = 1470

   parallel = 4

   interval = 1
   format = b

The last flag can be one of:

   * b (for bits/second)
   * k (for kilobits/second)
   * m (for megabits/second)
   * K (for KiloBytes/second)
   * M (for MegaBytes/second)
