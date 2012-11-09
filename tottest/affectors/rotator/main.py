"""
The main entry point to convert the rotator to a command.
"""

import argparse

from log_setter import set_logger

def enable_debugger(args):
    """
    :param:

     - `args`: an argument namespace
    """
    if args.pudb:
        try:
            import pudb
            pudb.set_trace()
            return
        except ImportError:
            print "Unable to import pudb"
    if args.pdb:
        import pdb
        pdb.set_trace()
    return

def parse_args():
    """
    An argument parser for the rate-table command
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("angle", help="The angle (in degrees) to rotate the table to (default=%(default)s)",
                        default=0, nargs="?", type=int)

    parser.add_argument("-d", "--debug",
                        help="Display debugging messages.",
                        action="store_true",
                        default=False, dest="debug")

    parser.add_argument("-s", "--silent",
                        help="Turn off screen output.",
                        action="store_true", default=False,
                        dest='silent')

    parser.add_argument("--pudb", help="Enable the pudb debugger.",
			action="store_true",
                        default = False)
    parser.add_argument("--pdb", help="Enable the pdb debugger.",
			action="store_true",
                        default = False)
    return parser.parse_args()

def main():
    args = parse_args()
    enable_debugger(args)
    #set_logger(args)
    from rotator import Rotator
    r = Rotator()
    r(args.angle)
    return

if __name__ == "__main__":
    main()
        
