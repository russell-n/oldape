The Network Topology
====================

This is an abstracted map of the network:

.. digraph:: BaseTopology

   C -> N
   C -> T
   N -> A [style="dotted", dir="both"]
   A -> T [dir="both"]

.. csv-table:: Base Legend
   :header: Label,Value
   
   **C**, the *Control PC* (where the *ape* is run and the configuration file is located)
   **N**, a *Node* (e.g. a tablet or PC configured in the :ref:`NODES <node-configuration>` section)
   **T**,the *Traffic PC* (used to generate traffic configured in the :ref:`TRAFFIC_PC <traffic-pc>` section)
   **A**, The Wireless Access Point
   --, Cabled Ethernet connection
   . ., Wireless Ethernet connection

Adding Rotation
---------------

To add rotations the topology is extended:

.. digraph:: RotationTopology

   C -> N
   C -> T
   C -> R
   N -> A [style="dotted", dir="both"]
   A -> T [dir="both"]

.. csv-table:: Rotation Legend
   :header: Label,Value
   
   **C**, the *Control PC* (where the *ape* is run and the config-file is located)
   **N**, a *Node* (e.g. a tablet or PC configured in the :ref:`NODES <node-configuration>` section)
   **T**,the *Traffic PC* (used to generate traffic configured in the :ref:`TRAFFIC_PC <traffic-pc>` section)
   **R**, The *Rotation Control* (PC attached to the turntable configured in the :ref:`ROTATE <rotate-configuration>` section) 
   **A**, Wireless Access Point
   --, Cabled Ethernet connection
   . ., Wireless Ethernet connection

Adding Power-Switching
----------------------

To add power-switching the topology is extended:

.. digraph:: RotationTopology

   C -> N
   C -> T
   C -> R
   C -> P
   N -> A [style="dotted", dir="both"]
   A -> T [dir="both"]

.. csv-table:: Rotation Legend
   :header: Label,Value
   
   **C**, the *Control PC* (where the *ape* is run and the config-file is located)
   **N**, a *Node* (e.g. a tablet or PC configured in the :ref:`NODES <node-configuration>` section)
   **T**,the *Traffic PC* (used to generate traffic configured in the :ref:`TRAFFIC_PC <traffic-pc>` section)
   **R**, The *Rotation Control* (PC attached to the turntable configured in the :ref:`ROTATE <rotate-configuration>` section) 
   **P**,  set of *Power Switches* (configured in the :ref:`POWERON <poweron-configuration>`)
   **A**, Wireless Access point
   --, Cabled Ethernet connection
   . ., Wireless Ethernet connection

