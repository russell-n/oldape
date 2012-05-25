#! /usr/bin/env python
"""
The entry point for stand-alone invocation (runs the argumentbureau).

"""
# python Libraries
import os
import sys
import signal

# testrunner Libraries
from infrastructure.argumentparser import ArgumentParser
from infrastructure.enabledebugging import enable_debugging
from log_setter import set_logger


def main():
    """
    The main entrance point. Relies on functions being defined in argparser.
    """
    parser = ArgumentParser()
    args = parser.args
    if args is None:
        raise Exception("Something's wrong with the ArgumentParser")
        return
    set_logger(args)
    enable_debugging(args.enable_debugging)

    watcher()
    args.function(args)
    return

def watcher():
    """
    The watcher watches for signal interrupts
    """
    child = os.fork()
    if child == 0:
        return
    try:
        os.wait()
    except KeyboardInterrupt as interrupt:
        print interrupt
        os.kill(child, signal.SIGKILL)
    sys.exit()
    return

if __name__ == "__main__":
    import pudb;pudb.set_trace()
    main()
