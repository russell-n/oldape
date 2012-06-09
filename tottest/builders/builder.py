"""
a module to hold a builder of objects
"""

# python
#import threading
#import os

# third party
from mock import Mock

# tottest
from tottest.baseclass import BaseClass

# infrastructure
from tottest.infrastructure import hortator
from tottest.infrastructure.testoperator import TestOperator
from tottest.infrastructure import countdowntimer

#config
from tottest.config.parametergenerator import ParameterGenerator

#commons
from tottest.commons import storageoutput
from tottest.commons import enumerations
operating_systems = enumerations.OperatingSystem

# builders
from devicebuilder import AdbDeviceBuilder
from connectionbuilder import AdbShellConnectionBuilder, SshConnectionBuilder
from teardownbuilder import TearDownBuilder
from testbuilder import IperfTestToDutBuilder


class Builder(BaseClass):
    """
    A builder builds objects
    """
    def __init__(self, parameters, *args, **kwargs):
        """
        :param:

         - `parameters`: A generator of OperatorParameters
        """
        super(Builder, self).__init__(*args, **kwargs)
        self.parameters = parameters
        self._operators = None
        self._hortator = None
        self.dut_device = None
        self.dut_connection = None
        self.tpc_connection = None
        self.storage = None
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



    def get_teardown(self, configfilename, storage):
        """
        :param:

         - `configfilename`: The name of the config-file to copy.
        :return: A Teardown for the TestOperator's cleanup
        """
        return TearDownBuilder(configfilename, storage).teardown
    
    def get_dut_device(self, parameters=None):
        """
        :param:

         - `parameters`: Nothing for the current ADB connection, meant to be used when generalized
        
        :warning: This returns the same connection repeatedly - don't use in threads.

        :return: device
        """
        if self.device is None:
            self.device = AdbDeviceBuilder().device
        return self.device

    def get_dut_connection(self, parameters=None):
        """
        :return: connection to the dut
        """
        if self.dut_connection is None:
            self.dut_connection = AdbShellConnectionBuilder().connection
        return self.dut_connection

    def get_tpc_connection(self, parameters):
        """
        This only creates a connection the first time.
        If used in threads it needs a lock.
        
        :param:

         - `parameters`: TpcConnection parameters
        
        :return: Connection to the traffic pc
        """
        if self.tpc_connection is None:
            self.tpc_builder = SshConnectionBuilder(parameters)
            self.tpc_connection = self.tpc_builder.connection
        return self.tpc_connection
        
    @property
    def operators(self):
        """
        :yield: test operators
        """
        for static_parameters in self.parameters:
            self.logger.debug("Building the TestParameters with StaticParameters - {0}".format(static_parameters))

            test_parameters = ParameterGenerator(static_parameters)
            setup = Mock()
            teardown = Mock()
            test = self.get_test(static_parameters)
            device = self.get_dut_connection(static_parameters.dut_parameters)
            watchers = Mock()
            cleanup = self.get_teardown(static_parameters.config_file_name,
                                        self.get_storage(static_parameters.output_folder))
            countdown_timer = countdowntimer.CountdownTimer(static_parameters.repetitions)
            
            yield TestOperator(test_parameters=test_parameters,
                               setup=setup,
                               teardown=teardown,
                               test=test,
                               device=device,
                               watchers=watchers,
                               cleanup=cleanup,
                               countdown_timer=countdown_timer)
        return
    
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


    def get_test(self, parameters):
        """
        :param:

         - `parameters` : named tuple with output_file and data_file names.
         
        :return: TimeToRecoveryTest object
        """
        storage = self.get_storage(parameters.output_folder)
        tpc = self.get_tpc_connection(parameters.tpc_parameters)
        dut = self.get_dut_connection(parameters.dut_parameters)
        direction = parameters.direction
        
        return IperfTestToDutBuilder(direction=direction,
                                     tpc_connection=tpc,
                                     dut_connection=dut,
                                     storage=storage).test

    def reset(self):
        """
        To be called when an operator has been built to reset the object.
        """
        self.dut_device = None
        self.dut_connection = None
        self.tpc_connection = None
        self.storage = None
        return
# end Builder
    
