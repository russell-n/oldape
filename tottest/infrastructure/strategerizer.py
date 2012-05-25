"""
A module to hold a keeper of Strategies
"""

#python Libraries

# testrunner Libraries
from setup import SetUp
from teardown import TearDown
from crashhandler import CrashHandler
from timetorecovertest.config.configfetcher import ConfigFetcher
from timetorecovertest.info.helper import Helper
from timetorecovertest.baseclass import BaseClass

# commons
from timetorecovertest.commons import errors

# tools
from timetorecovertest.tools import testsl4a


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
            setup = SetUp(args)
            self.logger.debug("Running the test setup")
            setup.run()
        except Exception as error:
            self.logger.error("Running the crash handler")
            crash_handler = CrashHandler(args)
            crash_handler.run(error)
            return
        #self.logger.info("Running the Tear-Down")
        #teardown = TearDown(setup)
        #teardown.run()
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
            self.logger.debug("Running the Setup")
            setup = SetUp(args)
            self.logger.debug("Running the SL4a Tester")
            for parameters in setup.lexicographer.parameters:
                # test sl4a
                test = testsl4a.TestSl4a(parameters)
                test.run()

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
