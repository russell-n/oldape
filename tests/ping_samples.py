NEWLINE = '\n'

ping_linux = """
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_req=1 ttl=64 time=0.196 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.196/0.196/0.196/0.000 ms

""".split(NEWLINE)

ping_android ="""
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_seq=1 ttl=64 time=98.4 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 98.450/98.450/98.450/0.000 ms

""".split(NEWLINE)

ping_fail_linux = """
PING 192.168.20.254 (192.168.20.254) 56(84) bytes of data.

--- 192.168.20.254 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 999ms

""".split(NEWLINE)

ping_fail_android = """
PING 192.168.20.254 (192.168.20.254) 56(84) bytes of data.

--- 192.168.20.254 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
"""
