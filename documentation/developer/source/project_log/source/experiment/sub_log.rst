SubLogger
=========

Problem
-------

* Log-files need to be preserved and kept with the data they relate to

* Queueing multiple config files means the main log will have multiple tests (so you can't move it or just copy it)

Attempted Solution
------------------

Log to multiple files.

Procedure
---------

Create a *SubLogger* that takes a path and adds a file-handler with to the path::

    def add(self, logname, logger=None):
        """
        :param:

         - `logname`: path (name) for the log
         - `logger`: logging instarce to add handler to

        :postcondition: file-handler has been added to logger
        """
        if logger is None:
            logger = log_setter.logger
        handler = self.handlers[logname] = logging.FileHandler(logname)
        handler_format = logging.Formatter(self.log_format)
        handler.setFormatter(handler_format)
        handler.setLevel(self.level)
        logger.addHandler(handler)
        return


And removes the handler::

    def remove(self, logger=None, logname=None):
        """
        :param:

         - `logname`: name of the log to remove
         - `logger`: logging instance with one of self.handlers

        :postcondition: log removed from logging
        """
        if logger is None:
            logger = log_setter.logger
        try:
            logger.removeHandler(self.handlers[logname])
        except KeyError as error:
            self.logger.debug(error)
            if logname is None and len(self.handlers) == 1:
                logger.removeHandler(self.handlers[self.handlers.keys()[0]])
        return

Then in the each test-operator add a log for the test-operator at the start of the call and remove the handler at the end of the call.

Things to Check
---------------

 * Does the *INFO* level get all the information needed (or should it be a *DEBUG* level log)

 * What happens if multiple files use the same name. 

 * What should happen to the master log that watches all the tests and contains the debug information?

Update December 30, 2012
------------------------

The output of the sub-logger is missing timestamps, destroying much of the intent of creating it.

.. todo::
   Add timestamps to the output format.

