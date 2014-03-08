The Node Builder
================

A module to build nodes (devices) based on Operating System and connection type.

Dependencies
------------

 * :ref:`The BaseClass <base-class>`

 * :ref:`ConfigurationError <configuration-error>`

 * :ref:`The BaseDeviceEnum <base-device-enum>`

 * :ref:`The connection builders <connection-builders>`

 * :ref:`The device builders <device-builders>`

 * :ref:`The ConfigOptions <config-options>`



.. _node-builder:

The NodeBuilder Class
---------------------

.. currentmodule:: apetools.builders.subbuilders.nodebuilder
.. autosummary::
   :toctree: api

   NodeBuilder

.. uml::

   NodeBuilder -|> BaseClass
   NodeBuilder : parameters
   NodeBuilder : role
   NodeBuilder : connection
   NodeBuilder : interface
   NodeBuilder : node
   NodeBuilder : address

Example Use
-----------

The expected way to use it (to build a traffic-PC node)::

   nb = NodeBuilder(parameters=parameters, role=BaseDeviceEnum.tpc)
   node = nb.node




NodeBuilderTypes
----------------

A holder of string constants to use for types of node-builders.

.. uml::

   NodeBuilderTypes : windows
   NodeBuilderTypes : linux
   NodeBuilderTypes : android
   

#node_builders = {NodeBuilderTypes.windows:WindowsNodeBuilder}

