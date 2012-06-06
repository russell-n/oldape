"""
A parameter generator maps the lexicographer's static configuration to a set of test parameters

This way a config-file can declare a set: e.g. repetitions=10

and the parameter-generator will create 10 parameter-objects

"""

#python
from collections import namedtuple

# tottest
from tottest.baseclass import BaseClass
from tottest.parameters import iperf_server_parameters
from tottest.parameters import iperf_client_parameters

parameters = ("repetition repetitions output_folder " +
              " receiver sender sleep").split()

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

    def sender_parameters(self, parameters):
        """
        :param:

         - `parameters`: an IperfStaticParameters object

        :return: IperfTcpClientParameters
        """
        sender_parameters = iperf_client_parameters.IperfTcpClientParameters()
        return self.get_values(parameters, sender_parameters)
        
        
    def forward(self):
        """
        The yielder of parameters for the iterator

        :yield: The next parameter
        """
        #for params in self.parameters:
        for rep in range(1, self.parameters.repetitions + 1):
            receiver_parameters = self.receiver_parameters(self.parameters.iperf)
            sender_parameters = self.sender_parameters(self.parameters.iperf)
            
            yield TestParameter(repetition=rep,
                                repetitions=self.parameters.repetitions,
                                output_folder=self.parameters.output_folder,
                                receiver=receiver_parameters,
                                sender=sender_parameters,
                                sleep=5)
        return

    def __iter__(self):
        """
        :return: The forward generator method
        """
        return self.forward()
# end class ParameterGenerator
