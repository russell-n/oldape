"""
a module to hold a builder of objects
"""

# python
#import threading
#import os
from threading import RLock

# third party
from mock import MagicMock

# tottest
from tottest.baseclass import BaseClass

# proletarians
from tottest.proletarians import hortator
from tottest.proletarians.testoperator import TestOperator
from tottest.proletarians import countdowntimer


#config
from tottest.lexicographers.parametergenerator import ParameterGenerator

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
        self._operators = None
        self._hortator = None
        self.tpc_connection = None
        self._storage = None
        self._lock = None
        self._nodes = None

        self._operation_setup_builder = None
        self._operation_teardown_builder = None
        self._setup_test_builder = None
        self._execute_test_builder = None
        self._teardown_test_builder = None        
        return

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
            self._nodes = NodesBuilder(self, self.current_config).nodes
        return self._nodes
    
    @property
    def lock(self):
        """
        :return: A re-entrant lock
        """
        if self._lock is None:
            self._lock = RLock()
        return self._lock

    @property
    def operators(self):
        """
        :yield: test operators
        """ 
        for config_map in self.maps:
            self.reset()
            self.current_config = config_map
            self.logger.debug("Building the TestParameters with configmap - {0}".format(config_map))
            operation_setup = self.operation_setup_builder(config_map).product
            operation_setup_parameters = self.operation_setup_builder(config_map).parameters
            
            operation_teardown = self.operation_teardown_builder(config_map, operation_setup_parameters).product
            operation_teardown_parameters = self.operation_teardown_builder(config_map, operation_setup_parameters).parameters
            
            test_setup = self.setup_test_builder(config_map, operation_teardown_parameters).product
            test_setup_parameters = self.setup_test_builder(config_map, operation_teardown_parameters).parameters
            
            test = self.execute_test_builder(config_map, test_setup_parameters).product
            test_parameters = self.execute_test_builder(config_map, test_setup_parameters).parameters
            
            test_teardown = self.teardown_test_builder(config_map, test_parameters).product
            test_teardown_parameters = self.teardown_test_builder(config_map, test_parameters).parameters
            
            yield TestOperator(ParameterGenerator(test_setup_parameters),
                               operation_setup=operation_setup,
                               operation_teardown=operation_teardown,
                               test_setup=test_setup,
                               tests=test,
                               test_teardown=test_teardown,
                               countdown_timer=MagicMock())
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
    
    def get_tpc_connection(self, parameters):
        """
        This only creates a connection the first time.
        
        :param:

         - `parameters`: TpcConnection parameters
        
        :return: Connection to the traffic pc
        """
        if self.tpc_connection is None:
            self.tpc_builder = connection_builders[parameters.connection_type](parameters)
            self.tpc_connection = self.tpc_builder.connection
            if parameters.paths is not None:
                self.tpc_connection.add_paths(parameters.paths)
        return self.tpc_connection
            
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
    
