def assert_equal(expected, actual):
    assert expected == actual, "Expected: {0} Actual: {1}".format(expected, actual)

def assert_is(expected, actual):
    assert expected is actual, "Expected: {0} Actual: {1}".format(expected, actual)

def assert_true(value):
    assert value, "{0} is not True".format(value)
