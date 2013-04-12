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
#   limitations under the License.
"""
A module to hold the basic device-poller, a watcher that queries the device at specific intervals
"""
# apetools
from basepollster import BasePollster



class BaseDevicePoller(BasePollster):
    """
    An abstract class to base Device-Pollsters on.
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `device`: a device to query
         - `output`: a file to send output to
         - `expression`: an expression to match the output
         - `interval`: time between polling
         - `timestamp`: a timestamp creator
         - `name`: Name to use in the logs
         - `event`: An event which if set starts the polling
         - `use_header`: If True, prepend header to output
        """
        super(BaseDevicePoller, self).__init__(*args, **kwargs)
        self._logger = None        
        return
# end class BaseDevicePoller
    
