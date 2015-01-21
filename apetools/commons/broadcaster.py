
from apetools.baseclass import BaseClass


class Broadcaster(BaseClass):
    """
    A broadcaster sends a single datum to multiple targets
    """
    def __init__(self, receivers):
        """
        :param:

         - `receivers`: an iterable of callable receivers
        """
        super(Broadcaster, self).__init__()
        self._receivers = None
        self.receivers = receivers
        self._temp_receivers = None
        return

    @property
    def receivers(self):
        """
        :return: receivers of broadcast
        """
        return self._receivers

    @receivers.setter
    def receivers(self, new_receivers):
        """
        :param:

         - `new_receivers`: iterable of callable receivers (or single receiver)
        """
        try:
            self._receivers = [receiver for receiver in new_receivers]
        except TypeError as error:
            self._receivers = [new_receivers]
            self.logger.debug(error)                
        return

    @property
    def temp_receivers(self):
        """
        :return: iterable of receivers to remove at next set-up
        """
        if self._temp_receivers is None:
            self._temp_receivers = []        
        return self._temp_receivers

    @temp_receivers.setter
    def temp_receivers(self, new_receivers):        
        """
        :param:

         - `new_receivers`: iterable of callable receivers (or single receiver)
        """
        try:
            self._temp_receivers = [receiver for receiver in new_receivers]
        except TypeError as error:
            self._temp_receivers = [new_receivers]
            self.logger.debug(error)                
        return
    
    def subscribe(self, receiver):
        """
        Adds a new receiver to the receivers (if it isn't already there)
        """
        if receiver not in self.receivers:
            self.logger.debug("subscribing {0}".format(receiver))
            self.receivers.append(receiver)
        return

    def unsubscribe(self, receiver):
        """
        :param:

         - `receiver`: a receiver object to remove
        """
        self._receivers = [r for r in self._receivers if r is not receiver]
        return

    def set_up(self, targets=None):
        """
        The targets are removed the next time this is called.
        
        :param:

         - `targets`: a set of temporary targets

        :postcondition: reset method for each permanent receiver called
        """
        self._temp_receivers = None
        if targets is not None:
            self.temp_receivers = targets
        for receiver in self.receivers:
            try:
                receiver.reset()
            except AttributeError as error:
                self.logger.debug(error)
                self.logger.debug("Unable to reset {0}".format(receiver))
        return
    
    def reset(self):
        """
        :postcondition: self.receivers is None
        """
        self._receivers = None
        return

    def __contains__(self, receiver):
        """
        :param:

         - `receiver`: an object
         
        :rtype: Boolean
        :return: True if item in receivers
        """
        return receiver in self.receivers

    def __iter__(self):
        """
        :return: iterator over self.receivers
        """
        return iter(self.receivers)
    
    def __call__(self, datum):
        """
        Calls each receiver with the `datum`
        
        :param:

         - `datum`: A single data item
        """
        for receiver in self.receivers:
            receiver(datum)
        return
# end class Broadcaster
