"""
The purpose of the Popen Producer is to provide ways to read from the standard out and standard error without allowing incomplete file outputs to block the execution of the program.
"""

import subprocess 
import threading
import Queue
from time import time as now
from sys import maxint
import shlex

from apetools.baseclass import BaseClass
from sharedcounter import SharedCounter

EOF = ""
SPACE = ' '

class PopenProducer(BaseClass):
    """
    The subprocess.Popen Producer executes a command when its process or one of its files is requested
    """
    def __init__(self, command, timeout=10):
        """
        :param:

         - `command`: String to pass to a subprocess to execute
         - `timeout`: the amount of time to allow a readline to return
        """
        super(PopenProducer, self).__init__()
        self.command = command
        self.timeout = timeout
        self._process = None
        self._stdout = None
        self._stderr = None
        self._counter = None
        self._lock = None
        return

    @property
    def lock(self):
        """
        :return: a re-entrant lock
        """
        if self._lock is None:
            self._lock = threading.Lock()
        return self._lock

    @property
    def counter(self):
        """
        :return: SharedCounter
        """
        if self._counter is None:
            self._counter = SharedCounter()
        return self._counter
    
    @property
    def process(self):
        """
        :return: a subprocess.Popen object
        """
        if self._process is None:
            self.logger.debug("Creating subprocess with command: {0}".format(self.command))
            self._process = subprocess.Popen(shlex.split(self.command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            count = self.counter.increment()
            assert count == 1
        return self._process

    @property
    def stdout(self):
        """
        :return: a subprocess.PopenFile containing the stdout of the process
        """
        if self._stdout is None:
            self.logger.debug("Creating Stdout for subprocess `{0}` (PID {1})".format(self.command, self.process.pid))
            output = self.process.stdout
            
            count = self.counter.increment()
            assert count > 1
            
            self._stdout = PopenFile(output, timeout=self.timeout, process=self.process, counter=self.counter, lock=self.lock)
        return self._stdout

    @property
    def stderr(self):
        """
        :return: a subprocess.PopenFile containing the stderr of the process
        """
        if self._stderr is None:
            self.logger.debug("Creating Stderr for subprocess `{0}` (PID {1})".format(self.command, self.process.pid))
            err = self.process.stderr
            self.logger.debug("Incrementing the counter")
            count = self.counter.increment()
            assert count > 1
            self._stderr = PopenFile(err, timeout=self.timeout, process=self.process, counter=self.counter, lock=self.lock)
            self.logger.debug("returning PopenFile with stderr")
        return self._stderr

    def __del__(self):
        """
        It appears that the way python's garbage collection works, the counter is unnecessary.
        
        :postconditions:

           - counter decremented
           - if counter = 0, process killed
        """
        if self.counter.decrement() == 0:
            self.logger.debug("Killing process `{0}` (PID: {1})".format(self.command, self.process.pid))
            with self.lock:
                if self.process.poll() is None:
                    try:
                        self.process.kill()
                    except OSError as error:
                        self.logger.debug(error)
        return
# end class PopenProducer
    
class PopenFile(BaseClass):
    """
    A container for a process' readable file-outputs
    """
    def __init__(self, file_object, process, lock, counter=None, timeout=10, queue=None):
        """
        :param:

         - `file_object`: stdout or stderr
         - `counter`: A shared counter to track how many users of the process are alive
         - `process`: process that created the file_object
         - `timeout`: max time to try a readline
         - `queue`: where to put output read from the file_object
        """
        super(PopenFile, self).__init__()
        self.file_object = file_object
        self.timeout = timeout
        self.counter = counter
        self._queue = queue
        self.started = False
        self.closed = False
        self.stop = False
        self.process = process
        self.lock = lock
        return

    @property
    def queue(self):
        """
        :return: Queue.Queue for lines of output
        """
        if self._queue is None:
            self._queue = Queue.Queue()
        return self._queue

    def run(self):
        """
        :postcondition: lines read from the file and put on the Queue
        """
        self.logger.debug("Starting to feed the queue")
        line = None
        while line != EOF:
            with self.lock:
                try:
                    line = self.file_object.readline()
                except AttributeError as error:
                    self.logger.debug(error)
                    line = EOF
                    if self.closed:
                        self.logger.debug("The file_object was already deleted by the close() method")
                    else:
                        self.logger.debug("The file_object was deleted by someone else.")
            self.queue.put(line)
            if self.stop:
                self.queue.put(EOF)
                return
        return

    def start(self):
        """
        :postcondition: self.run executing as self.thread
        """
        if self.started:
            return
        self.logger.debug("Starting thread")
        self.started = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        self.logger.debug("Active thread count: {0}".format(threading.active_count()))
        return

    def readline(self, timeout=None):
        """
        :return: Next item in queue or EOF if it times out
        """
        if timeout is None:
            timeout = self.timeout
        self.start()
        #self.logger.debug("Pulling from Queue with timeout = {0}".format(timeout))
        try:
            return self.queue.get(block=True, timeout=timeout)
        except Queue.Empty:
            if self.process.poll() is not None:
                return EOF
        return

    def read(self, timeout=None):
        """
        :param:

         - `timeout`: number of seconds to try and read.
        :return: lines from the queue joined as a string
        """
        self.start()
        output = EOF
        line = None

        max_time = maxint
        if timeout is not None:
            max_time = now() + timeout
            
        while all((line != EOF, self.process.poll() is None,  now() < max_time)):
            try:
                line = self.queue.get(block=False)
            except Queue.Empty:
                continue
            output += line
        return output

    def close(self):
        """
        :postcondition: file_object has been closed and self.closed is True
        """
        with self.lock:
            if self.file_object is not None:
                self.logger.debug("Closing the file")
                self.file_object.close()
                if self.process.poll() is None:
                    self.logger.debug("Killing process (PID: {0})".format(self.process.pid))
                    try:
                        self.process.kill()
                    except OSError as error:
                        # to avoid race-condition exception between end of command and this call
                        self.logger.debug(error)
                self.closed = True
            self.logger.debug("File Closed")
        return
        
    def __iter__(self):
        """
        SPACE is yielded on timeout so it isn't mistaken for an EOF
        
        :yield: next readline() or SPACE if it times out
        """
        self.start()
        line = None
        while line != EOF:
            line = self.readline(self.timeout)
            if line is not None:
                yield line
            else:
                yield SPACE
        return

    def __del__(self):
        """
        :postcondition: if process was given, self.close called
        """
        self.stop = True
        if self.process is not None:
            if self.counter.decrement() == 0:
                self.close()
        return
# end class PopenProducer

if __name__ == "__main__":
    def start_ping():
        p = PopenProducer("ping localhost")
        e = p.stderr
        return p.stdout
    f = start_ping()
    
    count = 0
    for line in f:
        print line
        if count == 10:
            del(f)
            print "premature break"
            break
        
        count += 1    
    # now the reason for this whole thing
    p = PopenProducer("cat")
    f = p.stdout
    print "Trying the cat"
    for line in f:
        print line
    del(p)

    # now stderr

    p = PopenProducer("ping -c")
    o = p.stdout
    for line in o:
        print line

    print "checking stderr"
    e = p.stderr
    for line in e:
        print line

    del(p)
