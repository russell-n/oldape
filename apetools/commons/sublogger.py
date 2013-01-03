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
A sub-logger for logs that are sub-sets of the main log.
"""

# python standard library
import logging

# apetools modules
from apetools.log_setter import SCREEN_FORMAT_QUIET, LOG_TIMESTAMP
from apetools import log_setter
from apetools.baseclass import BaseClass


class SubLogger(BaseClass):
    """
    A creator and holder of sub-logs (meant for the Hortator)
    """
    def __init__(self, log_format=SCREEN_FORMAT_QUIET, timestamp=LOG_TIMESTAMP,
                 level=logging.INFO):
        """
        :param:

         - `log_format`: a format string for the logging output
         - `timestamp`: a format string for the logging timestamp
         - `level`: the level of messages to record
        """
        super(SubLogger, self).__init__()
        self.log_format = log_format
        self.timestamp = timestamp
        self.level = level
        self._handlers = None
        return

    @property
    def handlers(self):
        """
        :return: dictionary of name:file-handlers
        """
        if self._handlers is None:
            self._handlers = {}
        return self._handlers

    def add(self, logname, logger=None):
        """
        :param:

         - `logname`: path (name) for the log
         - `logger`: logging instarce to add handler to

        :postcondition: file-handler has been added to logger
        """
        if logger is None:
            logger = log_setter.logger
        handler = self.handlers[logname] = logging.FileHandler(logname)
        handler_format = logging.Formatter(self.log_format)
        handler.setFormatter(handler_format)
        handler.setLevel(self.level)
        logger.addHandler(handler)
        return

    def remove(self, logger=None, logname=None):
        """
        :param:

         - `logname`: name of the log to remove
         - `logger`: logging instance with one of self.handlers

        :postcondition: log removed from logging
        """
        if logger is None:
            logger = log_setter.logger
        try:
            logger.removeHandler(self.handlers[logname])
        except KeyError as error:
            self.logger.debug(error)
            if logname is None and len(self.handlers) == 1:
                logger.removeHandler(self.handlers[self.handlers.keys()[0]])
        return
# end class SubLogger
