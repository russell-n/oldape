"""
Implements a Threading convenience class based on
one found in Allen Downey's 'Little Book of Semaphores'
"""

#python library
import threading

#time to recovertest libraries
#from apetools.baseclass import BaseClass


class Thread(threading.Thread):
    """
    Calls start in the constructor and sets daemonic.
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `target`: The function pointer to run in the thread.
         - `name`: Name of the thread to use.
        """
        super(Thread, self).__init__(*args, **kwargs)
        self.daemon = True
        self.start()
        return
# end class Thread
        
