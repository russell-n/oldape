Iperf Parameter Builders
========================

The builders for iperf parameter objects.




IperfParametersError
--------------------

An exception to raise if there is an error in one of the parameters.

.. module:: apetools.builders.subbuilders.iperfparameterbuilders
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

