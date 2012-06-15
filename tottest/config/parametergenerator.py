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
        return

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
        
        
    def forward(self):
        """
        The yielder of parameters for the iterator

        :yield: The next parameter
        """
        #for params in self.parameters:
        for rep in range(1, self.parameters.repetitions + 1):
            for value in self.parameters.affector_parameters.values:
                for direction in self.parameters.directions:
                    if direction == IperfDirection.to_dut:
                        sender = self.parameters.dut_parameters.test_ip
                    elif direction == IperfDirection.from_dut:
                        sender = self.parameters.tpc_parameters.test_ip
                    else:
                        raise ConfigurationError("Unknown Direction: {0}".format(direction))
                    receiver_parameters = self.receiver_parameters(self.parameters.iperf_server_parameters)
                    sender_parameters = self.sender_parameters(self.parameters.iperf_client_parameters, sender)
                
                    yield TestParameter(test_id=direction,
                                        repetition=rep,
                                        repetitions=self.parameters.repetitions,
                                        output_folder=self.parameters.output_folder,
                                        receiver=receiver_parameters,
                                        sender=sender_parameters,
                                        affector=value,
                                        recovery_time=self.parameters.recovery_time)
        return

    def __iter__(self):
        """
        :return: The forward generator method
        """
        return self.forward()
# end class ParameterGenerator
