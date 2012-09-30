"""
An adapter to make the tools match the use of multiple nodes.
"""
import re
from collections import namedtuple

from tottest.baseclass import BaseClass
from tottest.commons.errors import ConfigurationError

SenderReceiver = namedtuple("SenderReceiver", "sender receiver".split())

class IperfConfigurationError(ConfigurationError):
    """
    An exception to raise if the direction is unknown.
    """
# end class IperfConfigurationError

class IperfSession(BaseClass):
    """
    A bundler of nodes and the iperfcommand.
    """
    def __init__(self, iperf_command, nodes, tpc):
      """
      :param:

       - `iperf_command`: a bundle of parameters and storage
       - `nodes`: id:device pairs
       - `tpc`: traffic PC device
      """
      super(IperfSession, self).__init__()
      self.iperf_command = iperf_command
      self.nodes = nodes
      self.tpc = tpc
      self._to_node_expression = None
      self._from_node_expression = None
      self.poll = None
      return

    @property
    def from_node_expression(self):
        """
        Expects `from_node`, `uplink`, `send`, `transmit`, `tx`
        
        :return: compiled regex to match TPC <-- Node        
        """
        if self._from_node_expression:
            self._from_node_expression = re.compile("f.*|s.*|t[rx].*|u.*")
        return self._from_node_expression

    @property
    def to_node_expression(self):
        """
        Assumes something like `to_node`, `downlink`, `receive`, `rx`
        
        :return: compiled regex to match direction of traffic TPC --> Node
        """
        if self._expression is None:
            self._expression = re.compile("to.*|d.*|r.*")
        return self._expression

    def particpants(self, parameters):
        """
        :param:

         - `parameters`: namedtuple passed in to call

        :return: 
        """
        node = self.nodes[parameters.nodes.parameters]
        direction = parameters.directions.parameters
        if self.to_dut_expression.match(direction):
            return SenderReceiver(sender=self.tpc, receiver=node)
        elif self.from_dut_expression.match(direction):
            return SenderReceiver(sender=node, receiver=self.tpc)
        raise IperfConfigurationError("Unknown traffic direction: '{0}'".format(direction))
        return

    def filename(self, parameters):
        """
        :param:

         - `parameters`: Namedtuple passed in to __call__      
         
        :return: filename derived from the parameters
        """
        name = []
        name.append(parameters.nodes.parameters)
        name.append(parameters.directions.parameters)
        try:
            name.append(parameters.ssids.parameters)
        except AttributeError as error:
            self.logger.debug(error)
        return "_".join(name) + ".iperf"
    
    def __call__(self, parameters):
        """
        :param:

         - `parameters`: namedtuple with nodes and direction parameters
        """
        sender_receiver = self.particpants(parameters)
        filename = self.filename(parameters)
        self.poll = self.iperf_command(sender=sender_receiver.sender,
                                       receiver=sender_receiver.receiver,
                                       filename=filename)
        return
# end class IperfSession
    
