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
    A bundler of nodes and the iperftest
    """
    def __init__(self, iperf_test, nodes, tpc, filename_base=None):
      """
      :param:

       - `iperf_test`: a bundle of parameters and storage
       - `nodes`: id:device pairs
       - `tpc`: traffic PC device
       - `filename_base`: An optional string to add to the filename
      """
      super(IperfSession, self).__init__()
      self.iperf_test = iperf_test
      self.nodes = nodes
      self.filename_base = filename_base
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
        if self._from_node_expression is None:
            self._from_node_expression = re.compile("f.*|s.*|t[rx].*|u.*")
        return self._from_node_expression

    @property
    def to_node_expression(self):
        """
        Assumes something like `to_node`, `downlink`, `receive`, `rx`
        
        :return: compiled regex to match direction of traffic TPC --> Node
        """
        if self._to_node_expression is None:
            self._to_node_expression = re.compile("to.*|d.*|r.*")
        return self._to_node_expression

    def particpants(self, parameters):
        """
        :param:

         - `parameters`: namedtuple passed in to call

        :return: 
        """
        node = self.nodes[parameters.nodes.parameters]
        direction = parameters.iperf_directions.parameters
        if self.to_node_expression.match(direction):
            return SenderReceiver(sender=self.tpc, receiver=node)
        elif self.from_node_expression.match(direction):
            return SenderReceiver(sender=node, receiver=self.tpc)
        raise IperfConfigurationError("Unknown traffic direction: '{0}'".format(direction))
        return

    def filename(self, parameters, filename_prefix):
        """
        :param:

         - `parameters`: Namedtuple passed in to __call__      
         - `filename_prefix`: a prefix (not really) to add to the name
        :return: filename derived from the parameters
        """
        name = []
        name.append(parameters.nodes.parameters)
        if filename_prefix:
            name.append(filename_prefix)
        if self.filename_base is not None:
            name.append(self.filename_base)                    
        return "_".join(name) + ".iperf"
    
    def __call__(self, parameters, filename_prefix = None):
        """
        :param:

         - `parameters`: namedtuple with nodes and direction parameters
         - `filename_prefix`: prefix to prepend to the filename
        """
        sender_receiver = self.particpants(parameters)
        filename = self.filename(parameters, filename_prefix)
        self.poll = self.iperf_test(sender=sender_receiver.sender,
                                    receiver=sender_receiver.receiver,
                                    filename=filename)
        return
# end class IperfSession
    
