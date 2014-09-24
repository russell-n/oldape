The Builder
===========

A module to hold a builder of objects.

::

    class MagicMock(object):
        def __call__(self):
            print "This is a Mock"
            return
    
        def total_time(self):
            return "I Don't Know"
    # end class MagicMock
    
    



.. module:: apetools.builders.builder
.. autosummary:: 
   :toctree: api

   GeneratorHolder
   GeneratorHolder.__iter__

::

    class BuilderEnum(object):
        """
        A class to hold constants for the builder
        """
        __slots__ = ()
        repetition = 'repetition'
    
    



.. uml::
   
   BaseClass <|-- Builder

.. autosummary::
   :toctree: api

   Builder
   Builder.saved_semaphore
   Builder.semaphore
   Builder.events
   Builder.parameters
   Builder.repetitions
   Builder.operation_setup_builder
   Builder.operation_teardown_builder
   Builder.setup_test_builder
   Builder.execute_test_builder
   Builder.teardown_test_builder
   Builder.nodes
   Builder.thread_nodes
   Builder.build_operator
   Builder.operators
   Builder.hortator
   Builder.tpc_device
   Builder.storage
   Builder.reset

