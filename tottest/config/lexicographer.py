"""
A module to hold a translator of configurations to parameters
"""
#python
from collections import namedtuple

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons.generators import shallow_find
from configurationmap import ConfigurationMap
from config_options import ConfigOptions
from tottest.commons import errors

parameters = ('source_file output_folder data_file repetitions recovery_time timeout' +
              ' threshold criteria target wifi_interface' +
              ' logcat_logs logwatcher_logs').split()


class StaticParameters(namedtuple("StatictParameters", parameters)):
    """
    A set of parameters for a single test.
    """
    __slots__ = ()

    def __str__(self):
        return ','.join(("{f}:{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))


class Lexicographer(BaseClass):
    """
    A Lexicographer compiles parameters.
    """
    def __init__(self, glob, *args, **kwargs):
        """
        :param:

         - `glob`: a file glob to match the config file.
        """
        super(Lexicographer, self).__init__(*args, **kwargs)
        self.glob = glob
        self._parameters = None
        self._filenames = None
        return

    @property
    def filenames(self):
        """
        Generates filenames that match self.glob.
        This is made a parameter so other classes can retrieve the list.
        
        :yield: next name
        """
        for file_name in shallow_find(self.glob):
            yield file_name
        return
        
    @property
    def parameters(self):
        """
        A Generator of parameters

        :yield: StaticParameters
        """
        found = False
        for file_name in self.filenames:
            found = True
            parser = ConfigurationMap(file_name)
            values = {}
            
            interface = parser.get(ConfigOptions.dut_section,
                                   ConfigOptions.wifi_interface_option)

            logcat_logs = parser.get_list(ConfigOptions.logcatwatcher_section,
                                          ConfigOptions.logs_option,
                                          optional=True)

            logwatcher_logs = parser.get_list(ConfigOptions.logwatcher_section,
                                              ConfigOptions.logs_option,
                                              optional=True)

            values = self.test_section(parser, values)

            yield StaticParameters(source_file=file_name,
                                   output_folder=values[ConfigOptions.output_folder_option],
                                   data_file=values[ConfigOptions.data_file_option],
                                   repetitions=values[ConfigOptions.repetitions_option],
                                   recovery_time=values[ConfigOptions.recovery_time_option],
                                   timeout=values[ConfigOptions.timeout_option],
                                   criteria=values[ConfigOptions.criteria_option],
                                   threshold=values[ConfigOptions.threshold_option],
                                   target=values[ConfigOptions.target_option],
                                   wifi_interface=interface,
                                   logcat_logs=logcat_logs,
                                   logwatcher_logs=logwatcher_logs)
        if not found:
            raise errors.ConfigurationError("Unable to find 'self.glob' in this directory.")
        return

    def test_section(self, parser, values):
        """
        :param:

         - `parser`: A ConfigurationMap that's been opened
         - `values`: A dictionary to store the parameters.

        :return: The values dictionary with the test-section options added.
        """
        section = ConfigOptions.test_section
        self.logger.debug("Getting the {0} section".format(section))
        values[ConfigOptions.output_folder_option] = parser.get(section,
                                                                ConfigOptions.output_folder_option)
        values[ConfigOptions.data_file_option] = parser.get(section,
                                                            ConfigOptions.data_file_option)
        values[ConfigOptions.repetitions_option] = parser.get_int(section,
                                                                  ConfigOptions.repetitions_option)
        values[ConfigOptions.recovery_time_option] = int(parser.get_time(section,
                                                                         ConfigOptions.recovery_time_option))
        values[ConfigOptions.timeout_option] = parser.get_time(section,
                                                               ConfigOptions.timeout_option)
        values[ConfigOptions.threshold_option] = parser.get_int(section,
                                                                ConfigOptions.threshold_option)
        values[ConfigOptions.target_option] = parser.get(section,
                                                         ConfigOptions.target_option)
        values[ConfigOptions.criteria_option] = parser.get_time(section,
                                                                ConfigOptions.criteria_option)
        return values
# end class Lexicographer
