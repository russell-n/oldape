"""
A place for a time-converter.
"""
import re

from apetools.parsers import oatbran
from apetools.baseclass import BaseClass

ZERO = 0
EMPTY_STRING = ""


class TimeConversions(object):
    """
    A class in hold the multiplers for conversion
    """
    __slots__ = ()
    same = 1
    seconds_per_minute = 60
    seconds_per_hour = seconds_per_minute * 60
    seconds_per_day = seconds_per_hour * 24
# end class TimeConversions

class TimeUnits(object):
    """
    An enumerator of sorts for time-units
    """
    days = "d"
    hours = "h"
    minutes = "m"
    seconds = "s"
# end class TimeUnits
    
class TimeConverter(BaseClass):
    """
    The Time Converter converts times
    """
    def __init__(self, units=TimeUnits.seconds):
        """
        :param:

         - `units`: the units to convert to
        """
        super(TimeConverter, self).__init__()
        self.units = units
        self._expressions = None
        self._converter = None
        return

    @property
    def expressions(self):
        """
        :return: expression-based time-tokenizer
        """
        if self._expressions is None:
            self._expressions = TimeConverterExpressions()
        return self._expressions

    @property
    def converter(self):
        """
        :return: <time-prefix><units-prefix>:conversion-factor dictionary
        """
        if self._converter is None:
            self._converter = {TimeUnits.seconds + TimeUnits.seconds:TimeConversions.same,
                               TimeUnits.seconds:TimeConversions.same,
                               TimeUnits.minutes + TimeUnits.seconds:TimeConversions.seconds_per_minute,
                               TimeUnits.hours + TimeUnits.seconds:TimeConversions.seconds_per_hour,
                               TimeUnits.days + TimeUnits.seconds:TimeConversions.seconds_per_day}
        return self._converter

    def __call__(self, source):
        """
        :param:

         - `source`: string that has time-units tokens to convert
        """
        accumulator = 0
        for time_units in self.expressions.tokens(source):
            time = time_units[TimeConverterEnums.time]
            units = time_units[TimeConverterEnums.units]
            print units
            try:
                units_key = units.strip().lower()[0]
            except IndexError as error:
                self.logger.debug(error)
                units_key = EMPTY_STRING
            units_key += self.units
            if self.expressions.float.match(time):
                time = float(time)
            else:
                time = int(time)
            print time
            accumulator += self.converter[units_key] * time
            print units_key, time
        return accumulator
# end class Time Converter

class TimeConverterExpressions(BaseClass):
    """
    A class to hold the regular expressions for the TimeConverter
    """
    def __init__(self, source=None):
        """
        :param:

         - `source`: a string to iterate over and tokenize
        """
        super(TimeConverterExpressions, self).__init__()
        self._time = None
        self._enums = None
        self._seconds = None
        self._minutes = None        
        self._hours = None
        self._days = None
        self._unitless = None
        self._times = None
        self._integer = None
        self._float = None
        self.base_time = oatbran.NAMED(n=self.enums.time,
                                       e=oatbran.REAL)
        self.source = source
        return

    @property
    def float(self):
        """
        This requires a value after the decimal point::

            value = 1.0

        not::

            value = 1.
        
        :return: expression to match a float
        """
        if self._float is None:
            expression = oatbran.FLOAT
            self._float = re.compile(oatbran.NAMED(n=self.enums.float,
                                                   e=expression))
        return self._float

    @property
    def integer(self):

        """
        :return: expression that matches entire line as integer
        """
        if self._integer is None:
            self._integer = re.compile(oatbran.NAMED(n=self.enums.integer,
                                                     e=oatbran.INTEGER))
        return self._integer

    def units(self, prefix):
        """
        :param:

         - `prefix`: the character-class prefix for the units

        :rtype: String
        :return: regular expression to match the units
        """
        return oatbran.NAMED(n=self.enums.units,
                             e=(oatbran.OPTIONAL_SPACES +
                                prefix +
                                oatbran.OPTIONAL_LETTERS))
        
    @property
    def unitless(self):
        """
        :rtype: RegexObject
        :return: compiled expression to match unitless time
        """
        if self._unitless is None:
            self._unitless = re.compile(oatbran.STRING_START +
                                                   oatbran.OPTIONAL_SPACES +
                                                   self.base_time +
                                                   self.units(oatbran.STRING_END))
        return self._unitless

    @property
    def seconds(self):
        """
        :rtype: RegexObject
        :return: compiled expression to match seconds
        """
        if self._seconds is None:
            self._seconds = re.compile(self.base_time +
                                       self.units("[Ss]"))
        return self._seconds

    @property
    def minutes(self):
        """
        :rtype: RegexObject
        :return: compiled expression to match minutes
        """
        if self._minutes is None:
            self._minutes = re.compile(self.base_time +
                                       self.units("[Mm]"))
        return self._minutes

    @property
    def hours(self):
        """
        :rtype: RegexObject
        :return: compiled expression to match hours
        """
        if self._hours is None:
            self._hours = re.compile(self.base_time +
                                     self.units("[Hh]"))
        return self._hours

    @property
    def days(self):
        """
        :rtype: RegexObject
        :return: compiled expression to match days
        """
        if self._days is None:
            self._days = re.compile(self.base_time +
                                    self.units("[Dd]"))
        return self._days

    @property
    def times(self):
        """
        :rtype: tuple
        :return: collection of compiled expression to match times
        """
        if self._times is None:
            self._times = (self.unitless,
                           self.seconds,
                           self.minutes,
                           self.hours,
                           self.days)
        return self._times
        
    @property
    def enums(self):
        """
        :return: SublexicographerEnums
        """
        if self._enums is None:
            self._enums = TimeConverterEnums
        return self._enums
    
    def tokens(self, source):
        """
        Tokenizes a source stream based on `times` property.

        :yield: the next time-token group-dict in `source`
        """
        source = source.strip()
        for expression in self.times:
            match = expression.match(source)
            if match: break
        
        while match is not None:
            if match.start() != ZERO:
                self.logger.warning(source[ZERO:match.start()])
            yield match.groupdict()
            source = source[match.end():]
            source = source.strip()
            for expression in self.times:
                match = expression.match(source)
                if match: break
        return

    def __iter__(self):
        """
        :yield: groupdict for time and units
        """
        for token in self.tokens(self.source):
            yield token
        return
# end class TimeConverterExpressions

class TimeConverterEnums(object):
    """
    A class to hold some constants
    """
    __slots__ = ()
    integer = "integer"
    float = "float"
    time = "time"
    units = 'units'
# end class TimeConverterEnums
