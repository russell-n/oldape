Hortator
========

A module to hold an exhorter of operators.



CrashRecord
-----------

::

    class CrashRecord(namedtuple("CrashRecord",
                                 "id start_time crash_time error")):
        """
        A CrashRecord holds the crash information for later.
        """
        __slots__ = ()
    
        def __str__(self):
            message = ("Crash Record -- ID: {i}"
                       " Start Time: {s} Crash Time: {c} Error: {e}")
            return message.format(i=self.id,
                                  s=self.start_time,
                                  e=self.error,
                                  c=self.crash_time)
    
    



Hortator
--------

.. uml::

   BaseClass <|-- Hortator

.. module:: apetools.proletarians.hortator
.. autosummary::
   :toctree: api

   Hortator
   Hortator.countdown
   Hortator.__call__

