"""
A module to hold a file-like object for output.
"""

# python Libraries
import Queue
from timetorecovertest.threads import threads

#time to recover Libraries
from timetorecovertest.baseclass import BaseClass
from errors import TimeoutError

EMPTY_STRING = ''
EOF = EMPTY_STRING
QUEUE_TIMEOUT = "Queue Timed Out ({t} seconds)"


class StandardOutput(BaseClass):
    """
    A class to act as a file (read-only)
    """
    def __init__(self, queue, *args, **kwargs):
        """
        :param:

         - `queue`: A queue to check for output lines.x
        """
        super(StandardOutput, self).__init__(*args, **kwargs)
        self.queue = queue
        self._iterator = None
        self.end_of_file = False
        return

    @property
    def iterator(self):
        """
        Traverses queue until EOF is encountered.

        :yield: lines from queue
        """
        line = None
        while line != EOF:
            line = self.queue.get()
            yield line
        self.end_of_file = True
        yield line
        return

    def __iter__(self):
        """
        Implemented to make this class recognize the 'in' operator
        """
        return self.iterator

    def readline(self, timeout=1):
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
        self._queue = None
        self._iterator = None
        self.empty = False
        return

    @property
    def queue(self):
        """
        :return: A queue object
        """
        if self._queue is None:
            self._queue = Queue.Queue()
        return self._queue

    @property
    def iterator(self):
        """
        :yield: validated line
        """
        for line in self.lines:
            self.validate(line)
            yield line
        yield EOF
        return

    def __iter__(self):
        return self.iterator

    def _read_one_line(self):
        """
        Puts next iterator item on the queue.

        This is meant for threaded calls.
        """
        self.queue.put(self.iterator.next())
        return

    def readline(self, timeout=1):
        """
        :return: the next line in lines
        """
        try:
            if self.empty:
                return EMPTY_STRING
            threads.Thread(target=self._read_one_line)
            line = self.queue.get(timeout=timeout)
            if line == EOF:
                self.empty = True
        except Queue.Empty:
            raise TimeoutError("Readline timed out")
        return

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
        
