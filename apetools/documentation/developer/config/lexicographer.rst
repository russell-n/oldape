The Lexicographer
=================

.. _lexicographeruml:

Lexicographer
-------------

The `Lexicographer` maps a set of config files to a set of test parameters.

.. uml::

   Lexicographer "*" o-- StaticParameters
   Lexicographer: parameters
   Lexicographer: glob


