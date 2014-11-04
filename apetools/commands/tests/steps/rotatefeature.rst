Rotate Command
==============

.. literalinclude:: ../rotate.feature
   :language: gherkin



Scenario: Rotate Command is called with one table
-------------------------------------------------

::

    @given("the rotate command is built with one connection")
    def rotate_one_table(context):
        context.parser = MagicMock(spec=ConfigParser.SafeConfigParser)
        context.arguments = RotateParameters(configuration=context.parser,
                                             section='fakesection')
        context.connection = MagicMock()
        context.rotate = RotateCommand(connections = [context.connection])
        context.rotate.kill_process  = MagicMock(name='killprocess')
        context.rotate.rotate = MagicMock(name='rotate')
        context.parameters = MagicMock()
        context.parameters.turntable.parameters = {'table1': context.arguments}
        return
    

::

    @when("the rotate command is called")
    def rotate_call(context):
        context.rotate(context.parameters)
        return
    

::

    @then("the connection is given the parameters for it")
    def assert_connection_parameters(context):
        expected = [call()]
        assert_that(context.rotate.kill_process.mock_calls,
                    is_(equal_to(expected)))
    
        expected = [call(context.connection,
                         context.arguments)]
        assert_that(context.rotate.rotate.mock_calls,
                    is_(equal_to(expected)))
        return
    

