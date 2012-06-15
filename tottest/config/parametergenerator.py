"""
A parameter generator maps the lexicographer's static configuration to a set of test parameters

This way a config-file can declare a set: e.g. repetitions=10

and the parameter-generator will create 10 parameter-objects

"""

#python
from collections import namedtuple

# tottest
from tottest.baseclass import BaseClass
from tottest.commons import enumerations, errors
from tottest.parameters import iperf_server_parameters
from tottest.parameters import iperf_client_parameters
from tottest.parameters import iperf_test_parameters

IperfDirection = enumerations.IperfDirection
ConfigurationError = errors.ConfigurationError

parameters = ("test_id repetition repetitions output_folder " +
              " receiver sender recovery_time affector").split()

class TestParameter(namedtuple('TestParameter', parameters)):
    """
    A TestParameter holds the settings for a single test-iteration
    """
    __slots__ = ()

    def __str__(self):
        return (self.__class__.__name__ + ":" +
                ','.join(("{f}:{v}".format(f=f, v=getattr(self,f))
                          for f in self._fields)))

    
# end class TestParameter

class ParameterGenerator(BaseClass):
    """
    A ParameterGenerator is an iterator that generates test-parameters.
    """
    def __init__(self, parameters, *args, **kwargs):
        """
        :param:

         - `parameters`: A generator of parameters from a config file.
        """
        super(ParameterGenerator, self).__init__(*args, **kwargs)
        self.parameters = parameters
        self._receiver_hostname = None
        return

    @property
    def receiver_hostname(self):
        """
        :return: Dict of direction:hostname pairs
        """
        if self._receiver_hostname is None:
            self._receiver_hostname = {}
            self._receiver_hostname[IperfDirection.to_dut] = self.parameters.dut_parameters.test_ip
            self._receiver_hostname[IperfDirection.from_dut] = self.parameters.tpc_parameters.test_ip
        return self._receiver_hostname

    def get_values(self, source, target):
        """
        :param:

         - `source`: A named tuple
         - `target`: Object to take tuples values

        :return: The target with updated values
        """
        for field in source._fields:
            setattr(target, field, getattr(source, field))
        return target
                    
    def receiver_parameters(self, parameters):
        """
        :param:

         - `parameters`: IperfStaticParameters object
        :return: IperfServerParameters
        """
        receiver_parameters = iperf_server_parameters.IperfServerParameters()
        receiver_parameters.window = parameters.window
        return receiver_parameters

    def sender_parameters(self, parameters, target):
        """
        :param:

         - `parameters`: an IperfStaticParameters object
         - `target`: The hostname or IP of the target
        :return: IperfTcpClientParameters
        """
        sender_parameters = iperf_client_parameters.IperfTcpClientParameters()
        sender =  self.get_values(parameters, sender_parameters)
        sender.client = target
        return sender

    def iperf_parameters(self, switch, direction, repetition):
        """
        :param:

         - `switch`: The number of the current switch
         - `direction`: The current direction of iperf traffic
         - `repetition`: The current repetition
        :rtype: tuple
        :return: receiver test parameters, server test parameters
        """
        try:
            sender = self.receiver_hostname[direction]
        except KeyError as error:
            self.logger.error(error)
            raise ConfigurationError("Unknown Direction: {0}".format(direction))

        receiver_parameters = self.receiver_parameters(self.parameters.iperf_server_parameters)
        sender_parameters = self.sender_parameters(self.parameters.iperf_client_parameters, sender)

        try:
            receiver_filename = "switch_{s}_repetition_{r}_{p}".format(s=switch, r=repetition, p=receiver_parameters.udp)
            sender_filename = "switch_{s}_repetition_{r}_{p}".format(s=switch, r=repetition, p=sender_parameters.udp)
        except AttributeError:
            receiver_filename = "switch_{s}_repetition_{r}_{p}".format(s=switch, r=repetition, p="tcp")
            sender_filename = "switch_{s}_repetition_{r}_{p}".format(s=switch, r=repetition, p="tcp")
        receiver_test_parameters = iperf_test_parameters.IperfTestParameters(filename=receiver_filename,
                                                                             iperf_parameters=receiver_parameters)
        sender_test_parameters = iperf_test_parameters.IperfTestParameters(filename=sender_filename,
                                                                           iperf_parameters=sender_parameters)
        return receiver_test_parameters, sender_test_parameters
                                                          
        
    def forward(self):
        """
        The yielder of parameters for the iterator

        :yield: The next parameter
        """
        #for params in self.parameters:
        for rep in range(1, self.parameters.repetitions + 1):
            for switch in self.parameters.affector_parameters.values:
                for direction in self.parameters.directions:
                    receiver_parameters, sender_parameters = self.iperf_parameters(switch, direction, rep)
                    yield TestParameter(test_id=direction,
                                        repetition=rep,
                                        repetitions=self.parameters.repetitions,
                                        output_folder=self.parameters.output_folder,
                                        receiver=receiver_parameters,
                                        sender=sender_parameters,
                                        affector=switch,
                                        recovery_time=self.parameters.recovery_time)
        return

    def __iter__(self):
        """
        :return: The forward generator method
        """
        return self.forward()
# end class ParameterGenerator
