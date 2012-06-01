import string

NAMED = r"(?P<{name}>{pattern})"
GROUP = r"({group})"
CLASS = "[{0}]"
OR = "|"
NOT = "^"

SPACE = r'\s'
NOT_SPACE = r'\S'
DIGIT = r"\d"
ANYTHING = '.'
WORD_ENDING = r'\b'

# counts
M_TO_N_TIMES = "{{{m},{n}}}"
ONE_TO_3 = M_TO_N_TIMES.format(m=1, n=3)
EXACTLY = "{{{0}}}"
ONE_OR_MORE = "+"
ZERO_OR_MORE = '*'
ZERO_OR_ONE = '?'

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


# ps expressions
PSE_NAME = "pse"
PID_NAME = 'pid'
PID = NAMED.format(name=PID_NAME,  pattern=INTEGER)
TTY = GROUP.format(group="\?" + OR + "pts/" + INTEGER)
TIME = ":".join([DIGIT + EXACTLY.format(2)] * 3)
PROCESS_NAME = "process"
PROCESS = NAMED.format(name=PROCESS_NAME,pattern=CLASS.format(NOT + SPACE) + ONE_OR_MORE)
PSE_LINUX = SPACES.join([PID, TTY, TIME, PROCESS])
