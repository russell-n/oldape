List Strategy
=============

A Nonparametric strategy runs commands that don't require parameters.



List Strategy
-------------

.. uml::

   list <|-- ListStrategy

.. module:: apetools.proletarians.liststrategy
.. autosummary::
   :toctree: api

   ListStrategy
   ListStrategy.remove
   ListStrategy.purge
   ListStrategy.reset



Non-Parametric Strategy
-----------------------

.. uml::

   ListStrategy <|-- NonparametricStrategy

.. autosummary::
   :toctree: api

   NonparametricStrategy
   NonparametricStrategy.__call__



Parametric Strategy
-------------------

.. uml::

   ListStrategy <|-- ParametricStrategy

.. autosummary::
   :toctree: api

   ParametricStrategy
   ParametricStrategy.__call__

