"""
A place to put classes for operation teardowns
"""

from apetools.baseclass import BaseClass

class DummyTeardownOperation(BaseClass):
    """
    A dummy for an Operation 
    """
    def __init__(self):
        super(DummyTeardownOperation, self).__init__()
        return

    def __call__(self):
        return
# end class DummyOperationSetup

from baseoperation import BaseOperation, TOKEN_JOINER

class OperationTeardown(BaseOperation):
    """
    A class to run every operation (one per operator)
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `products`: list of builder products to execute
         """
        super(OperationTeardown, self).__init__(*args, **kwargs)

    def __call__(self):
        """
        The main interface, override if you need parameters

        :postcondition: all products called
        :return: string of joined return values from the products
        """
        return_tokens = []
        for product in self.products:
            returned = product()
            if returned:
                return_tokens.append(returned)
        return TOKEN_JOINER.join((str(token) for token in return_tokens))

# end class OperationTeardown
