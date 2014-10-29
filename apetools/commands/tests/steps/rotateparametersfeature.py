
# python standard library
import random

# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to
from mock import MagicMock

# this package
from apetools.commands.rotate import RotateParameters
from apetools.lexicographers.configurationmap import ConfigurationMap


def get_angles():
    angles = random.randrange(1, 20)
    return [str(random.randrange(360)) for angle in xrange(angles)]


@given("Rotate Parameters built with only angles")
def only_angles(context):
    context.angles = get_angles()
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.section = 'lrcgaoe098u7'
    context.parameters = RotateParameters(configuration=context.configuration,
                                          section=context.section)
    return


@when("the Rotate Parameters arguments are checked")
def check_parameters_arguments(context):
    context.argument_strings = [arguments for arguments in context.parameters.argument_strings]
    return


@then("the Rotate Parameters arguments are the angles")
def arguments_are_angles(context):
    return


@given("Rotate Parameters built with a configuration")
def configuration_setting(context):
    context.angles = get_angles()
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.section = 'lrcgaoeunth'
    context.parameters = RotateParameters(configuration=context.configuration,
                                          section=context.section)
    return


@then("the Rotate Parameters arguments have angles and configuration")
def check_configuration(context):
    return


@given("Rotate Parameters built with a section")
def section_parameter(context):
    context.angles = get_angles()
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.section = 'pdbdipbdubpdu'
    context.parameters = RotateParameters(section=context.section,
                                          configuration=context.configuration)
    return


@then("the Rotate Parameters arguments have angles and section")
def assert_section(context):
    return


@given("Rotate Parameters built with a velocity")
def velocity_parameter(context):
    context.angles = get_angles()
    context.velocity = random.randrange(100)
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.section = 'sthtnh'
    context.parameters = RotateParameters(configuration=context.configuration,
                                          section=context.section)
    return


@then("the Rotate Parameters arguments have angles and velocity")
def assert_velocity(context):
    return


@given("Rotate Parameters built with an acceleration")
def acceleration_option(context):
    context.angles = get_angles()
    context.acceleration = random.uniform(1, 100)
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.section = 'aoeu'
    context.parameters = RotateParameters(configuration=context.configuration,
                                          section=context.section)
    return


@then("the Rotate Parameters arguments have angles and acceleration")
def assert_acceleration(context):
    return


@given("Rotate Parameters built with an deceleration")
def deceleration_parameter(context):        
    context.angles = get_angles()
    context.deceleration = random.uniform(2, 1000)
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.configuration.get_ints.return_value = context.angles
    context.section = 'lcgfshtsaoeun'

    results = {'deceleration': context.deceleration}
    def side_effect(section, option, optional, default):
        return results[option]
    context.configuration.get_float.side_effect = side_effect


    
    context.parameters = RotateParameters(configuration= context.configuration,
                                          section=context.section)
    return


@then("the Rotate Parameters arguments have angles and deceleration")
def assert_deceleration(context):
    expected = [' --deceleration {0} {1}'.format(context.deceleration, angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))
    return
