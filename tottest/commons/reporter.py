from tottest.baseclass import BaseClass


class Reporter(BaseClass):
    """
    A reporter compiles facts and reports them
    """
    def __init__(self, header, filename, storage, delimiter=",", missing="na"):
        """
        :param:

         - `header`: The header for the file
         - `filename`: The name to use for the output file
         - `storage`: the file-opener
         - `delimiter`: The column separator
         - `missing`: The missing data representation
        """
        super(Reporter, self).__init__()
        self.header = header
        self.delimiter = delimiter
        self.missing = missing
        self.filename =  filename
        self.storage = storage
        self._output = None
        self._line_length = None
        self._tokens = None
        return

    @property
    def output(self):
        """
        :return: opened file-like object
        """
        if self._output is None:
            self._output = self.storage.open(self.filename)
            self.logger.debug("Opened: {0}".format(self._output))
        return self._output

    @property
    def line_length(self):
        """
        :return: Number of tokens needed in each line
        """
        if self._line_length is None:
            self._line_length = len(self.header.split(self.delimiter))
        return self._line_length

    @property
    def tokens(self):
        """
        :return: list of tokens for next line
        """
        if self._tokens is None:
            self._tokens = []
        return self._tokens
    
    def flush(self):
        """
        Writes whatever tokens there are to the output

        :postcondition: self.tokens is None
        """
        existing = [str(token) for token in self.tokens]
        need = self.line_length - len(self.tokens)
        missing = [self.missing for missing in range(need)]
        
        line = self.delimiter.join(existing + missing)
        self.logger.debug("reporting: {0}".format(line))
        self.output.write("{0}\n".format(line))
        self._tokens = None
        return

    def add_missing(self):
        """
        :postcondition: missing token added to tokens
        """
        self(self.missing)
        return
    
    def __call__(self, token):
        """
        Appends the token and flushes line if it's complete

        :param:

         - `token`: a single column entry
        """
        self.tokens.append(token)
        if len(self.tokens) == self.line_length:
            self.flush()
        return
# end Reporter
