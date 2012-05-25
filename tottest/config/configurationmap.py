"""
An extension of the ConfigParser to do conversions
"""
#python
import ConfigParser
from string import whitespace

# timetorecovertest Libraries
from timetorecovertest.baseclass import BaseClass
from timetorecovertest.commons.errors import ConfigurationError

STRIP_LIST = "'\"" + whitespace
EMPTY_STRING = ''
DAY_STRING = 'day'
MINUTE_STRING = 'm'
HOUR_STRING = 'h'
SECOND_STRING = 'second'
COMMA = ','
FORWARD_SLASH = '/'

MINUTES = 60
HOURS = 60 * MINUTES
DAYS = 24 * HOURS


class ConfigurationMap(BaseClass):
    """
    The ConfigurationMap is a variant of SafeConfigParser that adds some extra methods
    """
    def __init__(self, filename, *args, **kwargs):
        """
        :param:

         - `filename`: The name of the config file.
        """
        super(ConfigurationMap, self).__init__(*args, **kwargs)
        self.filename = filename
        self._parser = None
        return

    @property
    def parser(self):
        """
        :return: SafeConfigParser
        """
        if self._parser is None:
            self._parser = ConfigParser.SafeConfigParser()
            self._parser.readfp(open(self.filename))
        return self._parser

    def raise_error(self, error):
        self.logger.error(error)
        raise ConfigurationError(error)
    
    def get(self, section, option, default=None):
        """
        Convenience function:strip off extra quotes and whitespace after 'get'.

        :param:

         - `section`: The [section] name
         - `option`: the option in the section
         - `default`: returns default on error

        :raise: ConfigurationError if the section or option doesn't exist and no default
        """
        try:
            value = self.parser.get(section, option)
            return value.strip(STRIP_LIST)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError, AttributeError) as error:
            if default is not None:
                return default
            self.raise_error(error)

    def get_optional(self, section, option, default=None):
        """
        Convenience function:strip off extra quotes and whitespace after 'get'.

        :param:

         - `section`: The [section] name
         - `option`: the option in the section
         - `default`: returns default on error

        :raise: ConfigurationError if the section or option doesn't exist and no default
        """
        try:
            value = self.parser.get(section, option)
            return value.strip(STRIP_LIST)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError, AttributeError) as error:
            self.logger.debug(error)
            return default
        
    def get_boolean(self, section, option, default=None):
        """
        :raise: ConfigurationError if default not given on error
        """
        try:
            return self.parser.getboolean(section, option)
        except (ConfigParser.NoOptionError,ValueError) as error:
            if default is not None:
                return default
            self.raise_error(error)


    def get_int(self, section, option, default=None):
        """
        :raise: ConfigurationError if default not given on error
        """
        try:
            return self.parser.getint(section, option)
        except (ValueError, ConfigParser.NoOptionError) as error:
            if default is not None:
                return default
            self.raise_error(error)

        
    def get_float(self, section, option, default=None):
        """
        :raise: ConfigurationError if option not found or can't be coerced to float.
        """
        try:
            return self.parser.getfloat(section, option)
        except (ValueError, ConfigParser.NoOptionError) as error:
            if default is not None:
                return default
            self.raise_error(error)

    def get_string(self, section, option, default=EMPTY_STRING):
        """
        :return: value string or default
        """
        value_string = self.get(section, option)
        if value_string is None:
            return default
        return value_string
        
    def get_list(self, section, option, delimiter=COMMA, optional=False):
        """
        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `delimiter`: the value separator
         - `optional` if True, returns None instead of raising an error
        :return: list of strings stripped of whitespace

        :raises: ConfigurationError if not optional and not found.
        """
        if not optional:
            values = self.get(section, option)
            return [value.strip(STRIP_LIST) for value in values.split(delimiter)]
        else:
            try:
                values = self.get_optional(section, option)
                return [value.strip(STRIP_LIST) for value in values.split(delimiter)]
            except AttributeError:
                return None


    def has_option(self, section, option):
        return self.parser.has_option(section, option)

    def get_times(self, section, option):
        """
        Gets a list then converts the values to times.
        """
        times = self.get_list(section, option)
        return [self.time_in_seconds(time_with_units) for time_with_units in times]

    def get_time(self, section, option):
        """
        :param:

         - `section`: A section in the config file (e.g. TEST)
         - `option`: An option in the section in the config file.

        :rtype: int or float
        :return: Value in the option (in seconds) or 0 if not present.
        """
        if not self.has_option(section, option):
            return 0

        value = self.get(section, option)
        return self.time_in_seconds(value)
    
    def time_in_seconds(self, time_with_units):
        """
        :return: time_with_units converted to seconds
        """
        time_with_units = time_with_units.lower()
        tokens = time_with_units.split()
        if len(tokens) == 1:
            return float(tokens[0])

        total = 0
        for index, token in enumerate(tokens):
            if DAY_STRING in token:
                total += float(tokens[index - 1]) * DAYS
                continue

            if HOUR_STRING in token:
                total += float(tokens[index - 1]) * HOURS
                continue

            if MINUTE_STRING in token:
                total += float(tokens[index - 1]) * MINUTES
                continue

            elif SECOND_STRING in token:
                total += float(tokens[index - 1])
        return total

# end ConfigurationMap
