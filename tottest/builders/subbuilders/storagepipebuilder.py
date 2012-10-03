"""
A builder of storage pipes
"""
from tottest.lexicographers.config_options import ConfigOptions
from tottest.pipes.storagepipe import StoragePipe, StoragePipeEnum



class StoragePipeBuilder(object):
    """
    A class to build storage pipes.
    """
    def __init__(self, config_map, target=None, role=StoragePipeEnum.pipe,
                 header_token=None):
        """
        :param:

         - `config_map`: A loaded Configuration Map
         - `target`: Target to pipe output to if not a sink
         - `role`: a role to identify the type of pipe
         - `header_token`: token for the header if needed
        """
        self.config_map = config_map
        self.target = target
        self.role = role
        self.header_token = header_token
        self._pipe = None
        self._path = None
        return

    @property
    def path(self):
        """
        :return: the folder to send output to
        """
        if self._path is None:
            self._path = self.config_map(ConfigOptions.test_section,
                                         ConfigOptions.output_folder_option)
        return self._path

    @property
    def pipe(self):
        """
        :return: A storage pipe
        """
        if self._pipe is None:
            self._pipe = StoragePipe(path=self.path,
                                     target=self.target,
                                     header_token=self.header_token,
                                     role=self.role)
        return self._pipe
# end class StoragePipeBuilder
