"""
A pipe to hold Storage Output

The differernce between the 3 pipes (start, pipe, sink)
is the way they handle a header line (if there is one)

If no header token is given, it tee's all input to
storage and the target and ignores the header.
"""

from tottest.baseclass import BaseClass
from tottest.commons.coroutine import coroutine
from tottest.commons.storageoutput import StorageOutput

EOF = ""
NEWLINE = "\n"

class StoragePipeEnum(object):
    """
    A holder of constants for the StoragePipe
    """
    __slots__  = ()
    start = "start"
    pipe = "pipe"
    sink = "sink"
# end class StoragePipeEnum

class StoragePipe(BaseClass):
    """
    A class to add a pipe interface to the Storage Output
    """
    def __init__(self, path='', role=StoragePipeEnum.pipe,
                 target=None, header_token=None, transform=None):
        """
        :param:

         - `path`: The base path to send the files to
         - `role`: start, pipe, or sink to identify what kind of pipe to open
         - `target`: the target to send lines to
         - `header_token`: the token to use for a header before the data
         - `transform`: callable function to transform sent lines
        """
        self.path = path
        self.role = role        
        self.target = target
        self.header_token = header_token
        self.transform = transform
        self._storage = None
        return

    @property
    def storage(self):
        """
        :return: opened StorageOutput
        """
        if self._storage is None:
            self._storage = StorageOutput(output_folder=self.path)
        return self._storage

    @coroutine
    def pipe_start(self, target, filename):
        """
        If a header_token was set, starts the header line
        .
        :param:

         - `target`: a started coroutine
         - `filename`: the name of te file to open

        :postcondition: pipe_start is an opened coroutine
        """
        if self.transform is not None:
            filename = self.transform.filename(filename)
        output = self.storage.open(filename)
        line = None
        if self.header_token is not None:
            output.writeline(self.header_token)
            target.send(self.header_token)

        while line !=  EOF:
            line = (yield)
            if self.transform is not None:
                line = self.transform(line)
                if line is None:
                    continue
            output.writeline(str(line))
            target.send(line)
        output.close()
        return

    @coroutine
    def pipe_sink(self, filename):
        """
        Assumes there are no further targets in the pipe.
        
        :param:

         - `filename`: the name of the file to open

        :postcondition: pipe is an opened coroutine
        """
        if self.transform is not None:
            filename = self.transform.filename(filename)
        output = self.storage.open(filename)
        line = None
        if self.header_token is not None:
            line = (yield)
            output.writeline("{0},{1}".format(line, self.header_token))
        while line !=  EOF:
            line = (yield)
            if self.transform is not None:
                line = self.transform(line)
                if line is None:
                    continue

            output.writeline(str(line))
        output.close()
        return

    

    @coroutine
    def pipe(self, target, filename):
        """
        Acts as a tee between a previous agent and the next target.
        
        :param:

         - `target`: a started coroutine
         - `filename`: the name of te file to open

        :postcondition: pipe is an opened coroutine
        """
        if self.transform is not None:
            filename = self.transform.filename
        output = self.storage.open(filename)
        line = None
        if self.header_token is not None:
            line = (yield)
            target.send("{0},{1}".format(line, self.header_token))

        while line !=  EOF:
            line = (yield)

            # transform the data if needed before passing down the pipe
            if self.transform is not None:
                line = self.transform(line)
                if line is None:
                    continue

            output.writeline(str(line))
            target.send(line)
        output.close()
        return

    def open_start(self, filename):
        """
        :param:

         - `filename`: The name of the file to open

        :return: coroutine to send lines to
        """
        target = self.target.open(filename)
        return self.pipe_start(target, filename)

    def open_sink(self, filename):
        """
        :param:

         - `filename`: the name of the file to open

        :return: coroutine to send lines to
        """
        return self.pipe_sink(filename)

    def open(self, filename):
        """
        This uses self.role to chose the type of pipe to return.
        :param:

         - `filename`: the name of the file to open

        :return: coroutine to send lines to
        """
        if self.transform is not None:
            self.transform.reset()
        if self.role == StoragePipeEnum.start:
            return self.open_start(filename)
        elif self.role == StoragePipeEnum.sink:
            return self.open_sink(filename)
        target = self.target.open(filename)
        return self.pipe(target, filename)

    def extend_path(self, subdirectory):
        """
        A pass-through to the storage's command
        
        :param:

         - `subdirectory`: A sub-directory within the output folder
        """
        self.storage.extend_path(subdirectory)
        return
# end class StoragePipe
