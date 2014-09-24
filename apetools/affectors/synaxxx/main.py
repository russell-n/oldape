
# python standard library
import argparse

# this package
from handlers import run


def parse_args():
    """
    parses the command-line arguments

    :return: ArgumentParser namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--pudb", help="Enable pudb debugger.",
                        default=False, action="store_true")
    parser.add_argument("--pdb", help="Enable pdb debugger.",
                        default=False, action="store_true")
    parser.add_argument("hostname", help="Hostname (IP address) for the Synaccess power switch.")
    parser.add_argument('--status', help="Show the states (instead of setting them).",
                        default=False, action='store_true')
    parser.add_argument("-s", "--switches", nargs="*", help="Space-separated list of switches (or None to turn all off).",
                        default=None)
    return parser.parse_args()


def enable_debugging(args):
    """
    enables pudb or pdb if set in the args

    :param:

     - `args`: something with pudb and pdb attributes
    """
    if args.pudb:
        import pudb
        pudb.set_trace()
        return
    if args.pdb:
        import pdb
        pdb.set_trace()
    return


def main():
    """
    Parses the arguments, enables debugging, calls 'run'
    """
    args = parse_args()
    enable_debugging(args)
    run(args)
    return

if __name__ == "__main__":
    main()
