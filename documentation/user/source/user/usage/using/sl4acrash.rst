ERROR: [2012-05-24 16:28:52,111] -- The program has crashed. I weep for you.
ERROR: [2012-05-24 16:28:52,112] -- [Errno 104] Connection reset by peer
******************** Crash Report ********************
Traceback (most recent call last):
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/infrastructure/strategerizer.py", line 78, in test
    test.run()
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/tools/testsl4a.py", line 49, in run
    info = self.sl4a_device.get_wifi_info().replace(',', '\n')
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/devices/sl4adevice.py", line 61, in get_wifi_info
    self.connection.wifiGetConnectionInfo().items()))
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/connections/sl4aconnection.py", line 39, in rpc_call
    result = self._rpc(method, *args)
  File "/home/allionadmin/current/repository_code/hortators/timetorecovertesttop/timetorecovertest/timetorecovertest/connections/android.py", line 46, in _rpc
    response = self.client.readline()
  File "/usr/lib/python2.7/socket.py", line 447, in readline
    data = self._sock.recv(self._rbufsize)
error: [Errno 104] Connection reset by peer
******************************************************
