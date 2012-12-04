"""
a module to hold a builder of objects
"""

# python
#import threading
#import os


# third party
from mock import MagicMock

# tottest
from tottest.baseclass import BaseClass

# proletarians
from tottest.proletarians import hortator
from tottest.proletarians.testoperator import TestOperator
#from tottest.proletarians import countdowntimer

from subbuilders.basetoolbuilder import Parameters
#config
from tottest.lexicographers.parametergenerator import ParameterGenerator
from tottest.lexicographers.config_options import ConfigOptions


#commons
from tottest.commons import storageoutput
from tottest.commons import enumerations
operating_systems = enumerations.OperatingSystem
iperf_direction = enumerations.IperfDirection
ConnectionTypes = enumerations.ConnectionTypes
from tottest.commons import dummy
NoOpDummy = dummy.NoOpDummy


# builders
from subbuilders.nodesbuilder import NodesBuilder
from subbuilders.operationsetupbuilder import OperationSetupBuilder
from subbuilders.operationteardownbuilder import OperationTeardownBuilder
from subbuilders.setuptestbuilder import SetupTestBuilder
from subbuilders.executetestbuilder import ExecuteTestBuilder
from subbuilders.teardowntestbuilder import TeardownTestBuilder
from subbuilders.tpcdevicebuilder import TpcDeviceBuilder

class BuilderEnum(object):
    """
    A class to hold constants for the builder
    """
    __slots__ = ()
    repetition = 'repetition'
# end class BuilderEnum

class Builder(BaseClass):
    """
    A builder builds objects
    """
    def __init__(self, maps, *args, **kwargs):
        """
        :param:

         - `maps`: A generator of ConfigurationMaps
        """
        super(Builder, self).__init__(*args, **kwargs)
        self.maps = maps
        self._repetitions = None
        self._parameters = None
        self._operators = None
        self._hortator = None
        self._tpc_device = None
        self._storage = None
        self._lock = None
        self._nodes = None
        self._thread_nodes = None

        self._operation_setup_builder = None
        self._operation_teardown_builder = None
        self._setup_test_builder = None
        self._execute_test_builder = None
        self._teardown_test_builder = None        
        return

    @property
    def parameters(self):
        """
        :return: list of parameters
        """
        if self._parameters is None:
            self._parameters = []
            self._parameters.append(self.repetitions)
        return self._parameters

    @parameters.setter
    def parameters(self, new_parameters):
        """
        :param:

         - `new_parameters`: a list of parameter named tuples

        :postcondition: self.parameters = new_parameters
        """
        self._parameters = new_parameters
        return self._parameters

    @property
    def repetitions(self):
        """
        :return: list of named tuples giving repetitions parameters
        """
        if self._repetitions is None:
                reps = self.current_config.get_int(ConfigOptions.test_section,
                                               ConfigOptions.repeat_option)
                self._repetitions = Parameters(name=BuilderEnum.repetition,
                                                  parameters=[rep for rep in range(1, reps+1)])

        return self._repetitions
    
    def operation_setup_builder(self, config_map=None, parameters=None):
        """
        :return: builder for the operation
        """
        if self._operation_setup_builder is None:
            if parameters is None:
                parameters = []
            self._operation_setup_builder = OperationSetupBuilder(self, config_map, parameters)
        return self._operation_setup_builder

    def operation_teardown_builder(self, config_map=None, parameters=None):
        """
        :return: builder for the operation teardown
        """
        if self._operation_teardown_builder is None:
            if parameters is None:
                parameters = []
            self._operation_teardown_builder = OperationTeardownBuilder(self, config_map, parameters)
        return self._operation_teardown_builder

    def setup_test_builder(self, config_map=None, parameters=None):
        """
        :return: builder for the test setup
        """
        if self._setup_test_builder is None:
            if parameters is None:
                parameters = []
            self._setup_test_builder = SetupTestBuilder(self, config_map, parameters)
        return self._setup_test_builder

    def execute_test_builder(self, config_map=None, parameters=None):
        """
        :return: builder for the test executor
        """
        if self._execute_test_builder is None:
            if parameters is None:
                parameters = []
            self._execute_test_builder = ExecuteTestBuilder(self, config_map, parameters)
        return self._execute_test_builder

    def teardown_test_builder(self, config_map=None, parameters=None):
        """
        :return: builder for the test teardown
        """
        if self._teardown_test_builder is None:
            if parameters is None:
                parameters = []
            self._teardown_test_builder = TeardownTestBuilder(self, config_map, parameters)
        return self._teardown_test_builder
    

    @property
    def nodes(self):
        """
        :return: dictionary of id:node-device pairs
        """
        if self._nodes is None:
            #import pudb; pudb.set_trace()
            self._nodes = NodesBuilder(self, self.current_config).nodes
        return self._nodes

    @property
    def thread_nodes(self):
        """
        :return: dictionary of id:node-device pairs to be used in threads
        """
        if self._thread_nodes is None:
            #import pudb; pudb.set_trace()
            self._thread_nodes = NodesBuilder(self, self.current_config).nodes
        return self._thread_nodes

    @property
    def operators(self):
        """
        :yield: test operators
        """ 
        for config_map in self.maps:
            self.reset()
            self.current_config = config_map
            self.logger.debug("Building the TestParameters with configmap - {0}".format(config_map))
            operation_setup = self.operation_setup_builder(config_map, self.parameters).product
            self.parameters = self.operation_setup_builder(config_map).parameters
            
            operation_teardown = self.operation_teardown_builder(config_map, self.parameters).product
            self.parameters = self.operation_teardown_builder(config_map,
                                                               self.parameters).parameters

            
            test_setup = self.setup_test_builder(config_map, self.parameters).product
            self.parameters = self.setup_test_builder(config_map, self.parameters).parameters

            test = self.execute_test_builder(config_map, self.parameters).product
            self.parameters = self.execute_test_builder(config_map, self.parameters).parameters
            
            test_teardown = self.teardown_test_builder(config_map, self.parameters).product
            self.parameters = self.teardown_test_builder(config_map, self.parameters).parameters
            
            yield TestOperator(ParameterGenerator(self.parameters),
                               operation_setup=operation_setup,
                               operation_teardown=operation_teardown,
                               test_setup=test_setup,
                               tests=test,
                               test_teardown=test_teardown,
                               countdown_timer=MagicMock(),
                               nodes=self.nodes)
        return

    @property
    def hortator(self):
        """
        :return: The Hortator for the test operators
        """
        if self._hortator is None:
            self.logger.debug("Building the Hortator")
            self._hortator = hortator.Hortator(operators=self.operators)
        return self._hortator

    @property
    def tpc_device(self):
        """
        This only creates a new device the first time.
        
        :return: device for the traffic pc
        """
        if self._tpc_device is None:
            self._tpc_device = TpcDeviceBuilder(self.current_config).device
        return self._tpc_device
            
    def storage(self, folder_name=None):
        """
        :param:

         - `folder_name`: The name of the output folder for data.

        :return: StorageOutput for the folder.
        """
        if self._storage is None:
            self.logger.debug("Buidling the Storage with folder: {0}".format(folder_name))
            self._storage = storageoutput.StorageOutput(folder_name)
        return self._storage

    def reset(self):
        """
        :postcondition: parameters reset to None
        """
        self._parameters = None
        self._repetitions = None
        self._operation_setup_builder = None
        self._operation_teardown_builder = None
        self._setup_test_builder = None
        self._execute_test_builder = None
        self._teardown_test_builder = None
        self._storage = None
        self._nodes = None
        self._lock = None
        return
# end Builder
    
