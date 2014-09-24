The NetworkedPowerSupply
========================

::

    # Total number of AC ports device can control
    MAX_PINS = 24
    # Total number of AC devices per port (A, B, C)
    PINS_PER_PORT = 8
    # Time, in seconds, to delay between turning a device on/off
    TOGGLE_DELAY = 0.05
    # Maximum number of devices that are allowed to be on at a time.
    MAX_ON = 6
    # ID if first pin
    FIRST_PIN = 0
    
    ON = "on"
    OFF = "off"
    
    



.. uml::

   BaseClass <|-- NetworkedPowerSupply

.. module:: apetools.affectors.elexol.networkedpowersupply
.. autosummary::
   :toctree: api

   NetworkedPowerSupply
   NetworkedPowerSupply.turn_switch
   NetworkedPowerSupply.check_switch_is
   NetworkedPowerSupply.attempts
   NetworkedPowerSupply.pins
   NetworkedPowerSupply.pins_per_port
   NetworkedPowerSupply.elexol
   NetworkedPowerSupply.port_status
   NetworkedPowerSupply.set_port_status
   NetworkedPowerSupply.switch_is_on
   NetworkedPowerSupply.switch_is_off
   NetworkedPowerSupply.switches_on
   NetworkedPowerSupply.turn_on_switches
   NetworkedPowerSupply.turn_off_switches
   NetworkedPowerSupply.toggle_switch
   NetworkedPowerSupply.turn_on
   NetworkedPowerSupply.turn_off
   NetworkedPowerSupply.all_off_except
   

