"""
A module to hold a translator of configurations to parameters.

Parameter classes in this module are named tuples whose __str__ is defined
with `field_value,field_value,...` formatting for debug logging.
"""
#python
from collections import namedtuple

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.commons.generators import shallow_find
from configurationmap import ConfigurationMap
from config_options import ConfigOptions
from tottest.commons import errors

static_parameters = ('config_file_name output_folder repetitions '
                     'tpc_parameters dut_parameters iperf_client_parameters '
                     'iperf_server_parameters').split()

iperf_client_parameters = 'client window len parallel interval format time'.split()
iperf_server_parameters = 'window'
dut_parameters = "test_ip"
tpc_parameters = "hostname test_ip username password".split()

class IperfClientParameters(namedtuple("IperfClientParameters", iperf_client_parameters)):
    """
    lexicographer.IperfClientParameters is a named tuple of raw parameters 
    """
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}_{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))
# end IperfClientParameters

class IperfServerParameters(namedtuple("IperfServerParameters", iperf_server_parameters)):
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}_{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))
# end IperfServerParameters
    
class StaticParameters(namedtuple("StaticParameters", static_parameters)):
    """
    A set of parameters for a single test.
    """
    __slots__ = ()

    def __str__(self):
        return ','.join(("{f}:{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))
# end StaticParameters

class DutParameters(namedtuple("DutParameters", dut_parameters)):
    """
    Parameters needed to configure dut connections
    """
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}:{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))
# end DutParameters

class TpcParameters(namedtuple("TpcParameters", tpc_parameters)):
    """
    Parameters needed to configure the TPC connections
    """
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}:{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))

# end TpcParameters
    
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
        self.logger.debug("Lexicographer using glob: {0}".format(glob))
        self.glob = glob
        self._parameters = None
        self.dut_parameters = None
        return

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
        for file_name in self.filenames():
            self.logger.debug("Translating file '{0}'".format(file_name))
            found = True
            parser = self.get_parser(file_name)

            # start with the test section
            output_folder_name, repetitions = self.test_section(parser)

            # now the dut
            dut_parameters = self.dut_section(parser)

            # now the tpc
            tpc_parameters = self.tpc_section(parser)

            # now the iperf section
            client, server = self.iperf_section(parser)
            yield StaticParameters(config_file_name=file_name,
                                   output_folder=output_folder_name,
                                   repetitions=repetitions,
                                   tpc_parameters=tpc_parameters,
                                   dut_parameters=dut_parameters,
                                   iperf_client_parameters=client,
                                   iperf_server_parameters=server)
        if not found:
            raise errors.ConfigurationError("Unable to find '{0}' in this directory.".format(self.glob))
        return

    def get_parser(self, file_name):
        """
        :param:

         - `file_name`: The name of a config file

        :return: Configuration map for the file      
        """        
        return ConfigurationMap(file_name)
    
    def iperf_section(self, parser):
        """
        :param:

         - `parser`: An open Configuration map

        :rtype: Tuple
        :return: IperfClientParameters, IperfServerParameters
        """
        section = ConfigOptions.iperf_section
        self.logger.debug("Getting the {0} section".format(section))
        window = parser.get_optional(section,
                                     ConfigOptions.window_option,
                                     default="256K")
        length = parser.get_optional(section,
                                     ConfigOptions.length_option,
                                     default="1470")
        parallel = parser.get_optional(section,
                                       ConfigOptions.parallel_option,
                                       '4')
        interval = parser.get_optional(section,
                                       ConfigOptions.interval_option,
                                       '1')
        _format = parser.get_optional(section,
                                      ConfigOptions.format_option,
                                      default='megabits')[0]
        time = parser.get_time(section,
                               ConfigOptions.time_option)
        client = self.dut_section(parser).test_ip
        iperf_client = IperfClientParameters(client=client,
                                             window=window,
                                             len=length,
                                             parallel=parallel,
                                             interval=interval,
                                             format=_format,
                                             time=str(time))
        iperf_server = IperfServerParameters(window=window)
        return iperf_client, iperf_server
    
    def dut_section(self, parser):
        """
        :param:

         - `parser`: An open Configuration Map

        :return: DutParameters populated with the dut's values
        """
        if self.dut_parameters is None:
            section = ConfigOptions.dut_section
            self.logger.debug("Getting the {0} section".format(section))
            test = parser.get(section,
                              ConfigOptions.test_ip_option)
            self.dut_parameters = DutParameters(test_ip=test)
        return self.dut_parameters

    def tpc_section(self, parser):
        """
        :param:

         - `parser`: A Configuration map

        :return: TpcParameters with values set
        """
        section = ConfigOptions.traffic_pc_section
        self.logger.debug("Getting the {0} section.".format(section))
        control = parser.get(section,
                             ConfigOptions.control_ip_option)
        test = parser.get(section,
                             ConfigOptions.test_ip_option)
        login = parser.get(section,
                           ConfigOptions.login_option)
        password = parser.get_optional(section,
                                       ConfigOptions.password_option)
        return TpcParameters(hostname=control,
                             test_ip=test,
                             username=login,
                             password=password)
    
    def test_section(self, parser):
        """
        :param:

         - `parser`: A ConfigurationMap that's been opened

        :return: output_folder_name, data_file_name, repetitions
        """
        section = ConfigOptions.test_section
        self.logger.debug("Getting the {0} section".format(section))
        output_folder_name  = parser.get(section,
                                         ConfigOptions.output_folder_option)
        #data_file_name = parser.get(section,
        #                            ConfigOptions.data_file_option)
        repetitions = parser.get_int(section,
                                 ConfigOptions.repetitions_option)
        return output_folder_name, repetitions
# end class Lexicographer

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    l = Lexicographer("tot.ini")
    
    for parameter in l.parameters:
        print parameter.iperf
