Rotate Builder
==============

A module to build a rotate object.

::

    COLON = ":"
    
    class RotateBuilderEnums(object):
        """
        A holder of Rotate constants
        """
        __slots__ = ()
        angle_velocity = 'angle_velocity'
    # end class RotateBuilderEnums
    
    



Rotate Parameters
-----------------

The RotateParameters is a named tuple that should be passed into the RotateCommand's call method.

.. '

::

    class RotateParameters(namedtuple("RotateParameters", "angle velocity clock
    wise".split())):
        __slots__ = ()
    
        def __str__(self):
            return "angle: {0} velocity: {1} clockwise: {2}".format(self.angle,
     self.velocity,
                                                                    self.clockw
    ise)
    # end class RotateParameters
    
    



RotateBuilder
-------------

The RotateBuilder builds the RotateCommand.

.. uml::

   BaseToolBuilder <|-- RotateBuilder

   
.. module:: apetools.builders.subbuilders.rotatebuilder
.. autosummary::
   :toctree: api

   RotateBuilder
   RotateBuilder.connections_parameters
   RotateBuilder.connections
   RotateBuilder.angles
   RotateBuilder.velocities
   RotateBuilder.parameters
   RotateBuilder.product

