WPA CLI
=======

A module to query the device for interface information.




Wpa Cli Command
---------------

.. uml::

   BaseClass <|-- WpaCliCommand

.. module:: apetools.commands.wpacli
.. autosummary::
   :toctree: api

   WpaCliCommand
   WpaCliCommand.status
   WpaCliCommand.ip_address
   WpaCliCommand.ssid
   WpaCliCommand.supplicant_state
   WpaCliCommand.interface
   WpaCliCommand.mac_address
   WpaCliCommand._match
   WpaCliCommand.__str__






