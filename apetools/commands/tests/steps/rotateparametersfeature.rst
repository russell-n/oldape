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
        context.parameters = RotateParameters(angles=context.angles)
        return
    

::

    @when("the Rotate Parameters arguments are checked")
    def check_parameters_arguments(context):
        context.arguments = [argument for argument in context.parameters.arguments]
        return
    

::

    @then("the Rotate Parameters arguments are the angles")
    def arguments_are_angles(context):
        expected = [" {0}".format(angle) for angle in context.angles]
        assert_that(context.arguments,
                    is_(equal_to(expected)))
        return
    



Scenario: Rotate angles and configuration set
---------------------------------------------

::

    @given("Rotate Parameters built with a configuration")
    def configuration_setting(context):
        context.angles = get_angles()
        context.configuration = 'aoeusnthlrcg'
        context.parameters = RotateParameters(angles=context.angles,
                                              configuration=context.configuration)   
        return
    



  When the Rotate Parameters arguments are checked
  
::

    @then("the Rotate Parameters arguments have angles and configuration")
    def check_configuration(context):
        expected = [" --configuration {0} {1}".format(context.configuration,
                                                     angle) for angle in context.angles ]
        assert_that(context.arguments,
                    is_(equal_to(expected)))
        return
    



Scenario: Rotate angles and section set
---------------------------------------

::

    @given("Rotate Parameters built with a section")
    def section_parameter(context):
        context.angles = get_angles()
        context.section = 'pdbdipbdubpdu'
        context.parameters = RotateParameters(angles=context.angles,
                                              section=context.section)
        return
    


  When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and section")
    def assert_section(context):
        expected = [' --section {0} {1}'.format(context.section,
                                                angle) for angle in context.angles]
        assert_that(context.arguments,
                    is_(equal_to(expected)))
        return
    



Scenario: Rotate angles and velocity set
----------------------------------------

::

    @given("Rotate Parameters built with a velocity")
    def velocity_parameter(context):
        context.angles = get_angles()
        context.velocity = random.randrange(100)
        context.parameters = RotateParameters(angles=context.angles,
                                              velocity=context.velocity)
        return
    


  When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and velocity")
    def assert_velocity(context):
        expected = [' --velocity {0} {1}'.format(context.velocity,
                                                 angle) for angle in context.angles]
        assert_that(context.arguments,
                    is_(equal_to(expected)))
        return
    



Scenario: Rotate angles and acceleration set
--------------------------------------------

::

    @given("Rotate Parameters built with an acceleration")
    def acceleration_option(context):
        context.angles = get_angles()
        context.acceleration = random.uniform(1, 100)
        context.parameters = RotateParameters(angles=context.angles,
                                              acceleration=context.acceleration)
        return
    


When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and acceleration")
    def assert_acceleration(context):
        expected = [" --acceleration {0} {1}".format(context.acceleration,
                                                     angle) for angle in context.angles]
        assert_that(context.arguments,
                    is_(equal_to(expected)))
        return
    



Scenario: Rotate angles and deceleration set
--------------------------------------------

::

    @given("Rotate Parameters built with an deceleration")
    def deceleration_parameter(context):
        context.angles = get_angles()
        context.deceleration = random.uniform(2, 1000)
        context.parameters = RotateParameters(angles=context.angles,
                                              deceleration=context.deceleration)
        return
    


When the Rotate Parameters arguments are checked

::

    @then("the Rotate Parameters arguments have angles and deceleration")
    def assert_deceleration(context):
        expected = [" --deceleration {0} {1}".format(context.deceleration,
                                                     angle) for angle in context.angles]
        assert_that(context.arguments,
                    is_(equal_to(expected)))
        return
    

