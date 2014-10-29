
# python standard library
import random

# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to
from mock import MagicMock

# this package
from apetools.commands.rotate import RotateParameters, BaseArguments
from apetools.lexicographers.configurationmap import ConfigurationMap


base_arguments = BaseArguments(args=[])

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
    context.configuration.get_ints.return_value = context.angles
    context.configuration.get_boolean.return_value = False
    context.configuration.get.return_value = None
    return


@when("the Rotate Parameters arguments are checked")
def check_parameters_arguments(context):
    context.argument_strings = [arguments for arguments in context.parameters.argument_strings]
    return


@then("the Rotate Parameters arguments are the angles")
def arguments_are_angles(context):
    expected = [' {0}'.format(angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))

    return


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
    def side_effect(section, option, optional, default):
        if option in results:
            return str(results[option])
    context.configuration.get_boolean.side_effect = side_effect
    return


@then("the Rotate Parameters arguments have angles and test")
def check_configuration(context):
    expected = [' --test {0}'.format(angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))

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

    context.configuration.get_ints.return_value = context.angles
    results = {'velocity': context.velocity}
    def side_effect(section, option, optional):
        if option in results:
            return str(results[option])
    context.configuration.get.side_effect = side_effect
    context.configuration.get_boolean.return_value = False
    return


@then("the Rotate Parameters arguments have angles and velocity")
def assert_velocity(context):
    expected = [' --velocity {0} {1}'.format(context.velocity, angle)
                for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))

    return


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


@then("the Rotate Parameters arguments have angles and acceleration")
def assert_acceleration(context):
    expected = [' --acceleration {0} {1}'.format(context.acceleration, angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))

    return


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


@then("the Rotate Parameters arguments have angles and deceleration")
def assert_deceleration(context):
    expected = [' --deceleration {0} {1}'.format(context.deceleration, angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))
    return


@given("Rotate Parameters built with boolean options")
def boolean_options(context):
    context.angles = get_angles()
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.section = 'lrcgaoeunth'
    context.configuration.get_ints.return_value = context.angles
    context.parameters = RotateParameters(configuration=context.configuration,
                                          section=context.section)
    context.configuration.get.return_value = None
    
    context.booleans = [option for option in base_arguments.boolean_options
                                      if random.randrange(2)]
    results = dict(zip(context.booleans,
                       len(context.booleans) * [True]))
    def side_effect(section, option, optional, default):
        if option in results:
            return str(results[option])
    context.configuration.get_boolean.side_effect = side_effect
    
    return


@then("the Rotate Parameters arguments have angles and boolean options")
def assert_booleans(context):
    boolean_expected = "".join([" --{0}".format(option) for option in context.booleans])
    expected = ['{0} {1}'.format(boolean_expected, angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))
    return


@given("Rotate Parameters built with value options")
def value_options(context):
    context.angles = get_angles()
    context.configuration = MagicMock(spec=ConfigurationMap)
    context.section = 'lrcgaoeunth'
    context.configuration.get_ints.return_value = context.angles
    context.parameters = RotateParameters(configuration=context.configuration,
                                          section=context.section)
    context.configuration.get_boolean.return_value = None
    
    context.values = [option for option in base_arguments.value_options
                                      if random.choice((True, False))]
    context.results = dict(zip(context.values,
                       [random.randrange(1, 100) for value in xrange(len(context.values))]))
    def side_effect(section, option, optional, default=None):
        if option in context.results:
            return str(context.results[option])
    context.configuration.get.side_effect = side_effect
    

    return


@then("the Rotate Parameters arguments have angles and values options")
def assert_values(context):
    value_string = "".join([" --{0} {1}".format(option, context.results[option])
                            for option in context.values])
    expected = ["{0} {1}".format(value_string, angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))
    return


@given("Rotate Parameters built with value and boolean options")
def values_booleans_options(context):
    context.angles = get_angles()
    context.configuration = MagicMock(spec=ConfigurationMap)
    
    context.configuration.get_ints.return_value = context.angles

    
    context.parameters = RotateParameters(configuration=context.configuration,
                                          section='ammagamma')

    # setup the options that use values
    context.values = [option for option in base_arguments.value_options
                                      if random.choice((True, False))]
    context.results = dict(zip(context.values,
                       [random.randrange(1, 100) for value in xrange(len(context.values))]))
    def side_effect(section, option, optional, default=None):
        if option in context.results:
            return str(context.results[option])
    context.configuration.get.side_effect = side_effect

    # setup the boolean options
    context.booleans = [option for option in base_arguments.boolean_options
                                      if random.randrange(2)]
    
    results = dict(zip(context.booleans,
                       len(context.booleans) * [True]))
    def boolean_side_effect(section, option, optional, default):
        if option in results:
            return str(results[option])
    context.configuration.get_boolean.side_effect = boolean_side_effect

    return


@then("the Rotate Parameters arguments have angles, boolean and value options")
def assert_angles_booleans_values(context):
    boolean_string = "".join([" --{0}".format(option) for option in context.booleans])
    value_string = "".join([" --{0} {1}".format(option, context.results[option])
                            for option in context.values])
    expected = ["{0}{1} {2}".format(boolean_string,
                                    value_string,
                                    angle) for angle in context.angles]
    assert_that(context.argument_strings,
                is_(equal_to(expected)))

    return
