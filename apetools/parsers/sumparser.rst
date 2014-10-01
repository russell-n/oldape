Sum Parser
==========

The sumparser parses sums and logs the bandwidth sum.

::

    BITS = 'bits'
    
    



Human Expression Sum
--------------------

.. uml::

   HumanExpression <|-- HumanExpression

.. module:: apetools.parsers.sumparser
.. autosummary::
   :toctree: api

   HumanExpressionSum
   HumanExpressionSum.thread_column



CSV Expression Sum
------------------

.. uml:: 

   CsvExpression <|-- CsvExpressionSum

.. autosummary::
   :toctree: api

   CsvExpressionSum
   CsvExpressionSum.thread_column



Sum Parser
----------

.. uml::

   IperfParser <|-- SumParser

.. autosummary::
   :toctree: api

   SumParser
   SumParser.regex
   SumParser.__call__
   SumParser.pipe
    
