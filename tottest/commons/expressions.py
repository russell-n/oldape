import string

NAMED = r"(?P<{name}>{pattern})"
GROUP = r"({group})"
CLASS = "[{0}]"
OR = "|"

SPACE = r'\s'
DIGIT = r"\d"
ANYTHING = '.'


# counts
M_TO_N_TIMES = "{{{m},{n}}}"
ONE_TO_3 = M_TO_N_TIMES.format(m=1, n=3)
EXACTLY = "{{{0}}}"
ONE_OR_MORE = "+"
ZERO_OR_MORE = '*'

EVERYTHING = ANYTHING + ZERO_OR_MORE

# special characters 
SPACES = SPACE + ONE_OR_MORE
DOT = r"\."


# numbers
HEX = CLASS.format(string.hexdigits)
INTEGER = DIGIT + ONE_OR_MORE
REAL = INTEGER + GROUP.format(group= DOT + INTEGER) + ZERO_OR_MORE

# Addresses
OCTET = DIGIT + ONE_TO_3
OCTET_DOT = OCTET + DOT

IP_ADDRESS_NAME = "ip_address"
IP_ADDRESS = NAMED.format(name=IP_ADDRESS_NAME,
                       pattern=DOT.join([OCTET] * 4))

MAC_ADDRESS_NAME = "mac_address"
HEX_PAIR = HEX + EXACTLY.format(2)
MAC_ADDRESS = NAMED.format(name=MAC_ADDRESS_NAME,
                           pattern=":".join([HEX_PAIR] * 6))

LINUX_IP = SPACES.join('inet addr:'.split()) + IP_ADDRESS
LINUX_MAC = "HWaddr" + SPACES + MAC_ADDRESS
ANDROID_IP = 'ip' + SPACES + IP_ADDRESS

NETCFG_IP = SPACES + GROUP.format(group= "UP" + OR + "DOWN") + SPACES + IP_ADDRESS + EVERYTHING + MAC_ADDRESS

#ping expressions
RTT = NAMED.format(name="rtt", pattern=REAL)

PING = SPACES.join([INTEGER, "bytes", "from", IP_ADDRESS + ":",
                    "icmp_[rs]eq=" + INTEGER,
                        "ttl=" + INTEGER,
                        "time=" + RTT])


