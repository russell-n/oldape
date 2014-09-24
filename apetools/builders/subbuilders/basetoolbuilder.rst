Base Tool Builder
=================

A base-class for tool-builders.



.. uml::

   ConfigurationError <|-- BaseToolBuilderError

.. module:: apetools.builders.subbuilders.basetoolbuilder
.. autosummary::
   :toctree: api

   BaseToolBuilderError

::

    Parameters = namedtuple("Parameters", "name parameters".split())
    
    



.. uml::

   BaseClass <|-- BaseToolBuilder

.. autosummary::
   :toctree: api

   BaseToolBuilder
   BaseToolBuilder.product
   BaseToolBuilder.parameters

