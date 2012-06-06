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
from tottest.infrastructure import teardown
from tottest.infrastructure import hortator
from tottest.infrastructure.testoperator import TestOperator

#config
from tottest.config.parametergenerator import ParameterGenerator

# testoperator tools
from tottest.tools import iperftest, killall
from tottest.tools import copyfiles

#commons
from tottest.commons import storageoutput
from tottest.commons import enumerations
operating_systems = enumerations.OperatingSystem
#connections
from tottest.connections import adbconnection
from tottest.connections import sshconnection

#watchers

# commands
from tottest.commands import iperfcommand

from tottest.log_setter import LOGNAME

# builders
from device_builder import DeviceBuilder
from dutconnectionbuilder import DutConnection
from tpcbuilder import TpcConnection

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
        self._dut_device = None
        self.tpc = None
        self._sender = None
        self._receiver = None
        self._killers = None
        self._dut_connection = None
        self.storage = None
        return

    @property
    def hortator(self):
        """
        :return: The Hortator for the test operators
        """
        if self._hortator is None:
            self.logger.debug("Builing the Hortator")
            self._hortator = hortator.Hortator(operators=self.operators)
        return self._hortator


    @property
    def dut_device(self):
        """
        :warning: This returns the same connection repeatedly - don't use in threads.

        :todo:

         - Currently only SL4ADevice - need flexibility
         
        :return: device
        """
        if self._device is None:
            self._device = DeviceBuilder().device
        return self._device

    @property
    def dut_connection(self):
        """
        :return: ADBShell connection to the dut
        """
        if self._dut_connection is None:
            self._dut_connection = DutConnection().connection
        return self._dut_connection
    
    def get_tpc(self, login=None, address=None, password=None):
        """
        This only creates a connection the first time.
        If used in threads it needs a lock.
        
        :param:

         - `login`: The user login name
         - `address`: ip address or resolvable name
         - `password`: An optional login password
        
        :return: SSHConnection to the traffic pc
        """
        if self.tpc is None:
            self.tpc = TpcConnection(hostname=address,
                                     username=login,
                                     password=password)
        return self.tpc
    

    @property
    def killers(self):
        """
        :return: tuple of iperf killers        
        """
        if self._killers is None:
            tpc_killer = killall.KillAll(connection=self.get_tpc(), name="iperf")
            dut_killer = killall.KillAll(connection=self.dut_connection,
                                         name="iperf",
                                         operating_system=operating_systems.android)
            self._killers = (tpc_killer, dut_killer)
        return self._killers
    
    @property
    def operators(self):
        """
        :yield: test operators
        """
        for static_parameters in self.parameters:
            self.logger.debug("Building the TestParameters with StaticParameters - {0}".format(static_parameters))
            config_copier = copyfiles.CopyFiles((static_parameters.source_file,), self.get_storage(static_parameters.output_folder))
            log_copier = copyfiles.CopyFiles((LOGNAME,), self.get_storage(static_parameters.output_folder))
            cleanup = teardown.TearDown((config_copier, log_copier))
            test =self.test(static_parameters)
            test_parameters = ParameterGenerator(static_parameters)

            setup = Mock()
            #teardown = Mock()
            watchers = Mock()
            countdown_timer = Mock()
            
            yield TestOperator(test_parameters=test_parameters, setup=setup, teardown=teardown, test=test,
                               device=self.dut_device, watchers=watchers, cleanup=cleanup, countdown_timer=countdown_timer)
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

    def test(self, parameters):
        """
        :param:

         - `parameters` : named tuple with output_file and data_file names.
         
        :return: TimeToRecoveryTest object
        """
        storage = self.get_storage(parameters.output_folder)
        sender = iperfcommand.IperfCommand(connection=self.get_tpc(address=parameters.tpc_control_ip, login=parameters.tpc_login, password=parameters.tpc_password),
                                           output=storage,
                                           role="tpc_to_dut")
        receiver = iperfcommand.IperfCommand(connection=self.device,
                                             output=storage,
                                             role="dut_from_tpc")
        return iperftest.IperfTest(sender=sender, receiver=receiver,killers=self.killers)
        
# end Builder
    
