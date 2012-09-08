Infrastructure Errors
=====================

Since the infrastructure is the highest level of exception catchers these errors aren't placed in the commons, as no one else is expected to catch them.

Although they are actually exceptions, they are called errors to avoid conflicts with python's built-in exceptions.

ConfigurationError
------------------

A ConfigurationError is raised if there is an error in the configuration file

OperatorError
-------------

An OperatorError is raised by an Operator if the operation has failed.

