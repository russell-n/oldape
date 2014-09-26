WMIC
====

A module to hold a front for window's `wmic` command to enable/disable wifi.



Wmic Enumeration
----------------

::

    class WmicEnumeration(object):
        __slots__ = ()
        code = "code"
    # class WmicEnumeration
    
    



WmicWin32 Network Adapter
-------------------------

.. uml::

   BaseClass <|-- WmicWin32NetworkAdapter

.. module:: apetools.commands.wmic
.. autosummary::
   :toctree: api

   WmicWin32NetworkAdapter
   WmicWin32NetworkAdapter.base_command
   WmicWin32NetworkAdapter.return_expression
   WmicWin32NetworkAdapter.enable_wifi
   WmicWin32NetworkAdapter.disable_wifi
   WmicWin32NetworkAdapter.call_wmic
   WmicWin32NetworkAdapter.validate
    
