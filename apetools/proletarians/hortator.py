# Copyright 2012 Russell Nakamura
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.'
"""
A module to hold an exhorter of operators
"""

# python Libraries
from datetime import datetime as clock
from collections import namedtuple

# apetools Libraries
from apetools.baseclass import BaseClass
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
        self.operations = operators
        self.last_operator = None
        return

    
    def __call__(self):
        """
        Runs the operators
        """
        start = clock.now()

        crash_times = []
        #import pudb;pudb.set_trace()
        for operation_count, operation in enumerate(self.operations):
            operation_start = clock.now()
            try:
                operation()
            except OperatorError as error:
                crash_time = clock.now()
                self.logger.error(error)
                crash_times.append(CrashRecord(id=operation_count,
                                               start_time=operation_start,
                                               error=error,
                                               crash_time=crash_time))
            except KeyboardInterrupt:
                self.logger.warning("Oh, I am slain.")
                return
           
        end = clock.now()
        for crash in crash_times:
            print str(crash)
        self.logger.info(ELAPSED_TIME.format(t=end - start))
        return

# end class Hortator
