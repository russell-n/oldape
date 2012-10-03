"""
A module to build operations
"""

from abc import ABCMeta, abstractproperty
from tottest.operations.baseoperation import DummyOperation
from tottest.lexicographers.config_options import ConfigOptions
from tottest.commons.errors import ConfigurationError
from basetoolbuilder import BaseToolBuilder

from toolbuilder import ToolBuilder

class BaseOperationBuilder(BaseToolBuilder):
    """
    A class to build Test Setups
    """
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `master`: Builder (inherited argument)
         - `config_map`: ConfigurationMap (inherited argument)
        """
        super(BaseOperationBuilder, self).__init__(*args, **kwargs)
        self._logger = None
        self._plans = None
        self._builders = None
        self._products = None
        self._tool_builder = None
        self._operation = None
        self._config_option = None
        return

    @abstractproperty
    def config_option(self):
        """
        :return: Config file option corresponding to the operation
        """
        return self._config_option

    @abstractproperty
    def operation(self):
        """
        :return: class definition for the product
        """
        return self._operation

    @property
    def tool_builder(self):
        """
        :return: ToolBuilder aggregator
        """
        if self._tool_builder is None:
            self._tool_builder = ToolBuilder()
        return self._tool_builder

    @property
    def plans(self):
        """
        :return: list of options form the setup_test value
        """
        if self._plans is None:
            self._plans = self.config_map.get_list(ConfigOptions.test_section,
                                                   self.config_option)
        return self._plans

    @property
    def builders(self):
        """ 
        :return: list of builders made from plans
        """
        if self._builders is None:
            if self.previous_parameters is None:
                self.previous_parameters = []
            self._builders = []
            for plan in self.plans:
                builder = getattr(self.tool_builder, plan)(master=self.master,
                                                           config_map=self.config_map,
                                                           previous_parameters=self.previous_parameters)
                self.previous_parameters = builder.parameters
                self._builders.append(builder)
        return self._builders

    @property
    def products(self):
        """
        :return: list of products from the builders
        """
        if self._products is None:
            self._products = [builder.product for builder in self.builders]
        return self._products
    
    @property
    def product(self):
        """
        :return: Test Setup object
        
        """
        if self._product is None:
            try:
                self._product = self.operation(self.products)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._product = DummyOperation()
        return self._product

    @property
    def parameters(self):
        """
        :return: list of named-tuple parameters for the products
        """
        if self._parameters is None:
            try:
                self._parameters = self.builders[-1].parameters
            except (ConfigurationError, IndexError) as error:
                self.logger.debug(error)
                self._parameters = []
        return self._parameters
# end class BaseOperationBuilder