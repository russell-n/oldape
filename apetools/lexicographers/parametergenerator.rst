Parameter Generator
===================

A parameter generator maps the lexicographer's static configuration to a set of test parameters. This way a config-file can declare a set: e.g. repetitions=10 and the parameter-generator will create 10 parameter-objects.



TestParameters
--------------


::

    class TestParameter(namedtuple('TestParameter', parameters)):
        """
        A TestParameter holds the settings for a single test-iteration
        """
        __slots__ = ()
    
        def __str__(self):
            return (self.__class__.__name__ + ":" +
                    ','.join(("{f}:{v}".format(f=f, v=getattr(self,f))
                              for f in self._fields)))
    
        
    # end class TestParameter
    
    



Parameter Generator
-------------------

.. uml::
   
   BaseClass <|-- ParameterGenerator

.. module:: apetools.lexicographers.parametergenerator
.. autosummary::
   :toctree: api

   ParameterGenerator
   ParameterGenerator.tree
   ParameterGenerator.__iter__

