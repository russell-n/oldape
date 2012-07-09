"""
A module to handle parsing the command-line arguments for the test runner.

"""

# Python Libraries
import argparse

# testrunner Libraries
from tottest.baseclass import BaseClass
from strategerizer import Strategerizer

ARGUMENTS = ('fetch', 'run', 'help', 'test')

class ArgumentParser(BaseClass):
    """
    A class to parse command line arguments.
    """
    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self._parser = None
        self._subparsers = None
        self._args = None
        self._strategerizer = None
        return

    @property
    def parser(self):
        """
        :rtype: argparse.ArgumentParser
        :return: A parser for the command-line arguments.
        """
        if self._parser is None:
            self._parser = argparse.ArgumentParser()
        return self._parser

    @property
    def subparsers(self):
        """
        :rtype: ArgumentParser.SubparserAction
        :return: The subparsers for this parser.
        """
        if self._subparsers is None:
            self._subparsers = self.parser.add_subparsers(title='Test Subcommands Help',
                                                         description="Available Subcommands",
                                                         help="test subcommands")

        return self._subparsers

    @property
    def args(self):
        """
        :rtype: argparse.Namespace
        :return: The parsed arguments
        
        """
        if self._args is None:
            self._add_arguments()
            self._add_subparsers()
            self._args = self.parser.parse_args()
        return self._args

    @property
    def strategerizer(self):
        """
        :return: Holder of strategies
        """
        if self._strategerizer is None:
            self._strategerizer = Strategerizer()
        return self._strategerizer
    
    def _add_arguments(self):
        """
        Adds the base arguments used for the top-level command (runtest)
        """
        #the base arguments
        self.parser.add_argument("-d", "--debug",
                                 help="Display debugging messages.",
                                 action="store_true",
                                 default=False, dest="debug")
    
        self.parser.add_argument("--pdb",
                                 help="Enable interactive debugging.",
                                 action="store_true",
                                 default=False, dest='enable_debugging')

        self.parser.add_argument("-s", "--silent",
                                 help="Turn off screen output.",
                                 action="store_true", default=False,
                                 dest='silent')
        return

    def _add_subparsers(self):
        """
        Add the subparsers this is an external method so that the parser isn't too cluttered up.
        """
        runner = self.subparsers.add_parser("run", help="Run a Test")
        runner.add_argument("glob", help="A file glob to match config files (e.g. *.ini - default='%(default)s').",
                            metavar="<config-file glob>",
                            default="*.ini",
                            nargs="?")
        runner.set_defaults(function=self.strategerizer.run)

        fetcher = self.subparsers.add_parser("fetch", help="Fetch a sample config file.")
        fetcher.set_defaults(function=self.strategerizer.fetch)

        tester = self.subparsers.add_parser('test', help='Test your setup.')
        tester.add_argument("glob", help="A file glob to match config files (e.g. *.ini - default='%(default)s').",
                            metavar="<config-file glob>",
                            default="throughputovertime.ini",
                            nargs="?")

        tester.set_defaults(function=self.strategerizer.test)

        helper = self.subparsers.add_parser("help", help="Show more help")
        helper.add_argument('topic', help="A specific subject to inquire about.", nargs="?")
        helper.set_defaults(function=self.strategerizer.handle_help)
        return
    
    def print_help(self):
        """
        Calls on  ArgumentParser.print_help()
        """
        self.parser.print_help()
        return
# end class ArgumentParser
    
