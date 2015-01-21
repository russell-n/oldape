
class SharedCounter(object):
    """
    A counter for classes to share
    """
    def __init__(self, count=0, step=1):
        """
        :param:

         - `count`: initial-value (integer) for counter
         - `step`: amount to increment or decrement
        """
        self.count = count
        self.step = step
        return

    def increment(self):
        """
        :postcondition: self.count incremented by 1 step
        :return: the current value of self.count
        """
        self.count += self.step
        return self.count

    def decrement(self):
        """
        :postcondition: self.count decremented by 1 step
        :return: the current value of self.count
        """
        self.count -= self.step
        return self.count

    def __eq__(self, other):
        """
        :rtype: Boolean
        :return: if self.count equals 'other'
        """
        return self.count == other


    def __str__(self):
        return "Count: {0}".format(self.count)
# end class SharedCounter
