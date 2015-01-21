The Synaxxx
===========
A module to adapt the Synaccess network controller.



.. uml::

   CommandError <|-- SynaxxxError

.. module:: apetools.affectors.synaxxx.synaxxx
.. autosummary::
   :toctree: api

   SynaxxxError



.. uml::

   BaseClass <|-- Synaxxx
   Synaxxx o- Sleep
   Synaxxx o- Telnet

.. autosummary::
   :toctree: api

   Synaxxx
   Synaxxx.sleeper
   Synaxxx.client
   Synaxxx.status
   Synaxxx.exec_command
   Synaxxx.lines
   Synaxxx.validate
   Synaxxx.all_off
   Synaxxx.all_on
   Synaxxx.turn_on
   Synaxxx.__call__
   Synaxxx.increment_sleep
   Synaxxx.show_status
   Synaxxx.close

