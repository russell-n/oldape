IpConfig
========

A module to extract information from `ipconfig`.







The Ipconfig Enum
-----------------


.. code:: python

    class IpconfigEnum(object):
        __slots__ = ()
        address = "address"
    # end class IpConfigEnum
    



The Ipconfig Error
------------------

.. uml::

   CommandError <|-- IpconfigError

.. module:: apetools.commands.ipconfig
.. autosummary::
   :toctree: api

   IpconfigError




The Ipconfig Command
--------------------

.. uml::

   BaseClass <|-- Ipconfig

.. autosummary::
   :toctree: api
   
   Ipconfig
   Ipconfig.ip_expression
   Ipconfig.address



