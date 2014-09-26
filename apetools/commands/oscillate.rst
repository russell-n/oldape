Oscillate
=========

A class to talk to an oscillator.



Oscillator Error
----------------

.. uml::

   CommandError <|-- OscillatorError

.. module:: apetools.commands.oscillate
.. autosummary::
   :toctree: api

   OscillatorError



Oscillate
---------

.. uml::

   BaseThreadedCommand <|-- Oscillate

.. module:: apetools.commands.oscillate
.. autosummary::
   :toctree: api

   Oscillate
   Oscillate.sleep
   Oscillate.event
   Oscillate.timestamp
   Oscillate.error_queue
   Oscillate.rotation_start
   Oscillate.thread
   Oscillate.run
   Oscillate.check_error
   Oscillate.generate_output
   Oscillate.stop
   Oscillate.__call__
   Oscillate.__del__



The Oscillate Event
-------------------

.. uml::

   BaseClass <|-- OscillateEvent

.. autosummary::
   :toctree: api

   OscillateEvent
   OscillateEvent.is_set
   OscillateEvent.wait
   OscillateEvent.__str__



Oscillate Stop
--------------

.. uml::

   BaseClass <|-- OscillateStop

.. autosummary::
   :toctree: api

   OscillateStop
   OscillateStop.check_output
   OscillateStop.kill_and_rotate
   OscillateStop.__call__

