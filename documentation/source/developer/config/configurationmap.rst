The Configuration Map
=====================

The `ConfigurationMap` is an *Adapter* for the `SafeConfigParser` to add helper methods and unify the Exceptions.

The purpose of the defaults is to allow some configuration options to be optional.  

.. uml::

   ConfigurationMap: filename
   ConfigurationMap: SafeConfigParser parser
   ConfigurationMap: raise_error(error)
   ConfigurationMap: String get(section, option, default)
   ConfigurationMap: Boolean get_boolean(section, option, default)
   ConfigurationMap: Integer get_int(section, option, default)
   ConfigurationMap: Float get_float(section, option, default)
   ConfigurationMap: String get_string(section, option, default)
   ConfigurationMap: List get_list(section, option, delimiter)
   ConfigurationMap: Boolean has_option(section, option)
   ConfigurationMap: List get_times(section, option)
   ConfigurationMap: Float get_time(section, option)
   ConfigurationMap: Float time_in_seconds(time_with_units)

