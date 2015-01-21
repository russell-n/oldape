Iperf Server Parameters
=======================

A module to hold iperf server parameters


Iperf Server Parameters
-----------------------

.. uml::

   IperfCommonTcpParameters <|-- IperfServerParameters

.. module:: apetools.parameters.iperf_server_parameters
.. autosummary::
   :toctree: api

   IperfServerParameters
   IperfServerParameters.daemon



Iperf UDP Server Parameters
---------------------------

.. uml::

   IperfServerParameters <|-- IperfUdpServerParameters

.. autosummary::
   :toctree: api

   IperfUdpServerParameters
   IperfUdpServerParameters.single_udp

::

    server_parameters = {IperfParametersEnum.tcp:IperfServerParameters,
                         IperfParametersEnum.udp: IperfUdpServerParameters}
    
    

