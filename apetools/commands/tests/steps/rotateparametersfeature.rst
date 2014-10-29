Rotate Parameters
=================

.. literalinclude:: ../rotateparameters.feature
   :language: gherkin

::

    def get_angles():
        angles = random.randrange(1, 20)
        return [str(random.randrange(360)) for angle in xrange(angles)]
    
    



Scenario: Rotate angles set
---------------------------

::

    @given("Rotate Parameters built with only angles")
    def only_angles(context):
        context.angles = get_angles()
        context.configuration = MagicMock(spec=ConfigurationMap)
        context.section = 'lrcgaoe098u7'
        context.parameters = RotateParameters(configuration=context.configuration,
                                              section=context.section)
        context.configuration.get_ints.return_value = context.angles
        context.configuration.get.return_value = None
        return
    

::

    @when("the Rotate Parameters arguments are checked")
    def check_parameters_arguments(context):
        context.argument_strings = [arguments for arguments in context.parameters.argument_strings]
        return
    

::

    @then("the Rotate Parameters arguments are the angles")
    def arguments_are_angles(context):
        expected = [' {0}'.format(angle) for angle in context.angles]
        assert_that(context.argument_strings,
                    is_(equal_to(expected)))
    
        return
    



Scenario: Rotate angles and test set
---------------------------------------------

::

    @given("Rotate Parameters built with test flag")
    def configuration_setting(context):
        context.angles = get_angles()
        context.configuration = MagicMock(spec=ConfigurationMap)
        context.section = 'lrcgaoeunth'
        context.configuration.get_ints.return_value = context.angles
        context.parameters = RotateParameters(configuration=context.configuration,
                                              section=context.section)
        context.configuration.get.return_value = None
        results = {'test': True}
        def side_effect(section, option, optional):
            if option in results:
                return str(results[option])
        context.configuration.get_boolean.side_effect = side_effect
        return
    



  When the Rotate Parameters arguments are checked
  
::

    @then("the Rotate Parameters arguments have angles and test")
    def check_configuration(context):
        expected = [' --test {0}'.format(angle) for angle in context.angles]
        assert_that(context.argument_strings,
                    is_(equal_to(expected)))
    
        return
    



Scenario: Rotate angles and section set
---------------------------------------

::

    @given("Rotate Parameters built with a section")
    def section_parameter(context):
        context.angles = get_angles()
        context.configuration = MagicMock(spec=ConfigurationMap)
        context.section = 'pdbdipbdubpdu'
        context.parameters = RotateParameters(section=context.section,
                                              configuration=context.configuration)
        return
    


  When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and section")
    def assert_section(context):
        return
    



Scenario: Rotate angles and velocity set
----------------------------------------

::

    @given("Rotate Parameters built with a velocity")
    def velocity_parameter(context):
        context.angles = get_angles()
        context.velocity = random.randrange(100)
        context.configuration = MagicMock(spec=ConfigurationMap)
        context.section = 'sthtnh'
        context.parameters = RotateParameters(configuration=context.configuration,
                                              section=context.section)
    
        context.configuration.get_ints.return_value = context.angles
        results = {'velocity': context.velocity}
        def side_effect(section, option, optional):
            if option in results:
                return str(results[option])
        context.configuration.get.side_effect = side_effect
        context.configuration.get_boolean.return_value = False
        return
    


  When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and velocity")
    def assert_velocity(context):
        expected = [' --velocity {0} {1}'.format(context.velocity, angle)
                    for angle in context.angles]
        assert_that(context.argument_strings,
                    is_(equal_to(expected)))
    
        return
    



Scenario: Rotate angles and acceleration set
--------------------------------------------

::

    @given("Rotate Parameters built with an acceleration")
    def acceleration_option(context):
        context.angles = get_angles()
        context.acceleration = random.uniform(1, 100)
        context.configuration = MagicMock(spec=ConfigurationMap)
        context.section = 'aoeu'
        context.configuration.get_ints.return_value = context.angles
        context.parameters = RotateParameters(configuration=context.configuration,
                                              section=context.section)
        results = {'acceleration': context.acceleration}
        def side_effect(section, option, optional):
            if option in results:
                return str(results[option])
        context.configuration.get.side_effect = side_effect
        context.configuration.get_boolean.return_value = False
        return
    


When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and acceleration")
    def assert_acceleration(context):
        expected = [' --acceleration {0} {1}'.format(context.acceleration, angle) for angle in context.angles]
        assert_that(context.argument_strings,
                    is_(equal_to(expected)))
    
        return
    



Scenario: Rotate angles and deceleration set
--------------------------------------------

::

    @given("Rotate Parameters built with an deceleration")
    def deceleration_parameter(context):        
        context.angles = get_angles()
        context.deceleration = random.uniform(2, 1000)
        context.configuration = MagicMock(spec=ConfigurationMap)
        context.configuration.get_ints.return_value = context.angles
        context.section = 'lcgfshtsaoeun'
    
        results = {'deceleration': context.deceleration}
        def side_effect(section, option, optional):
            if option in results:
                return str(results[option])
        context.configuration.get.side_effect = side_effect
        context.configuration.get_boolean.return_value = False
        
        context.parameters = RotateParameters(configuration= context.configuration,
                                              section=context.section)
        return
    


When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and deceleration")
    def assert_deceleration(context):
        expected = [' --deceleration {0} {1}'.format(context.deceleration, angle) for angle in context.angles]
        assert_that(context.argument_strings,
                    is_(equal_to(expected)))
        return
    

