"""
A set of tests that check different cases for the network tester
"""
#python

#third-party
from mock import MagicMock
import nose

#from apetools.tools import networkcheck

from apetools.tools import timetorecovery as ttr
from apetools.tools import networktester
from apetools.commons import errors

def test_case_1():
    """
    :description: dut and tpc ping each other

    :assert: Nothing happens
    """
    # Setup the mock ttr test to the tpc (linux)
    tpc_ttr = MagicMock()
    tpc_ttr.run.return_value = ttr.TTRData(5, '0.98')
    dut_ttr = MagicMock()
    dut_ttr.run.return_value = ttr.TTRData(10, '9.2')

    testers = [tpc_ttr, dut_ttr]
    tester = networktester.NetworkTester(testers)
    tester.run()
    assert True
    return

@nose.tools.raises(errors.ConnectionError)
def test_case_2():
    """
    :description: dut pings pc, ping fails to ping dut

    :assert: Raises ConnectionError
    """
    tpc_ttr = MagicMock()
    tpc_ttr.run.return_value = None
    dut_ttr = MagicMock()
    dut_ttr.run.return_value = ttr.TTRData(2, '0.9')

    tester = networktester.NetworkTester([dut_ttr, tpc_ttr])
    tester.run()
    return

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test_case_2()
