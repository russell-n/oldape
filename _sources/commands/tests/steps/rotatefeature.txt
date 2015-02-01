Rotate Command
==============

.. literalinclude:: ../rotate.feature
   :language: gherkin



Scenario: Rotate Command is called with one table
-------------------------------------------------

::

    @given("the rotate command is built with one connection")
    def rotate_one_table(context):
        context.angle = str(random.randrange(100))
        context.parser = SafeConfigParser()
        context.parser.add_section('ape')
        context.parser.set('ape', 'angles', context.angle)
        config = ConfigurationMap('test')
        config._parser = context.parser
    
        context.arguments = RotateParameters(configuration=config,
                                             section='ape')
        context.connection = MagicMock()
        context.connection.identifier = 'table1'
        context.rotate = RotateCommandUsurper(connections = [context.connection])
        context.rotate.kill_process  = MagicMock(name='killprocess')
        context.rotate.rotate = MagicMock(name='rotate')
        context.parameters = MagicMock()
        context.parameters.turntable.parameters = {context.connection.identifier: context.arguments.argument_strings.next()}
        return
    

::

    @when("the rotate command is called")
    def rotate_call(context):
        context.outcome = context.rotate(context.parameters)
        return
    

::

    @then("the connection is given the parameters for it")
    def assert_connection_parameters(context):
        expected = [call()]
        assert_that(context.rotate.kill_process.mock_calls,
                    is_(equal_to(expected)))
    
        expected = [call(connection=context.connection,
                         arguments=" {0}".format(context.angle))]
        assert_that(context.rotate.rotate.mock_calls,
                    is_(equal_to(expected)))
        return
    
    

::

    @then("the call returns the expected string")
    def check_return_string(context):
        expected = "{0}_{1}".format(context.connection.identifier,
                                          context.angle)
        assert_that(context.outcome,
                    is_(equal_to(expected)))
        return
    



Scenario: Rotate command is called and gives output
---------------------------------------------------

::

    @given("the rotate command is built without kill_process")
    def rotate_no_kill_process(context):
        context.angle = str(random.randrange(100))
        context.parser = SafeConfigParser()
        context.parser.add_section('ape')
        context.parser.set('ape', 'angles', context.angle)
        config = ConfigurationMap('test')
        config._parser = context.parser
    
        context.arguments = RotateParameters(configuration=config,
                                             section='ape')
    
        context.connection = MagicMock()
        context.rotate = RotateCommandUsurper(connections=[context.connection])
        context.rotate.kill_process  = MagicMock(name='killprocess')
        context.parameters = MagicMock()
        context.parameters.turntable.parameters = {context.connection.identifier: context.arguments.argument_strings.next()}
    
        # setup the logging
        context.logger = MagicMock()
        context.rotate._logger = context.logger
        context.stdout = "alpha bravo charlie delta".split()
        context.stderr = "ape buffalo chimpanzee".split()
        context.connection.rotate.return_value = (context.stdout,
                                                  context.stderr)
    
        return
    


  When the rotate command is called

::

    @then("the output from the connection is logged")
    def logged_output(context):
        expected = [call(line) for line in context.stdout]
        assert_that(context.logger.info.mock_calls,
                    is_(equal_to(expected)))
    
        expected = [call(RED_RESET.format(thing=line)) for line in context.stderr]
        assert_that(context.logger.error.mock_calls,
                    is_(equal_to(expected)))
        return
    

