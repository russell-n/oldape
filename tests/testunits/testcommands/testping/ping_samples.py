NEWLINE = '\n'


# linux samples
ping_linux = """
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_req=1 ttl=64 time=0.196 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.196/0.196/0.196/0.000 ms

""".split(NEWLINE)

ping_linux_rtt = "0.196"

ping_linux_2="""
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_req=1 ttl=64 time=0.348 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.348/0.348/0.348/0.000 ms

""".split(NEWLINE)

ping_linux_2_rtt = "0.348"

ping_linux_3 = """
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_req=1 ttl=64 time=0.398 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.398/0.398/0.398/0.000 ms
""".split(NEWLINE)

ping_linux_3_rtt = "0.398"

# linux failure
ping_fail_linux = """
PING 192.168.20.254 (192.168.20.254) 56(84) bytes of data.

--- 192.168.20.254 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 999ms

""".split(NEWLINE)

# android samples
ping_android ="""
PING 192.168.20.24 (192.168.20.24) 56(84) bytes of data.
64 bytes from 192.168.20.24: icmp_seq=1 ttl=64 time=98.4 ms

--- 192.168.20.24 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 98.450/98.450/98.450/0.000 ms

""".split(NEWLINE)

ping_android_rtt = "98.4"


ping_fail_android = """
PING 192.168.20.254 (192.168.20.254) 56(84) bytes of data.

--- 192.168.20.254 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
"""
