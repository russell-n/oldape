"""
Implements a Threading convenience class based on
one found in Allen Downey's 'Little Book of Semaphores'
"""

#python library
import threading

#time to recovertest libraries
#from timetorecovertest.baseclass import BaseClass


class Thread(threading.Thread):
    """
    Calls start in the constructor and sets daemonic.
    """
    def __init__(self, target, *args, **kwargs):
        super(Thread, self).__init__(target = target, args=args, kwargs=kwargs)
        self.daemon = True
        self.start()
        return
# end class Thread
        
