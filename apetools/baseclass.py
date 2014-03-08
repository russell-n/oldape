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
A module for base classes that have common methods to inherit.

 * Sets up a logger.
 * Has a run_thread method to wrap run methods meant for threads
"""

import logging

DOT_JOIN = "{0}.{1}"


class BaseClass(object):
    """
    This class holds the minimum common features.
    """
    def __init__(self):
        self._logger = None
        return

    @property
    def logger(self):
        """
        :return: A logging object.
        """
        if self._logger is None:
            self._logger = logging.getLogger(DOT_JOIN.format(self.__module__,
                                  self.__class__.__name__))
        return self._logger
# end BaseClass

class BaseThreadClass(BaseClass):
    """
    Extends the base-class with a run_thread method.
    """
    def __init__(self):
        super(BaseThreadClass, self).__init__()
        self._logger = None
        return

    def run_thread(self, *args, **kwargs):
        """
        To use:

           * define run(*args, **kwargs) in child
           * use self.run_thread as target for thread
        
        :param: Whatever self.run accepts
        :precondition: self.run method exists and is thread-safe
        """
        try:
            self.run(*args, **kwargs)
        except Exception as error:
            import traceback
            self.logger.debug(traceback.format_exc())
            self.logger.error(error)
        return
        
# end BaseThreadClass
