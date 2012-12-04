"""
A module to hold a file-like object for output.
"""

# python Libraries
import Queue
import socket

#time to recover Libraries
from tottest.baseclass import BaseClass
from errors import TimeoutError

EMPTY_STRING = ''
EOF = EMPTY_STRING
SPACE = ' '
QUEUE_TIMEOUT = "Queue Timed Out ({t} seconds)"


class StandardOutput(BaseClass):
    """
    A class to act as a file (read-only)
    """
    def __init__(self, source,  *args, **kwargs):
        """
        :param:

         - `source`: the source file
        """
        super(StandardOutput, self).__init__(*args, **kwargs)
        self._logger = None
        self.source = source
        self.end_of_file = False
        return

    def __iter__(self):
        """
        Implemented to make this class recognize the 'in' operator
        """
        line = None
        while line != EOF:
            line = self.readline()
            yield line
        self.end_of_file = True
        yield line
        return

    def readline(self, timeout=10):
        """
        :param:

         - `timeout`: The length of time to wait for output
        """
        if not self.end_of_file:
            try:
                line = self.queue.get(timeout=timeout)
                if line == EOF:
                    self.end_of_file = True
                return line
            except Queue.Empty:
                self.logger.debug(QUEUE_TIMEOUT.format(t=timeout))
                raise TimeoutError(QUEUE_TIMEOUT.format(t=timeout))
        return EOF

    def readlines(self):
        """
        :return: lisf of lines of output.
        """
        line = None
        lines = []
        for line in self:
            lines.append(line)
        return lines

    def read(self):
        """
        :return: output as a single string
        """
        return EMPTY_STRING.join(self.readlines())
# end class StandardOutput

class ValidatingOutput(BaseClass):
    """
    A ValidatingOutput reads from an iterable and validates the lines.
    """
    def __init__(self, lines, validate, *args, **kwargs):
        """
        :param:

         - `lines`: A file-like object
         - `validate`: A function to validate lines
        """
        super(ValidatingOutput, self).__init__(*args, **kwargs)
        self.lines = lines
        self.validate = validate
        self.empty = False
        return

    def __iter__(self):
        """
        :yield: validated line
        """
        line = None
        while line != EOF:
            try:
                line = self.lines.readline()
            except socket.timeout:
                self.logger.debug("Socket timed out")
                line = SPACE
            self.validate(line)
            yield line
        #yield EOF
        return

    def readline(self, timeout=1):
        """
        :return: the next line in lines
        """
        if self.empty:
            return EMPTY_STRING
        line = self.lines.readline()
        self.validate(line)
        return line

    def readlines(self):
        """
        :return: list of validated lines
        """
        lines = []
        line = None
        while line != EOF:
            line = self.readline()
            lines.append(line)
        lines.append(EOF)
        return lines

    def read(self):
        """
        :return: validated lines joined as a string
        """
        return EMPTY_STRING.join(self.readlines())
# end class ValidatingOutput
        
