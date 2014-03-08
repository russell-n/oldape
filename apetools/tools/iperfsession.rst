The IperfSession
================

An adapter to make the tools match the use of multiple nodes. It extracts the correct node and determines if it is acting as the client or server based on the parameters passed in, then calls on the :ref:`IperfTest <iperf-test>` to run the test.



.. currentmodule:: apetools.tools.iperfsession

Parameters
----------

The `SenderReceiver` parameters are used to bundle two nodes and identify their role.

.. uml::

   SenderReceiver -|> collections.namedtuple
   SenderReceiver : sender
   SenderReceiver : receiver
   


The Errors
----------

The `IperfConfigurationError` is raised if an error in the parameters is detected.

.. uml::

   IperfConfigurationError -|> ConfigurationError



.. _iperf-session:

The Iperf Session
-----------------

The `IperfSession` bundles nodes and the Iperf Test.

.. autosummary::
   :toctree: api

   IperfSession
   IperfSession.from_node_expression
   IperfSession.to_node_expression
   IperfSession.participants
   IperfSession.filename
   IperfSession.__call__

.. uml::

   BaseClass <|-- IperfSession
   IperfSession o- IperfTest
   IperfSession : nodes
   IperfSession : tpc
   IperfSession : filename_base
   IperfSession : __call__(parameters, filename_prefix)

* See :ref:`IperfTest <iperf-test>`    
* ``nodes`` is a dictionary of `id` (key`) to `device` (value) mappings.
* ``tpc`` is a built `device` for the traffic-generating PC 
   


The Call
--------

The ``__call__`` takes a namedtuple (`parameters`) and an optional filename-prefix that it will add to the output file (if given)::

    sender_receiver = self.particpants(parameters)
    filename = self.filename(parameters, filename_prefix)
    self.poll = self.iperf_test(sender=sender_receiver.sender,
                                receiver=sender_receiver.receiver,
                                filename=filename)


* ``self.participants`` gets the `node` and direction from the parameters and returns a `SenderReceiver`
* ``self.filename`` creates a string with the suffix `.iperf`
* ``self.poll`` is set in case meaningful output is returned and a user of the `IperfSession` wanted to retrieve it later
