import re

NAMED = r"(?P<{name}>{pattern})"
CLASS = "[{0}]"
OR = "|"
DIGIT = r"\d"
DOT = r"\."
ONE_TO_3 = "{1,3}"
EXACTLY = "{{{0}}}"
OCTET = DIGIT + ONE_TO_3
OCTET_DOT = OCTET + DOT
ADDRESS = OCTET_DOT + OCTET_DOT + OCTET_DOT + OCTET

IP_ADDRESS = re.compile(ADDRESS)
