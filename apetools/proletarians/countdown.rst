Countdown Timer
===============
A countdown timer for the hortators and operators.

::

    class Times(namedtuple("Times", 'days hours minutes seconds'.split())):
        """
        A Times holds the times after seconds are converted to d,h,m,s
        """
        __slots__ = ()
        def __str__(self):
            return "{0} days, {1} hours, {2} minutes, and {3} seconds".format(s
    elf.days,
                                                                              s
    elf.hours,
                                                                              s
    elf.minutes,
                                                                              s
    elf.seconds)
    #end class Times
    
    



.. uml:: 

   BaseClass <|-- CountDown

.. module:: apetools.proletarians.countdown
.. autosummary::
   :toctree: api

   CountDown
   CountDown.elapsed
   CountDown.median
   CountDown.heap
   CountDown.now
   CountDown.start
   CountDown.add
   CountDown.remaining
   CountDown.to_time

