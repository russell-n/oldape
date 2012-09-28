"""
A module to build test setups
"""

from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.setuptest import DummySetupTest
from tottest.commons.errors import ConfigurationError
from basetoolbuilder import BaseToolBuilder
from tottest.operations.setuptest import SetupTest

from toolbuilder import ToolBuilder

class SetupTestBuilder(BaseToolBuilder):
    """
    A class to build Test Setups
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `master`: Builder (inherited argument)
         - `config_map`: ConfigurationMap (inherited argument)
        """
        super(SetupTestBuilder, self).__init__(*args, **kwargs)
        self._plans = None
        self._builders = None
        self._products = None
        self._tool_builder = None
        return

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
                                                   ConfigOptions.test_setup_option)
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
                self._product = SetupTest(self.products)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._product = DummySetupTest()
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
# end class SetupTestBuilder