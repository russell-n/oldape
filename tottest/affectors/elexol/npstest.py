import nps
import time

ps = nps.nps('192.168.20.68', clear = False)
"""
ps.GetPortStatus()
print ps.OnCnt()
print ps.port_status
for i in xrange(24):
    if i % 8 == 0:
        ps.AllOff()
    ps.TurnOn(i)
    time.sleep(1)

ps.AllOff()
"""
ps.TurnOnList([11, 18, 23, 22, 21, 20, 19])
time.sleep(1)
#ps.TurnOffList([11, 18, 23, 22, 21, 20, 19])
ps.AllOff(exception=[18, 23])
port, pin = ps.ToPortPin(12)
status = ps.port_status[port][pin]
print status


