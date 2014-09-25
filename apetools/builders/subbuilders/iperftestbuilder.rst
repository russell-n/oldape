The Iperf Test Builder
======================

A module to hold test builders.



.. uml::

   BaseClass <|-- IperfTestBuilder
   IperfTestBuilder o- IperfCommandBuilder
   IperfTestBuilder o- IperfTest

.. module:: apetools.builders.subbuilders.iperftestbuilder
.. autosummary::
   :toctree: api

   IperfTestBuilder
   IperfTestBuilder.commands
   IperfTestBuilder.test
   
