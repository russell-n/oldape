The Parameter Generator
=======================

.. _parametergeneratoruml:

ParameterGenerator
------------------

The `ParameterGenerator` maps a single config file to a series of parameters. It is intended to be used as an iterator.

.. uml::

   ParameterGenerator: TestParameter Parameters
   ParameterGenerator: forward()
   ParameterGenerator: __iter__()

