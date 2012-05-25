"""
A parameter generator maps the lexicographer's static configuration to a set of test parameters

This way a config-file can declare a set: e.g. repetitions=10

and the parameter-generator will create 10 parameter-objects

"""

#python
from collections import namedtuple

# timetorecovertest
from timetorecovertest.baseclass import BaseClass


parameters = ("repetition repetitions output_folder recovery_time timeout" +
              " threshold criteria target wifi_interface").split()

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

    def forward(self):
        """
        The yielder of parameters for the iterator

        :yield: The next parameter
        """
        #for params in self.parameters:
        for rep in range(1, self.parameters.repetitions + 1):
            yield TestParameter(repetition=rep,
                                repetitions=self.parameters.repetitions,
                                output_folder=self.parameters.output_folder,
                                recovery_time=self.parameters.recovery_time,
                                criteria=self.parameters.criteria,
                                timeout=self.parameters.timeout,
                                threshold=self.parameters.threshold,
                                target=self.parameters.target,
                                wifi_interface=self.parameters.wifi_interface)
        return

    def __iter__(self):
        """
        :return: The forward generator method
        """
        return self.forward()
# end class ParameterGenerator
