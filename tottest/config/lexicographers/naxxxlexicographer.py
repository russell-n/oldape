"""
A sub-lexicographer for naxxx options
"""
from tottest.baseclass import BaseClass
from tottest.config import config_options

ConfigOptions = config_options.ConfigOptions
DELIMITER = ','


class NaxxxLexicographer(BaseClass):
    """
    The NaxxxLexicographer converts a configuration map to naxxx parameters
    """
    def __init__(self, parser):
        """
        :param:

         - `parser`: A ConfigurationMap
        """
        super(NaxxxLexicographer, self).__init__()
        self.parser = parser
        self._switches = None
        self._hostname = None
        self._section = None
        return

    @property
    def section(self):
        """
        :return: The section name in the config file for the naxxx parameters
        """
        if self._section is None:
            self._section = ConfigOptions.naxxx_section
        return self._section

    @property
    def switches(self):
        """
        :rtype: List of Integers
        :return: switches or None if parser doesn't have section-option pair
        """
        if self._switches is None:            
            option = ConfigOptions.switches_option
            self._switches = self.parser.get_ranges(self.section,
                                                    option, optional=True)
        return self._switches

    @property
    def hostname(self):
        """
        :return: The ip address or hostname of the naxxx or None
        """
        if self._hostname is None:
            option = ConfigOptions.hostname_option
            self._hostname = self.parser.get_optional(self.section,
                                                      option)
        return self._hostname
# end class NaxxxLexicographer
