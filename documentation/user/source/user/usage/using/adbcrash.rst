ERROR: [2012-05-24 16:36:41,877] -- The program has crashed. I weep for you.
ERROR: [2012-05-24 16:36:41,877] -- Unable to create an SL4A connection: [Errno 111] Connection refused
******************** Crash Report ********************
Traceback (most recent call last):
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/infrastructure/strategerizer.py", line 78, in test
    test.run()
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/tools/testsl4a.py", line 49, in run
    info = self.sl4a_device.get_wifi_info().replace(',', '\n')
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/devices/sl4adevice.py", line 61, in get_wifi_info
    self.connection.wifiGetConnectionInfo().items()))
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/devices/sl4adevice.py", line 29, in connection
    self._connection = SL4AConnection()
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/connections/sl4aconnection.py", line 23, in __init__
    raise ConnectionError("Unable to create an SL4A connection: {0}".format(error))
ConnectionError: Unable to create an SL4A connection: [Errno 111] Connection refused
******************************************************
