
from bisect import insort


ZERO = 0
ONE = 1
TWO = 2
HALF = 0.5
TWO_FLOAT = 2.0


class Data(object):
    """
    A Data holds data.
    """
    def __init__(self, data=None):
        """
        :param:

         - `data`: An optional list to start the data set.
        """
        self._data = data
        self._median = None
        return

    @property
    def data(self):
        """
        :return: list of data
        """
        if self._data is None:
            self._data = []
        return self._data

    @property
    def median(self):
        """
        :return: The median data value
        """
        x = self.data
        if len(x) % TWO == ZERO:
            # n is even, return mean of middle points
            right = len(x)/TWO
            return (x[right - ONE] + x[right]) * HALF
        # else n is odd, return the middle point
        return x[len(x)/TWO]
    

    def insert(self, datum):
        """
        :param:

         - `datum`: A single numeric value to add to the data.
        """
        insort(self.data, datum)
        return
# end class Data
