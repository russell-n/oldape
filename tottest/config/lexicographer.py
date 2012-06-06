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

parameters = ('source_file output_folder data_file  repetitions dut_test_ip '
              'tpc_control_ip tpc_test_ip tpc_login tpc_password iperf').split()

iperf_parameters = 'window len parallel interval format time'.split()
class IperfStaticParameters(namedtuple("IperfStaticParameters", iperf_parameters)):
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}_{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))


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
            found = True
            parser = self.get_parser(file_name)

            # start with the test section
            output_folder_name, data_file_name, repetitions = self.test_section(parser)

            # now the dut
            dut_test_ip = self.dut_section(parser)
                                        

            # now the tpc
            tpc_control_ip, tpc_test_ip, tpc_login, tpc_password = self.tpc_section(parser)

            # now the iperf section
            iperf = self.iperf_section(parser)
            yield StaticParameters(source_file=file_name,
                                   output_folder=output_folder_name,
                                   data_file=data_file_name,
                                   repetitions=repetitions,
                                   dut_test_ip=dut_test_ip,
                                   tpc_login=tpc_login,
                                   tpc_control_ip=tpc_control_ip,
                                   tpc_test_ip=tpc_test_ip,
                                   tpc_password=tpc_password,
                                   iperf=iperf)
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

        :rtype: IperfStaticParameters
        :return: iperf parameters
        """
        section = ConfigOptions.iperf_section
        window = parser.get(section,
                            ConfigOptions.window_option)
        length = parser.get(section,
                            ConfigOptions.length_option)
        parallel = parser.get(section,
                              ConfigOptions.parallel_option)
        interval = parser.get(section,
                              ConfigOptions.interval_option)
        _format = parser.get(section,
                             ConfigOptions.format_option)[0]
        time = parser.get_time(section,
                               ConfigOptions.time_option)                              
        return IperfStaticParameters(window=window,
                                     len=length,
                                     parallel=parallel,
                                     interval=interval,
                                     format=_format,
                                     time=str(time))
    
    def dut_section(self, parser):
        """
        :param:

         - `parser`: An open Configuration Map

        :return: dut_test_ip
        """
        section = ConfigOptions.dut_section
        test = parser.get(section,
                          ConfigOptions.test_ip_option)
        return test

    def tpc_section(self, parser):
        """
        :param:

         - `parser`: A Configuration map

        :return: tpc_control_ip, tpc_test_ip, tpc_login, password
        """
        section = ConfigOptions.traffic_pc_section
        control = parser.get(section,
                             ConfigOptions.control_ip_option)
        test = parser.get(section,
                             ConfigOptions.test_ip_option)
        login = parser.get(section,
                           ConfigOptions.login_option)
        password = parser.get_optional(section,
                                       ConfigOptions.password_option)
        return control, test, login, password
    
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
        data_file_name = parser.get(section,
                                    ConfigOptions.data_file_option)
        repetitions = parser.get_int(section,
                                 ConfigOptions.repetitions_option)
        return output_folder_name, data_file_name, repetitions
# end class Lexicographer

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    l = Lexicographer("tot.ini")
    
    for parameter in l.parameters:
        print parameter.iperf
