
from synaxxx import Synaxxx


def run(args):
    naxxx = Synaxxx(args.hostname)
    if args.status:
        status = naxxx.status
        for switch in sorted(status):
            print switch, status[switch]
        return
    naxxx(args.switches)
    return
