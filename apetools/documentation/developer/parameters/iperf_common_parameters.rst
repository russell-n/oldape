Common Iperf Parameters
=======================

A module to hold iperf parameter classes.

Names of parameters match the long-options given to iperf:

    e.g. ``--port`` becomes ``IperfCommonParameters.port``

and the doc-strings cross-reference them as the short form (``-p``).

Dependencies
------------





.. _iperf-parameters-enum:

IperfParametersEnum
-------------------

Holds constants for the Iperf Parameters.

.. uml::

   IperfParametersEnum : udp
   IperfParametersEnum : tcp



.. _iperf-common-parameters:

IperfCommonParameters
---------------------

The parameters common to all Iperf command-types.

.. currentmodule:: apetools.parameters.iperf_common_parameters
.. autosummary::
   :toctree: api

   IperfCommonParameters

.. uml::

   IperfCommonParameters -|> BaseClass
   IperfCommonParameters : format
   IperfCommonParameters : interval
   IperfCommonParameters : len
   IperfCommonParameters : output
   IperfCommonParameters : port
   IperfCommonParameters : bind
   IperfCommonParameters : compatibility
   IperfCommonParameters : ipv6version
   IperfCommonParameters : reportexclude
   IperfCommonParameters : reportstyle
   IperfCommonParameters : parameter_names
   IperfCommonParameters : parallel
   IperfCommonParameters : path
   IperfCommonParameters : String parameter_names

.. note:: the parameter names attribute is there to get a list of the parameters names (presumably for the builder).



Iperf Extra Parameters
----------------------

This is a holder of valid non-iperf parameters.

.. autosummary::
   :toctree: api

   IperfExtraParameters

.. uml::

   IperfExtraParameters : directions
   IperfExtraParameters : parameters

.. note:: ``IperfExtraParameters.parameters`` is a collection of the parameters so you can check membership.

