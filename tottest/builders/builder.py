"""
a module to hold a builder of objects
"""

# python
#import threading
#import os
from threading import RLock

# third party

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
        self.storage = None
        self._lock = None
        self._nodes = None
        return

    def nodes(self, config_map):
        """
        :param:

         - `config_map`: a configuration map with enough information for a node-builder

        :return: dictionary of id:node-device pairs
        """
        if self._nodes is None:
            self._nodes = NodesBuilder(config_map).nodes
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
            self.logger.debug("Building the TestParameters with configmap - {0}".format(config_map))
            operation_setup = OperationSetupBuilder(config_map).operation_setup
            operation_teardown = OperationTeardownBuilder(config_map).operation_teardown
            test_setup = SetupTestBuilder(config_map).test_setup
            test = ExecuteTestBuilder(config_map).execute_test
            test_teardown = TeardownTestBuilder(config_map).teardown_test
            yield TestOperator([],
                               operation_setup=operation_setup,
                               operation_teardown=operation_teardown,
                               test_setup=test_setup,
                               tests=test,
                               test_teardown=test_teardown,
                               countdown_timer=NoOpDummy())
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
            
    def get_storage(self, folder_name=None):
        """
        :param:

         - `folder_name`: The name of the output folder for data.

        :return: StorageOutput for the folder.
        """
        if self.storage is None:
            self.logger.debug("Builing the Storage with folder: {0}".format(folder_name))
            self.storage = storageoutput.StorageOutput(folder_name)
        return self.storage
# end Builder
    
