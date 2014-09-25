Naxxx Builder
=============

A module to build a naxxx object.



Naxxx Configuration Error
-------------------------

.. uml::

   ConfigurationError <|-- NaxxxConfigurationError

.. module:: apetools.builders.subbuilders.naxxxbuilder
.. autosummary::
   :toctree: api

   NaxxxConfigurationError



Naxxx Builder Constants
-----------------------

::

    class NaxxxBuilderEnum(object):
        """
        A holder of Synaxxx constants
        """
        __slots__ = ()
        hostname = "hostname"
        name = 'naxxx'
    # end class NaxxxBuilderEnums
    
    



Naxxx Parameters
----------------

::

    class NaxxxParameters(namedtuple("NaxxxParameters",
                                       "identifier switch".split())):
        __slots__ = ()
    
        def __str__(self):
            return "identifier: {1} switch: {0}".format(','.join(self.switch, s
    elf.identifier))
    # end class PowerOnParameters
    
    



The NaxxxBuilder
----------------

.. uml::

   BaseToolBuilder <|-- NaxxxBuilder
   NaxxxBuilder o- ConfigurationMap
   NaxxxBuilder o- Naxxx

.. autosummary::
   :toctree: api

   NaxxxBuilder
   NaxxxBuilder.hostname
   NaxxxBuilder.config_options
   NaxxxBuilder.product
   NaxxxBuilder.parameters


