Iperf Parameter Builders
========================

The builders for iperf parameter objects.




IperfParametersError
--------------------

An exception to raise if there is an error in one of the parameters.

.. currentmodule:: apetools.builders.subbuilders.iperfparameterbuilders
.. autosummary::
   :toctree: api

   IperfParametersError

.. uml::

   IperfParametersError -|> ConfigurationError



IperfParametersBuilder
----------------------

The builder of iperf parameters.

.. autosummary::
   :toctree: api

   IperfParametersBuilder

.. uml::

   IperfParametersBuilder: config_map
   IperfParametersBuilder : client_parameters
   IperfParametersBuilder : server_parameters
   IperfParametersBuilder : protocol
   IperfParametersBuilder : options




Testing the IperfParametersBuilder
----------------------------------

.. autosummary::
   :toctree: api

   TestIperfParametersBuilder.test_invalid_client_option
   TestIperfParametersBuilder.test_invalid_server_option
   #TestIperfParametersBuilder.test_valid_server_option


   

