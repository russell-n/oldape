import argparse

class Arguments(object):
    """
    An adapter for the argparse.ArgumentParser
    """
    def __init__(self):
        self._parser = None
        return

    @property
    def parser(self):
        """
        :return: ArgumentParser 
        """
        if self._parser is None:
            self._parser = argparse.ArgumentParser()
        return self._parser

    def parse_args(self):
        """
        :return: namespace with command-line arguments
        """
        self.parser.add_argument("-g", "--glob",
                                 help="A file-glob to match input file names.",
                                 default=None)

        self.parser.add_argument("-u", "--units",
                                 help="Output units per second [bits,Bytes,KBits,KBytes,Mbits,MBytes,Gbits,GBytes] (default=%(default)s)",
                                 default="Mbits")
        
        self.parser.add_argument('-s', '--save',
                                 help="If  glob is provided, save to a file instead of sending to stdout.",
                                 default=False,
                                 action="store_true")

        self.parser.add_argument("-v", "--voodoo",
                                 help="Assume that Iperf doesn't know how to add so add threads yourself.",
                                 action="store_true", default=False)
        
        self.parser.add_argument('--pudb',
                                 help="Enable pudb (if installed).",
                                 default=False,                        
                                 action="store_true")
        self.parser.add_argument('--pdb',
                                 help="Enable pdb",
                                 default=False, action="store_true")
        self.parser.add_argument("-t", '--tee',
                                 help="Send lines standard error as they come in.",
                                 default=False,
                                 action="store_true")

        self.parser.add_argument("-m", "--maximum",
                                 help="Maximum allowed bandwidth (default=%(default)s",
                                 default=1000000, type=int)
        return self.parser.parse_args()
# end class Arguments
