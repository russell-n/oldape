"""
a module to hold a builder of objects
"""

# python
import threading
import os

# timetorecovertest
from timetorecovertest.baseclass import BaseClass

from hortator import Hortator
from testoperator import TestOperator, OperatorStaticTestParameters, OperatorParameters
from timetorecovertest.config.parametergenerator import ParameterGenerator

# testoperator tools
from timetorecovertest.tools import setupiteration
from timetorecovertest.tools import timetofailure
from timetorecovertest.tools import teardowniteration
from timetorecovertest.tools import timetorecovery
from timetorecovertest.tools import timetorecoverytest
from timetorecovertest.tools import copyfiles
from timetorecovertest.tools import movefiles

# devices
from timetorecovertest.devices import sl4adevice

#commons
from timetorecovertest.commons import storageoutput
#connections
from timetorecovertest.connections import adbconnection
#watchers
from timetorecovertest.watchers import logcatwatcher, logwatcher, thewatcher
# commands
from timetorecovertest.commands import ping

# infrastructur
from teardown import TearDown
from timetorecovertest.log_setter import LOGNAME

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
        self._watchers = None
        self._hortator = None
        self._pinger = None
        self._device = None
        self._thread_connection = None
        self._mutex = None
        self.storage = None
        self._event = None
        return

    @property
    def hortator(self):
        """
        :return: The Hortator for the test operators
        """
        if self._hortator is None:
            self.logger.debug("Builing the Hortator")
            self._hortator = Hortator(operators=self.operators)
        return self._hortator

    @property
    def pinger(self):
        """
        :warning: This returns the same connection repeatedly - threads need locks.
        
        :todo:

         - This is currently only an adb-pinger, this needs to be made flexible
         
        :return: pinger
        """
        if self._pinger is None:
            self.logger.debug("Building the pinger")
            self._pinger = ping.ADBPing()
        return self._pinger

    @property
    def device(self):
        """
        :warning: This returns the same connection repeatedly - don't use in threads.

        :todo:

         - Currently only SL4ADevice - need flexibility
         
        :return: device
        """
        if self._device is None:
            self.logger.debug("Building the SL4A Device")
            self._device = sl4adevice.SL4ADevice()
        return self._device

    @property
    def thread_connection(self):
        """
        :rtype: ADBShellConnection
        :return: A connection meant for threads (so they can setup locks).
        """
        if self._thread_connection is None:
            self._thread_connection = adbconnection.ADBShellConnection() 
        return self._thread_connection

    @property
    def mutex(self):
        """
        :return: a Semaphore set to allow 1 thread to pass.
        """
        if self._mutex is None:
            self._mutex = threading.RLock()
        return self._mutex

    @property
    def event(self):
        """
        :return: A threading event.
        """
        if self._event is None:
            self._event = threading.Event()
            self._event.clear()
        return self._event

    def log_watchers(self, output_folder, data_file, logs):
        """
        : param:

         - `output_folder`: The name of the folder to store the log in.
         - `data_file`: The name of the file to store the log in.
         - `logs`: A list of log paths
         
        :return: List of log watchers or None
        """
        if logs is None:
            return
        watchers = []
        for log in logs:
            extension = ".{0}".format(os.path.basename(log))
            watchers.append(logwatcher.SafeLogWatcher(lock=self.mutex,
                                                     event=self.event,
                                                     output=self.get_storage(output_folder).open(data_file,
                                                                                                 extension=extension),
                                                     path=log,
                                                     connection=self.thread_connection))

        return  watchers
    
    @property
    def operators(self):
        """
        :yield: test operators
        """
        for static_parameters in self.parameters:
            self.logger.debug("Building the TestParameters with StaticParameters - {0}".format(static_parameters))
            config_copier = copyfiles.CopyFiles((static_parameters.source_file,), self.get_storage(static_parameters.output_folder))
            log_copier = copyfiles.CopyFiles((LOGNAME,), self.get_storage(static_parameters.output_folder))
            cleanup=TearDown((config_copier, log_copier))
            setup = self.setup_iteration()
            teardown = teardowniteration.TeardownIteration()
            test =self.test(static_parameters)
            test_parameters = ParameterGenerator(static_parameters)

            logcat_watcher = logcatwatcher.SafeLogcatWatcher(lock=self.mutex,
                                                             logs=static_parameters.logcat_logs,
                                                             event=self.event,
                                                             output=self.get_storage(static_parameters.output_folder).open(static_parameters.data_file,
                                                                                                                     extension=".logcat"),
                                                             connection=self.thread_connection)
            watchers = self.log_watchers(static_parameters.output_folder, static_parameters.data_file, static_parameters.logwatcher_logs)
            if watchers is not None:
                watchers.append(logcat_watcher)
            else:
                watchers = [logcat_watcher]
                
            watcher = thewatcher.TheWatcher(watchers=watchers, event=self.event)
            op_parameters = OperatorParameters(setup, teardown, test, self.device,
                                               watcher, cleanup)
            ost_parameters = OperatorStaticTestParameters(op_parameters,
                                                          static_parameters,
                                                          test_parameters)
            yield TestOperator(ost_parameters)
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
        ttrt = timetorecoverytest
        storage = self.get_storage(parameters.output_folder).open(parameters.data_file, extension="_data.csv")
        ttr = timetorecovery.TimeToRecovery(self.pinger)
        ttrtp = ttrt.TimeToRecoveryTestParameters(output=storage,
                                                  device=self.device,
                                                  time_to_recovery=ttr)
        return ttrt.TimeToRecoveryTest(ttrtp)
        
    def setup_iteration(self):
        """
        :return: A SetupIteration object
        """
        ttf = timetofailure.TimeToFailure(self.pinger)
        return setupiteration.SetupIteration(self.device, ttf)

# end Builder
    
