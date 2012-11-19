"""
A module to fetch config files.

The ConfigFetcher within copies the config file to the current working directory.

It was built to be used to pick config files from a folder of different files,
but if it gets no parameters, it will load whatever is set as the DEFAULTS
in the `config.constants` module.
"""

# Python libraries
import os
import shutil

# tottest Libraries
import tottest.baseclass as baseclass
from constants import CONFIG_FOLDER, DEFAULTS

INI_EXTENSION = '.ini'


class ConfigFetcher(baseclass.BaseClass):
    """
    A class to fetch config files.
    """
    def __init__(self, name=None, config_folder=None, *args, **kwargs):
        """
        :param:

         - `name`: The name of the test whose config-file is being fetched.
         - `config_folder`: The path to the folder .
        """
        super(ConfigFetcher, self).__init__(*args, **kwargs)
        self.name = name
        self._folder_path = None
        self._config_folder_path = None
        self.config_folder_path = config_folder
        return

    @property
    def folder_path(self):
        """
        :rtype: String
        :return: The path to the parent main `testrunner` folder.
        """
        if self._folder_path is None:
            module = __import__(__package__)
            self._folder_path = module.__path__[0]
        return self._folder_path

    @property
    def config_folder_path(self):
        """
        :rtype: String
        :return: The path to the config files
        """
        if self._config_folder_path is None:
            sub_folder = CONFIG_FOLDER
            self._config_folder_path = os.path.join(self.folder_path, sub_folder)
        return self._config_folder_path

    @config_folder_path.setter
    def config_folder_path(self, path):
        """
        :param:

         - `path`: The path to a config_folder
        """
        self._config_folder_path = path
        return

    def config_names(self):
        """
        generates config file names

        :yield: .ini file name
        """
        for file_name in os.listdir(self.config_folder_path):
            if file_name in DEFAULTS:
                yield file_name
        return

    def fetch_config(self):
        """
        Copies the .ini file to the current working directory.

        """
        self.logger.info("Fetching Config file.")
            
        for file_name in self.config_names():
            shutil.copy(os.path.join(self.config_folder_path,
                                     file_name), os.getcwd())
            
        return
# End class ConfigFetcher
