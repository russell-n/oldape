
# python standard library
import random
import string

# third-party
from behave import given, when, then
from hamcrest import assert_that, is_, equal_to

# this package
from apetools.connections.sshconnection import SSHConnection


@given("an ssh connection created with an identifier")
def ssh_connection_identifier(context):
    context.identifier = random.sample(string.letters, 10)
    context.connection = SSHConnection(hostname='bob',
                                       username='ted',
                                       identifier=context.identifier)
    return


@when("the connection's identifier is checked")
def check_identifier(context):
    context.outcome = context.connection.identifier   
    return


@then("the connection's identifier is the one the user set")
def assert_identifier(context):
    assert_that(context.outcome,
                is_(equal_to(context.identifier)))
    return
