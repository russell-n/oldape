Time Converter
==============

A place for a time-converter.



Time Conversions
----------------

::

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
    
    



Time Units
----------

::

    class TimeUnits(object):
        """
        An enumerator of sorts for time-units
        """
        days = "d"
        hours = "h"
        minutes = "m"
        seconds = "s"
    # end class TimeUnits
    
    


 
Time Converter
--------------

.. uml::

   BaseClass <|-- TimeConverter
   TimeConverter o- TimeConverterExpressions
   
.. module:: apetools.lexicographers.timeconverter
.. autosummary::
   :toctree: api

   TimeConverter
   TimeConverter.expressions
   TimeConverter.converter
   TimeConverter.__call__
   



Time Converter Expressions
--------------------------

.. uml::

   BaseClass <|-- TimeConverterExpressions

.. autosummary::
   :toctree: api

   TimeConverterExpressions
   TimeConverterExpressions.float
   TimeConverterExpressions.integer
   TimeConverterExpressions.units
   TimeConverterExpressions.unitless
   TimeConverterExpressions.seconds
   TimeConverterExpressions.minutes
   TimeConverterExpressions.hours
   TimeConverterExpressions.days
   TimeConverterExpressions.times
   TimeConverterExpressions.enums
   TimeConverterExpressions.tokens
   TimeConverterExpressions.__iter__



Time Converter Enums
--------------------

::

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
    
    

