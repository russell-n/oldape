
# python standard library

# the use of call is to overcome a permission problem with the python logger
from subprocess import call
import sys

# this package
from ratetable import RateTable

from apetools.baseclass import BaseClass


class Rotator(BaseClass):
    """
    A reduction of the RateTable class to a single call.
    """
    def __init__(self):
        super(Rotator, self).__init__()
        self._table = None
        return

    @property
    def table(self):
        """
        :return: RateTable control
        """
        if self._table is None:
            self._table = RateTable()
        return self._table

    def __call__(self, angle, velocity=0):
        """
        :param:

         - `angle`: degrees from the home position to rotate to
         - `velocity`: velocity of rotation
        """
        message = "Setting the table angle to: {0} degrees ({1} velocity)".format(angle,
                                                                                  velocity)
        print message
        call(["logger","-i", "ROTATE:", message])
        try:
            self.table.zAxis.setPosition(angle, 0, velocity)
        except (IOError, SystemError) as error:
 	    sys.stderr.write("{0}\n".format(error))
	    if "No such file or directory" in str(error):
	        sys.stderr.write("Is the USB cable plugged in?\n")

	    call(["logger", "-i", "ROTATE:", str(error)])
        return
# end class Rotator
