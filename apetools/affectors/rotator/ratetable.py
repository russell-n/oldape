
class RateTable(object):
    """
    Represents the z-axis::

    """
    def setPosition(self, position, direction=0, velocity=0.0):
        """
        Sets the position of the axis in degrees.

        Use::

           r = RateTable.RateTable()
           r.zAxis.setPosition(<angle>, 0, <velocity>)

        :param:

         - `position`: Degrees of rotation relative to the position at powering on (0)
         - `direction`: Always `0`
         - `velocity`: the rate of rotation
        :C++ signature : void setPosition(AxisBridge {lvalue},float [,unsigned char [,float]])
        """
        return
