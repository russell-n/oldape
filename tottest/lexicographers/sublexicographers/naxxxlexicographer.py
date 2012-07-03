"""
A sub-lexicographer for naxxx options
"""
from collections import namedtuple

from tottest.baseclass import BaseClass
from tottest.lexicographers import config_options
from tottest.affectors.elexol import networkedpowersupply
from tottest.commons import errors
from tottest.commons import enumerations

MAX_PINS = networkedpowersupply.MAX_PINS
ConfigOptions = config_options.ConfigOptions
DELIMITER = ','
SWITCHES = [str(index) for index in range(MAX_PINS)]
ConfigurationError = errors.ConfigurationError
AffectorTypes = enumerations.AffectorTypes

class NaxxxParameters(namedtuple("NaxxxParameters", "type switch name")):
    """
    NaxxxParameters hold the parameters for the Naxxx
    """
    __slots__ = ()

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return "switch_{0}".format(self.switch)

    def __int__(self):
        return int(self.switch)
# end class NaxxxParameters


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
        self._switches_names = None
        self._type = AffectorTypes.naxxx
        return

    @property
    def section(self):
        """
        :return: The section name in the config file for the naxxx parameters
        """
        if self._section is None:
            self._section = ConfigOptions.affector_section
        return self._section

    @property
    def switches_names(self):
        """
        :return: NaxxxParameters
        """
        if self._switches_names is None:
            self._switches_names = []
            
            for switch in SWITCHES:
                name = self.parser.get_optional(self.section,
                                                switch)
                if name is not None:
                    self._switches_names.append(NaxxxParameters(type=self._type,
                                                                name=name,
                                                                switch=switch))
        return self._switches_names

    @property
    def switches(self):
        """
        :rtype: List of Integers
        :return: switches or None if parser doesn't have section-option pair
        """
        if self._switches is None:
            try:
                self._switches = self.switches_names
            except ConfigurationError:
                option = ConfigOptions.switches_option
                self._switches = []
                switches = self.parser.get_ranges(self.section,
                                                  option, optional=True)
                for switch in switches:
                    self._switches.append(NaxxxParameters(type=self._type,
                                                          name=None,
                                                          switch=switch))
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
