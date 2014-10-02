
# python Libraries
from datetime import datetime as clock
from datetime import timedelta

# apetools Libraries
from apetools.baseclass import BaseClass
from data import Data


class CountdownTimer(BaseClass):
    """
    A countdown timer keeps track of time Remaining.
    """
    def __init__(self, repetitions, *args, **kwargs):
        """
        :param:

         - `repetitions`: The total number of repetitions to be run
        """
        super(CountdownTimer, self).__init__(*args, **kwargs)
        self.total_repetitions = repetitions
        
        self.current_repetition = 0
        self.start = None
        self.lap_start = None
        
        self._lap_times = None
        self._remaining_time = None
        self._median_laptime = None
        self._remaining_repetitions = None
        self._total_time = None
        return

    @property
    def lap_times(self):
        """
        :rtype: Data
        :return: sorted list of lap-times (timedeltas)
        """
        if self._lap_times is None:
            self._lap_times = Data()
        return self._lap_times
    
    @property
    def remaining_time(self):
        """
        calls next_laptime(), calculates remaining time
        
        :rtype: datetime.timedelta
        :return: median laptime x remaining repetitions
        """
        self.next_laptime()
        return self.median_laptime * self.remaining_repetitions

    @property
    def total_time(self):
        """
        :rtype: datetime.timedelta
        :return: Total elapsed time since the timer was started
        """
        return clock.now() - self.start

    @property
    def median_laptime(self):
        """
        :rtype: datetime.timedelta
        :return: median of self.lap_times (based on total_seconds)
        """
        return timedelta(seconds=self.lap_times.median)

    @property
    def remaining_repetitions(self):
        """
        :rtype: IntegerType
        :return: total - current repetition
        """
        return self.total_repetitions - self.current_repetition
    
    def next_laptime(self):
        """
        #. appends a timedelta for now-lap_start to lap_times
        #. sets lap_start to now
        #. increments current_repetition
        """
        now = clock.now()
        self.lap_times.insert((now - self.lap_start).total_seconds())
        self.lap_start = now
        self.current_repetition += 1
        return

    def start_timer(self):
        """
        Sets the lap_start and start to now() and current_repetition to 1
        """
        self.start = self.lap_start = clock.now()
        self.current_repetition = 0
        return
# end class CountdownTimer
