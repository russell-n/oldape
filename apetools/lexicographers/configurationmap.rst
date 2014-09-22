Configuration Map
=================

An extension of the ConfigParser to do conversions



Helper Classes
--------------

.. module:: apetools.lexicographers.configuratiomap
.. autosummary::
   :toctree: api

   ConfigurationSectionError
   ConfigurationOptionError
   BooleanValues

.. uml::

   ConfigurationError <|-- ConfigurationSectionError
   ConfigurationError <|-- ConfigurationOptionError

::

    class BooleanValues(object):
        """
        A class to hold the valid booleans.
        """
        __slots__ = ()
        true = "y yes 1 true t on".split()
        false = "n no 0 false f off".split()
        map = dict([(t, True) for t in true] + [(f, False) for f in false])
    # end class Booleans
    
    



ConfigurationMap
----------------

.. uml::

   BaseClass <|-- ConfigurationMap

.. autosummary::
   :toctree: api

   ConfigurationMap
   ConfigurationMap.time_converter
   ConfigurationMap.sections
   ConfigurationMap.options
   ConfigurationMap.parser
   ConfigurationMap.raise_error
   ConfigurationMap.get
   ConfigurationMap._get
   ConfigurationMap.get_boolean
   ConfigurationMap.get_booleans
   ConfigurationMap.get_int
   ConfigurationMap.get_ints
   ConfigurationMap.get_float
   ConfigurationMap.get_floats
   ConfigurationMap.get_string
   ConfigurationMap.get_strings
   ConfigurationMap.get_list
   ConfigurationMap.get_lists
   ConfigurationMap.get_dictionary
   ConfigurationMap.get_dictionaries
   ConfigurationMap.get_namedtuple
   ConfigurationMap.get_range
   ConfigurationMap.get_ranges
   ConfigurationMap.get_times
   ConfigurationMap.get_time
   ConfigurationMap.time_in_seconds

   
