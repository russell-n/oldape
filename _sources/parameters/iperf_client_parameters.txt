Iperf Client Parameters
=======================

A module to hold client-specific parameters.



Iperf TCP Client Parameters
---------------------------

.. uml::

   IperfCommonTcpParameters <|- IperfTcpClientParameters

.. module:: apetools.parameters.iperf_client_parameters
.. autosummary::
   :toctree: api

   IperfTcpClientParameters
   IperfTcpClientParameters.client
   IperfTcpClientParameters.dualtest
   IperfTcpClientParameters.fileinput
   IperfTcpClientParameters.listenport
   IperfTcpClientParameters.num
   IperfTcpClientParameters.time
   IperfTcpClientParameters.tradeoff
   IperfTcpClientParameters.ttl



Iperf UDP Client Parameters
---------------------------

.. uml::

   IperfTcpClientParameters <|-- IperfUdpClientParameters

.. autosummary::
   :toctree: api

   IperfUdpClientParameters
   IperfUdpClientParameters.bandwidth

::

    client_parameters = {IperfParametersEnum.tcp: IperfTcpClientParameters,
                         IperfParametersEnum.udp: IperfUdpClientParameters}
    
    

