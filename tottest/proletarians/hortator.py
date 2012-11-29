"""
A module to hold an exhorter of operators
"""

# python Libraries
from datetime import datetime as clock
from collections import namedtuple

# tottest Libraries
from tottest.baseclass import BaseClass
from errors import OperatorError

ELAPSED_TIME = 'Elapsed Time: {t}'

class CrashRecord(namedtuple("CrashRecord",  "id start_time crash_time error")):
    """
    A CrashRecord holds the crash information for later.
    """
    __slots__ = ()

    def __str__(self):
        return "Crash Record -- ID: {i} Start Time: {s} Crash Time: {c} Error: {e}".format(i=self.id,
                                                                                   s=self.start_time,
                                                                                   e=self.error,
                                                                                   c=self.crash_time)

class Hortator(BaseClass):
    """
    A builder builds objects.
    """
    def __init__(self, operators, *args, **kwargs):
        """
        :param:

         - `operators`: An iterator of operators
        """
        super(Hortator, self).__init__(*args, **kwargs)
        self.operators = operators
        return

    def __call__(self):
        """
        Runs the operators
        """
        start = clock.now()
        operation = 0
        crash_times = []

        for operator in self.operators:
            operation += 1
            operation_start = clock.now()
            try:
                operator()
            except OperatorError as error:
                crash_time = clock.now()
                self.logger.error(error)
                crash_times.append(CrashRecord(id=operation,
                                               start_time=operation_start,
                                               error=error,
                                               crash_time=crash_time))
        end = clock.now()
        for crash in crash_times:
            print str(crash)
        self.logger.info(ELAPSED_TIME.format(t=end - start))
        return
# end class Hortator
