"""
The central tendency is the `middle` of a dataset.
"""
import random
from math import modf
from itertools import repeat

#import numpypy as numpy
#except ImportError:
#import numpy
TWO = SQUARED = 2
TWO_F = 2.0
SQUARE_ROOT = 0.5
PERCENT = 1/100.0

class CentralTendency(object):
    """
    The central tendency stores data and reports the median and mean
    """
    def __init__(self, bootstraps=200, z_score=1.96, precision=4):
        """
        :param:

         - `bootstraps`: the number of bootstrap samples to take to calculate the error
         - `z_score`: the multiplier for the confidence level
         - `precision`: number of decmal places for the string representation
        """
        self.bootstraps = bootstraps
        self.z_score = z_score
        self.precision = precision
        self._data = None
        self._median = None
        self._median_error = None
        self._mean = None
        self._sample_deviation = None
        self.sorted = False
        return

    @property
    def data(self):
        """
        :return: a list
        """
        if self._data is None:
            self._data = []
        return self._data
    
    @property
    def median(self):
        """
        :return: the median value for the data
        """
        if not self.sorted:
            self.data.sort()
            self.sorted = True
        return self.percentile(self.data)

    def percentile(self, data, k=50):
        k *= PERCENT
        remainder, quotient = modf(len(data) *k)
        quotient = int(quotient)
        if remainder:
            return data[quotient]
        return (data[quotient]+ data[quotient - 1])/TWO_F

    @property
    def median_error(self):
        """
        :return: bootstrapped error
        """
        choose = random.choice
        data = self.data
        std = self._std
        length = len(self.data)
        bootstraps = repeat(None, self.bootstraps)
        median = self.percentile
        return std([median([choose(data) for n in repeat(None, length)]) for b in bootstraps]) * self.z_score

    
    @property
    def mean(self):
        """
        :return: the mean of the data set
        """
        return self.meanaverage(self.data)

    def meanaverage(self, data):
        """
        :param:

         - `data`: a list or array

        :return: the mean of the data
        """
        return sum(data)/float(len(data))

    @property
    def sample_deviation(self):
        """
        :return: sample standard deviation for the data set
        """
        return self._std(self.data)
    
    def _std(self, data):
        """
        :param:

         - `data`: a list or array
         
        :return: standard deviation of the data
        """
        count = float(len(data)) - 1
        xbar = self.meanaverage(data)
        
        return (sum([(x - xbar)**SQUARED for x in data])/count)**SQUARE_ROOT
    
    def __call__(self, value):
        """
        :param:

         - `value`: a datum to add to the data
        """
        self.data.append(value)
        self.sorted = False
        return

    def add(self, value):
        """
        An alias for __call__ for backwards compatibility
        """
        self(value)
        return

    def reset(self):
        """
        :postcondition:

         - `data` is None
         - `tail` = 0
        """
        self.tail = 0
        self._data = None
        return
    
    def __str__(self):
        base = ",".join(["{{{i}:.{p}f}}".format(i=index,p=self.precision) for index in range(4)])
        return base.format(self.mean, self.sample_deviation, self.median, self.median_error)
# end class CentralTendency
