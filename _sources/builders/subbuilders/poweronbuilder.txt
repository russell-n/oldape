The Power On Builder
====================

A module to build a Power On object.



The Power On Configuration Error
--------------------------------

.. uml::

   ConfigurationError <|-- PowerOnConfigurationError

.. module:: apetools.builders.subbuilders.poweronbuilder
.. autosummary::
   :toctree: api

   PowerOnConfigurationError



The Power On Builder Enum
-------------------------

::

    class PowerOnBuilderEnum(object):
        """
        A holder of Synaxxx constants
        """
        __slots__ = ()
        id_switch = "id_switch"
        timeout = 'timeout'
        sleep = "sleep"
    # end class PowerOnBuilderEnums
    
    



The Power On Parameters
-----------------------

::

    class PowerOnParameters(namedtuple("PowerOnParameters",
                                       "identifier switch".split())):
        __slots__ = ()
    
        def __str__(self):
            return "identifier: {0} switch: {1}".format(self.identifier,
                                                        self.switch)
    # end class PowerOnParameters
    
    



The Power On Builder
--------------------

.. uml::

   BaseToolBuilder <|-- PowerOnBuilder

.. autosummary::
   :toctree: api

   PowerOnBuilder
   PowerOnBuilder.synaxxxes
   PowerOnBuilder.clients
   PowerOnBuilder.config_options
   PowerOnBuilder.product
   PowerOnBuilder.parameters
   
