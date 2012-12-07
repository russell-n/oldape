"""
A base for certain (simple) commands.
"""

# python standard library
from abc import ABCMeta, abstractmethod
from threading import Thread


#apetools
from apetools.baseclass import BaseClass


class BaseThreadedCommand(BaseClass):
    """
    An abstract base-class for simple commands to run in a thread
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        """
        Only instantiates the BaseClass and sets the properties
        """
        super(BaseThreadedCommand, self).__init__()
        self._logger = None
        self.stopped = False
        self.thread = None
        return

    @abstractmethod
    def run(self):
        """
        The method put into the thread.
        """
        return

    @abstractmethod
    def stop(self):
        """
        :postcondition: the thread is stopped 
        """
        return
    
    def __call__(self, *args, **kwargs):
        """
        The main interface for the command.

        Calls run and puts it in a daemonized thread.

        :postcondition: self.thread is a running thread
        """
        #import pudb;pudb.set_trace()
        self.thread = Thread(target=self.run, args=args,
                             kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()
        return

    def __del__(self):
        """
        :postcondition: `stop` is called.
        :postcondition: connection is closed
        """
        self.stop()
        return
# end class BaseThreadedCommand
