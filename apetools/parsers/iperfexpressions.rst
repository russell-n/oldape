Iperf Expressions
=================



Expression Base
---------------

.. uml::

   BaseClass <|-- ExpressionBase

.. module:: apetools.parsers.iperfexpressions
.. autosummary::
   :toctree: api

   ExpressionBase
   ExpressionBase.expression
   ExpressionBase.regex



Human Expression
----------------

.. uml::

   ExpressionBase <|-- HumanExpression

.. autosummary::
   :toctree: api

   HumanExpression
   HumanExpression.thread_column
   HumanExpression.expression
   HumanExpression.regex
   



Csv Expression
--------------

.. uml::

   ExpressionBase <|- CsvExpression

.. autosummary::
   :toctree: api

   CsvExpression
   CsvExpression.thread_column
   CsvExpression.expression
   CsvExpression.regex



Combined Expression
-------------------

.. uml::

   ExpressionBase <|-- CombinedExpression

.. autosummary::
   :toctree: api

   CombinedExpression
   CombinedExpression.expression
   CombinedExpression.regex
    


Parser Keys
-----------

::

    class ParserKeys(object):
        """
        A holder of the keys to the groupdict
        """
        __slots__ = ()
        units = "units"
        thread = "thread"
        start = "start"
        end = "end"
        transfer = "transfer"
        bandwidth = 'bandwidth'
    
        #csv-only
        timestamp = "timestamp"
        sender_ip = "sender_ip"
        sender_port = "sender_port"
        receiver_ip = "receiver_ip"
        receiver_port = "receiver_port"
    
        # combined
        human = "human"
        csv = "csv"
    # end class ParserKeys
    
    

