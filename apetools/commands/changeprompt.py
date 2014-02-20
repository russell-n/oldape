"""
A module to change the prompt variable on a device.
Meant to help serial, telnet and other connections that read streams.
"""

#python libraries
import random
from string import ascii_letters, digits
from itertools import repeat
#from time import sleep

# apetools libraries
from apetools.baseclass import BaseClass

EMPTY_STRING = ''


class ChangePrompt(BaseClass):
    """
    Changes a prompt.
    """
    def __init__(self, adapter, length=10, variable="PS1", prompt=None):
        """
        :param:

         - `adapter`: The connection adapter for the device (needs exec_command)
         - `length`: The number of characters to use for the prompt.
         - `variable`: The name of the prompt variable on the device.
         - `prompt`: A prompt to use [default is a random one].
        """
        super(ChangePrompt, self).__init__()
        self.adapter = adapter
        self.length = length
        self.variable = variable
        self._prompt = prompt
        return

    @property
    def prompt(self):
        """
        :return: the alternative prompt to use
        """
        if self._prompt is None:
            source = ascii_letters + digits
            self._prompt = (random.choice(ascii_letters) +
                            EMPTY_STRING.join((random.choice(source)) for x in repeat(None,
                                                                                      self.length - 1)))
        return self._prompt


    def run(self):
        """
        :postcondition: prompt variable is set to new prompt.
        :return: The new prompt value.
        """
        self.adapter.prompt=self.prompt
        self.adapter.exec_command("{0}={1}".format(self.variable, self.prompt))
        # the input and output of the telnet connection will come back out of order if
        # you call it too fast (thus the sleeps)
        #sleep(0.1)
        #self.adapter.exec_command("echo $" + self.variable)
        #sleep(0.1)
        #line = ""
        # this doesn't seem very safe, but it isn't blocking so I'll let it go for now
        #while 'echo' not in line:
        #    line = output.readline(finite=False)
        #    self.logger.debug(line)
        #line = self.adapter.readline(finite=False)
        #if self.prompt not in line:
        #    self.logger.warning("missed finding the new prompt {0} in the output".format(self.prompt))

        return self.prompt
        
# end class ChangePrompt

#if __name__ == "__main__":
#    from apetools.connections import telnetadapter 
#    t = telnetadapter.TelnetAdapter("192.168.10.172")
#    c = ChangePrompt(t)
#    print c.run()
