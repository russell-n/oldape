Time to Recovery Use Case
=========================

The system impels the |DUT| to ping the |TPC| until it succeeds, recording the time of the first success.

.. uml::

   left to right direction

   APE --> (Measure Time To Recovery)

.. uml::

   TimeToRecover: Command ping_command
   TimeToRecover: float time_limit
   TimeToRecover: integer threshold
   TimeToRecover: tuple run()

   TimeToRecover o-- PingCommand

   PingCommand: string target
   PingCommand: Connection connection
   PingCommand: tuple run()

   PingCommand o-- ADBShellConnection

   ADBShellConnection o-- LocaNixConnection

Related Requirements
--------------------

* |A14|
* |A15|

Preconditions
-------------

#. The |DUT| and |TPC| are on the same subnet.
#. The |DUT| is attached to the |CPC| via |ADB|.
#. The |DUT| is in a recovering or ready state.

Postcondition
-------------

Time to first ping is returned calculated.


Main Path
---------

#. DUT pings TPC
#. If ping and is first ping, set first ping time.
#. If ping increment ping count
#. If not ping, set first ping time to none and ping count to 0.
#. If ping count matches threshold, return the time to the first ping.
#. Go to step 1.

.. uml::

   (*) --> "Ping Target"
   if "" then
      --> "Set First Ping Time To None" as reset_time
   else
      if "pinged" then
         --> [first ping] "Set First Ping Time" 
      else
         --> "Increment Ping Count"
      endif
   endif
   reset_time --> "Set Ping Count To 0"   
   "Set Ping Count To 0" --> "Ping Target"
   "Set First Ping Time" --> "Increment Ping Count"
   if "" then
      --> [threshold met | time limit reached] (*)
   else
      --> "Ping Target"

.. include:: ../requirements_source.rst
