The Argument Parser
===================

ArgumentParser
--------------

.. uml::

   ArgumentParser "1" o-- Strategerizer
   ArgumentParser: parser
   ArgumentParser: args
   ArgumentParser: strategerizer

The ArgumentParser interprets command line arguments to choose a strategy to execute.


