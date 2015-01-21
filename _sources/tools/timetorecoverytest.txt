Time To Recovery Test
=====================

A module to hold the time-to-recovery test.

::

    TimeToRecoveryTestParameters = namedtuple("TimeToRecoveryTestParameters",
                                              ['output',
                                              'device',
                                               'time_to_recovery'])
    
    

::

    NEWLINE_STRING = "{0}\n"
    
    



.. uml::

   BaseClass <|-- TimeToRecoveryTest

.. module:: apetools.tools.timetorecoverytest
.. autosummary::
   :toctree: api

   TimeToRecoveryTest
   TimeToRecoveryTest.device
   TimeToRecoveryTest.output    
   TimeToRecoveryTest.time_to_recovery
   TimeToRecoveryTest.run
   TimeToRecoveryTest.save_data
   TimeToRecoveryTest.log_message

