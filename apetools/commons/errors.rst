Errors
======

A module to hold common exceptions.

These are made sub-classes of the OperatorError so that the hortator can recover and move on to the next hortator.

Any exception raised that isn't a sub-class of the OperatorError is unexpected and will crash the program (to make it obvious).



.. uml::

   OperatorError <|-- ConnectionError

.. module:: apetools.commons.errors
.. autosummary:: 
   :toctree: api

   ConnectionError



.. uml::

   OperatorError <|-- ConnectionWarning

.. autosummary::
   :toctree: api

   ConnectionWarning



.. uml::

   OperatorError <|-- TimeoutError

.. autosummary::
   :toctree: api

   TimeoutError



.. uml::

   OperatorError <|-- CommandError

.. autosummary::
   :toctree: api

   CommandError



.. uml::

   OperatorError <|-- ConfigurationError

.. autosummary::
   :toctree: api

   ConfigurationError



.. uml::

   OperatorError <|-- StorageError

.. autosummary::
   :toctree: api

   StorageError



.. uml::

   OperatorError <|-- AffectorError

.. autosummary::
   :toctree: api

   AffectorError
    


.. uml::

   OperatorError <|-- ArgumentError

.. autosummary::
   :toctree: api

   ArgumentError

