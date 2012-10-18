The Builder
===========

Builder
-------

The Builder builds Operators from a set of parameters.

.. uml::

   Builder "*" o-- Operator
   Builder o-- Hortator
   Builder "*" o-- Parameters
   Builder: parameters
   Builder: operators
   Builder: hortator


