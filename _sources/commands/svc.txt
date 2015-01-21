SVC
===

A module to hold a front for android's `svc` command.


Toggle WiFi Base
----------------

.. uml::

   BaseClass <|-- ToggleWifiBase

.. module:: apetools.commands.svc
.. autosummary::
   :toctree: api

   ToggleWifiBase
   ToggleWifiBase.command
   ToggleWifiBase.__call__



Enable Wifi
-----------

.. uml::

   ToggleWifiBase <|-- EnableWifi

.. autosummary::
   :toctree: api

   EnableWifi
   EnableWifi.__call__



Disable Wifi
------------

.. uml::

   ToggleWifiBase <|-- DisableWifi

.. autosummary::
   :toctree: api

   DisableWifi
   DisableWifi.__call__
    


SVC
---

.. uml::

   BaseClass <|-- Svc

.. autosummary::
   :toctree: api

   Svc
   Svc.connection
   Svc.call_svc
   Svc.enable_wifi
   Svc.disable_wifi
   Svc.validate
    
