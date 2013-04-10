The Degenerate Oscillator
=========================

Although the purpose of the oscillation is to randomize the angles to eliminate any bias, a request was made to use the turn-table to do a single slow rotation and correlate the throughput as it spins.

Problem 1
---------

The turn-table needs to be reset between tests or it drifts off over time.

Experiment 1
------------

Put the oscillate stop in the Test-Teardown and let it go back to 0 on its own, the expectation being that since the Iperf Command looks for the start of the anti-clockwise rotation anyway, this should suffice to make it work.

Observations
------------

* A telnet error for the synaxxx caused it to crash (the hostname was unknown) but the errors from the threaded ssh-connections trying to teardown already torn-down connections hid the error (scrolled off the screen)

* The Oscillator got a `Rate table returned invalid amount of data` message and the command failed, but didn't raise an error so the rest of the test continued, even though the turn-table wasn't turning.

* It needs to make sure that the next oscillate command isn't called while it is still resetting or it will not be correct.

Proposed Fixes
--------------

* Change the Oscillator to retry multiple times 
* raise an error if unsuccessful

Conclusion
----------

The use of the oscillate stop would work if the table were more robust and there were a way to make sure that the start of the next oscillation comes after it has fully reset.

Experiment 2
------------

Add a sleep tool to the Test-Teardown so that it always gives the table enough time to reset.

Observations
------------

* This works but is reallly messy

* But it also allows the inclusion of sleeps for other cases, and leaves the code more or less correct for the case where the rate-table is fully functional.

