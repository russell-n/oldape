
# python libraries
import argparse
import traceback
import logging
import logging.handlers

#nps libraries
from naxxx import Naxxx


IPERF_TIMESTAMP = "%Y%m%d%H%M%S"
logger = logging.getLogger(__package__)
SCREEN_FORMAT = "%(levelname)s: %(name)s.%(funcName)s, Line: %(lineno)d [%(asctime)s] -- %(message)s"
SCREEN_FORMAT_QUIET = "%(levelname)s: [%(asctime)s] -- %(message)s"
LOG_FORMAT = "%(levelname)s,%(name)s,%(threadName)s,%(funcName)s,Line: %(lineno)d,%(asctime)s,%(message)s"

GIGABYTE = 1073741824
BACKUP_LOGS = 5


def set_logger(args):
    """
    Creates a logger and sets the level based on args.

    :param:

     - `args`: args with debug and silent attributes
    """
    stderr = logging.StreamHandler()
    if args.debug:
        screen_format = SCREEN_FORMAT
    else:
        screen_format = SCREEN_FORMAT_QUIET
        
    screen_format = logging.Formatter(screen_format)
    stderr.setFormatter(screen_format)

    log_file = logging.handlers.RotatingFileHandler('{0}.log'.format(__package__),
                                           maxBytes=GIGABYTE, backupCount=BACKUP_LOGS)
    file_format = logging.Formatter(LOG_FORMAT, datefmt=IPERF_TIMESTAMP)
    log_file.setFormatter(file_format)
    
    logger.setLevel(logging.DEBUG)
    log_file.setLevel(logging.DEBUG)

    if args.debug:
        stderr.setLevel(logging.DEBUG)
    elif args.silent:
        stderr.setLevel(logging.ERROR)
    else:
        stderr.setLevel(logging.INFO)

    logger.addHandler(stderr)
    logger.addHandler(log_file)
    return 


def enable_debugging(args):
    """
    Checks if pdb pudb has been set runs pudb if it was
    """
    if not args.pdb:
        return
    try:
        import pudb as pdb
    except ImportError as error:
        logger.error(error)
    pdb.set_trace()
    return


def parse_args():
    """
    parses the command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdb", help="Start an interactive debugger.",
                        action="store_true", default=False)

    parser.add_argument("-d", "--debug", help="Enable more debugging output to the screen.",
                        action="store_true", default=False)
    parser.add_argument('-s', '--silent', help="Turn off screen output.",
                        action="store_true", default=False)
    
    parser.add_argument("-a", "--address", help="The IP Address of the Networked Power Supply.",
                        metavar="ip-address",
                        dest="ip_address",
                        required=True)

    parser.add_argument("-i", "--id-list", help="comma-seprated ids of the switches to turn on.",
                        dest="id_list")
    return parser.parse_args()


def handle_crash(error):
    """
    Generates a crash report.
    """
    logger.error(error)
    with open("crashreport.naxxx", 'w') as f:
        traceback.print_exc(file=f)
    return


def run(args):
    """
    Runs the naxxx

    :param:

     - `args`: namespace with id_list attribute
    """
    try:
        ids = [int(item) for item in args.id_list.split(',')]
    except AttributeError:
        ids = []
        print "Killing all switches"
        return
    except ValueError:
        print "ids need to be comma-separated integers, got {0}".format(args.id_list)
        return
    naxxx = Naxxx(IP=args.ip_address)
    naxxx.run(ids)
    return


def main():
    """
    calls parse_args, set_logger, enable_debugging, and run
    """
    args = parse_args()
    set_logger(args)
    enable_debugging(args)

    try:
        run(args)
    except Exception as error:
        handle_crash(error)
    return

if __name__ == "__main__":
    main()
