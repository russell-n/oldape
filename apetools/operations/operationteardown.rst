Operation Teardown
==================

A place to put classes for operation teardowns.



Dummy Teardown Operation
------------------------

.. uml::

   BaseClass <|-- DummyTeardownOperation

.. module:: apetools.operations.operationteardown
.. autosummary::
   :toctree: api

   DummyTeardownOperation
   DummyTeardownOperation.__call__



Operation Teardown
------------------

.. uml::

   BaseOperation <|-- OperationTeardown

.. autosummary::
   :toctree: api

   OperationTeardown
   OperationTeardown.__call__

