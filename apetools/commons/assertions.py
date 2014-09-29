
def assert_equal(expected, actual):
    """
    :param:

     - `expected`: The expected Value
     - `actual`: The actual value
    """
    assert expected==actual, \
        "Expected: {e}=={a}, Actual: {e} != {a}".format(e=expected,a=actual)
    return


def assert_is(expected, actual):
    """
    :param:

     - `expected`: The expected Value
     - `actual`: The actual value
    """
    assert expected is actual, \
        "Expected: {e} is {a}, Actual: {e} is not {a}".format(e=expected,a=actual)
    return
