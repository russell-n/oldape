Read Output
===========

A module to hold a file-like object for output.



Standard Output
---------------

.. uml::

   BaseClass <|-- StandardOutput

.. module:: apetools.commons.readoutput
.. autosummary::
   :toctree: api

   StandardOutput
   StandardOutput.__iter__
   StandardOutput.readline
   StandardOutput.readlines
   StandardOutput.read



The Validating Output
---------------------

.. uml::

   BaseClass <|-- ValidatingOutput

.. autosummary::
   :toctree: api

   ValidatingOutput
   ValidatingOutput.__iter__
   ValidatingOutput.readline
   ValidatingOutput.readlines

