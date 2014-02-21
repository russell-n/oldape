"""
A module to hold a keeper of Strategies
"""

#python Libraries

# testrunner Libraries
from setuprun import SetUp
#from teardown import TearDown
from crashhandler import CrashHandler
from apetools.lexicographers.configfetcher import ConfigFetcher
#from apetools.informants.helper import Helper
from apetools.baseclass import BaseClass
from apetools.tools import testdumpsyswifi

# commons
from apetools.commons import errors

# tools
#from apetools.tools import testsl4a


class Strategerizer(BaseClass):
    """
    A Strategerizer holds strategies.
    """
    def __init__(self, *args, **kwargs):
        super(Strategerizer, self).__init__(*args, **kwargs)
        return
    
    def run(self, args):
        """
        The strategy to run tests
        """
        try:
            self.logger.debug("Building the SetUp")
            run = SetUp(args)
            self.logger.debug("Running the test setup")
            run()
        except Exception as error:
            self.logger.error("Running the crash handler")
            crash_handler = CrashHandler(args)
            crash_handler.run(error)
            return
        return

    def fetch(self, args):
        """
        Fetches or lists Available config files.
        """
        self.logger.info("Running the fetcher.")
        fetcher = ConfigFetcher()
        fetcher.fetch_config()
        return

    def handle_help(self, args):
        """
        Runs the helper
        """
        self.logger.debug("Running the helper")
        helper = Helper()
        helper.display(args.topic)
        return

    def test(self, args):
        """
        Tests the setup
        """
        try:
            self.logger.info("Testing the Setup")
            setup = SetUp(args)
            for parameters in setup.lexicographer.parameters:
                # test the adb info
                test = testdumpsyswifi.TestDumpsysWifi(parameters)
                test()

                #test the network
                target = parameters.target
                self.logger.info("Pinging " + target)
                if not setup.builder.pinger.run(target=target):
                    print "Unable to ping target: " + target
        except errors.ConfigurationError as error:
            print error
        except Exception as error:
            crash_handler = CrashHandler(args)
            crash_handler.run(error)
        return
# end class Strategerizer
