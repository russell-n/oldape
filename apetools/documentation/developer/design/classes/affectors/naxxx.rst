The NAXXX
=========

The *NAxxx* is a *Networked Alternating current control switch XXX* (no one under age 17 admitted) adapter.

.. uml::

   NAXXX : NetworkedPowerSupply naxxx
   NAXXX : init(hostname, clear, retries)
   NAXXX : run(outlets)
   NAXXX o-- NetworkedPowerSupply

   NetworkedPowerSupply : String IP
   NetworkedPowerSupply : Boolean clear
   NetworkedPowerSupply : Integer retry
   NetworkedPowerSupply : turn_on_switches(List outlets, Boolean turn_others_off)

.. csv-table:: Exceptions
   :header: Exception,Cause
   
   **NaxxxError** (AffectorError), Unable to connect to the *NAXXX*
   **FaucetteError** (ConfigurationError), Unable to coerce outlets to integers


.. csv-table:: Helper Function
   :header: Label, Value
   
   **Signature**, *_clean_outlets(outlets)*
   **Accepts**, *ListType* *TupleType* or anything which can be cast to an *IntegerType*
   **Returns**,List of integers
   **Raises**, *FaucetteError* if the list can't be built.
