"""
A module to build a setup for iterations.
"""

from tottest.tools import setupiteration

class SetupIterationBuilder(object):
    """
    A SetupIterationBuilder builds Setup Iteration runners
    """
    def __init__(self, device, affector, time_to_recovery):
        """
        :param:

         - `device`: A connection to the DUT
         - `affector`: An environmental affector
         - `time_to_recovery`: A time to recovery tester
        """
        self.device = device
        self.affector = affector
        self.time_to_recovery = time_to_recovery
        self._setup = None
        return

    @property
    def setup(self):
        """
        :return: A setup iteration runner
        """
        if self._setup is None:
            self._setup = setupiteration.SetupIteration(device=self.device,
                                                        time_to_recovery=self.time_to_recovery,
                                                        affector=self.affector)
        return self._setup
    
# end class SetupIterationBuilder
