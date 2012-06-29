"""
A place to hold tools for the infrastructure.
"""

def enable_debugging(debug):
    """
    if debug is True, enables interactive debugging.

    Tries pudb, if it isn't installed, runs pdb instead.

    :param:

     - `debug`: Boolean to enable debugging.
    """
    if not debug:
        return
    try:
        import pudb
        pudb.set_trace()
        return
    except ImportError:
        import pdb
    pdb.set_trace()
    return

