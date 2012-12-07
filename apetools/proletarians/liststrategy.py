"""
A Nonparametric strategy runs commands that don't require parameters
"""
from apetools.baseclass import BaseClass


class ListStrategy(list):
    """
    A List Strategy extends the list to use for executing commands.
    """
    def remove(self, command):
        """
        This doesn't raise an error so it can be called at any time
        
        :param:

         - `command`: an object to remove from the commands

        :postcondition: first added instance of command is removed
        """
        if command in self:
            self.pop(self.index(command))
        return

    def purge(self, command):
        """
        :param:

         - `command`: an object to remove from the commands

        :postcondition: *all* instances of command are removed
        """
        while True:
            if command in self:
                self.remove(command)
                continue
            break
        return
              
    def reset(self):
        """
        :postcondition: list is emptied
        """
        self.__init__()
        return
# end class ListStrategy

class NonparametricStrategy(ListStrategy):
    """
    A nonparametric Strategy is a container and runner of commands
    """
    def __call__(self):
        """
        :postcondition: commands called in the order they were added
        """
        for command in self:
            command()
        return
# end class NonParametricStrategy

class ParametricStrategy(ListStrategy):
    """
    A parametric strategy is a container and runner of commands.
    """
    def __call__(self, parameters):
        """
        :param:

         - `parameters`: an object that all contained items can use or ignore
        """
        for command in self:
            command(parameters)
        return
# end class ParametricStrategy
