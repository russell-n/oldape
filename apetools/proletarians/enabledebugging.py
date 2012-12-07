"""
A place to hold tools for the infrastructure.
"""

def enable_debugging(args):
    """
    if debug is True, enables interactive debugging.

    Tries pudb, if it isn't installed, runs pdb instead.

    :param:

     - `debug`: Boolean to enable debugging.
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

