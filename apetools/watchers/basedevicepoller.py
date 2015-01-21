
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
