Time To Recovery Builder
========================

A module to build time-to-recovery tools.



The Time To Recovery Builder Enum
---------------------------------

::

    class TimeToRecoveryBuilderEnum(object):
        __slots__ = ()
        nodes = 'nodes'
        target = 'target'
        timeout = "timeout"
        threshold = "threshold"
    # end class TimeToRecoveryBuilderEnum
    
    



The Time To Recovery Builder
----------------------------

.. uml::

   BaseToolBuilder <|-- TimeToRecoveryBuilder

.. module:: apetools.builders.subbuilders.timetorecoverybuilder
.. autosummary::
   :toctree: api

   TimeToRecoveryBuilder
   TimeToRecoveryBuilder.section
   TimeToRecoveryBuilder.timeout
   TimeToRecoveryBuilder.threshold
   TimeToRecoveryBuilder.target
   TimeToRecoveryBuilder.ttr
   TimeToRecoveryBuilder.product
   TimeToRecoveryBuilder.parameters
   TimeToRecoveryBuilder.add_parameter

