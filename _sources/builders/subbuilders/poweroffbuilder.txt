The Power Off Builder
=====================

A module to build a power-off object.



The PowerOffConfigurationError
------------------------------

.. uml::

   ConfigurationError <|-- PowerOffConfigurationError

.. module:: apetools.builders.subbuilders.poweroffbuilder   

.. autosummary::
   :toctree: api

   PowerOffConfigurationError



The Power Off Builder Enum
--------------------------

::

    class PowerOffBuilderEnum(object):
        """
        A holder of Synaxxx constants
        """
        __slots__ = ()
        id_switch = "id_switch"
    # end class PowerOffBuilderEnums
    
    



The Power Off Parameters
------------------------

::

    class PowerOffParameters(namedtuple("PowerOffParameters", "identifier switc
    h".split())):
        __slots__ = ()
    
        def __str__(self):
            return "identifier: {0} switch: {1}".format(self.identifier,
                                                        self.switch)
    # end class PowerOffParameters
    
    



The Power Off Builder
---------------------

.. uml::

   BaseToolBuilder <|-- PowerOffBuilder
   PowerOffBuilder o- PowerOff

.. autosummary::
   :toctree: api

   PowerOffBuilder
   PowerOffBuilder.synaxxxes
   PowerOffBuilder.clients
   PowerOffBuilder.product
   PowerOffBuilder.parameters
    
