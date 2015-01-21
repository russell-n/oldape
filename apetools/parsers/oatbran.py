
# python standard library
import string


def GROUP(e):
    """
    puts the argument in a group

    :param:

     - `e`: a string regular expression

    :return: grouped regular expression (string)
    """
    return "({e})".format(e=e)


def NAMED(n, e):
    """
    Puts the expression in a named-group

    :param:

     - `n`: the name of the group
     - `e`: regular expression

    :return: named-group
    """
    return "(?P<{n}>{e})".format(n=n, e=e)


def CLASS(e):
    """
    puts e in a character class

    :param:

     - `e`: a regular expression

    :return: character class
    """
    return "[{e}]".format(e=e)


def NOT(e):
    """
    match only if none of the characters in e are there

    :param:

     - `e`: characters to not match
     
    :return: character class not to match
    """
    return "[^{e}]+".format(e=e)


def NOT_FOLLOWED_BY(e):
    """
    look-ahead group

    :param:

     - `e`: expression that can't follow preceding string
     
    :return: not-followed by look ahead group
    """
    return "(?!{e})".format(e=e)


def NOT_PRECEDED_BY(e):
    """
    look-behind group

    :param:

     - `e`: expression that can't precede what follows

    :return: negative look-behind group
    """
    return "(?<!{e})".format(e=e)


ONE_OR_MORE = "+"
ZERO_OR_MORE = '*'
ZERO_OR_ONE = "?"
EXACTLY = "{{{0}}}"


def M_TO_N(m, n, e):
    """
    match from m to n occurences of e

    :param:

     - `m`: the minimum required number of matches
     - `n`: the maximum number of  matches
     - `e`: the expression to match
    """
    return "{e}{{{m},{n}}}".format(m=m, n=n, e=e)


def M_TO_N_ONLY(m, n, e):
    """
    match from m to n occurences of e as an entire word
    (not a sub-string of a longer word)    

    :param:

     - `m`: the minimum required number of matches
     - `n`: the maximum number of  matches
     - `e`: the expression t match
    """
    return r"\b{e}{{{m},{n}}}\b".format(m=m, n=n, e=e)


DECIMAL_POINT = r'\.'
L_BRACKET = r"\["
R_BRACKET = r"\]"


OR = "|"


def WORD_BOUNDARY(e):
    """
    adds word-boundaries

    :param: 

     - `e`: expression to bound

    :return: expression than matches entire words
    """
    return r"\b{e}\b".format(e=e)


def STRING_BOUNDARY(e):
    """
    :return: expr that matches an entire line
    """
    return r"^{e}$".format(e=e)


STRING_START = "^"
STRING_END = "$"
ALPHA_NUM = r"\w"
ALPHA_NUMS = ALPHA_NUM + ONE_OR_MORE


ANYTHING = r"."
EVERYTHING = ANYTHING + ZERO_OR_MORE


DIGIT = r"\d"
NOT_DIGIT = r"\D"
NON_ZERO = CLASS("1-9")
SINGLE_DIGIT = WORD_BOUNDARY(DIGIT)
TWO_DIGITS = WORD_BOUNDARY(NON_ZERO + DIGIT)
ONE_HUNDREDS = WORD_BOUNDARY("1" + DIGIT + DIGIT)
NATURAL = DIGIT + ONE_OR_MORE

INTEGER = (NOT_PRECEDED_BY(DECIMAL_POINT) +  "-" + ZERO_OR_ONE + 
           NATURAL + NOT_FOLLOWED_BY(DECIMAL_POINT))

FLOAT = "-" + ZERO_OR_ONE + NATURAL + DECIMAL_POINT + NATURAL
REAL = GROUP(FLOAT + OR + INTEGER)
HEX = CLASS(string.hexdigits)
HEXADECIMALS = HEX + ONE_OR_MORE


SPACE = r"\s"
SPACES = SPACE + ONE_OR_MORE
NOT_SPACE = r'\S'
NOT_SPACES = NOT_SPACE + ONE_OR_MORE
OPTIONAL_SPACES = SPACE + ZERO_OR_MORE


DASH = "-"
LETTER = CLASS(e=string.ascii_letters)
LETTERS = LETTER + ONE_OR_MORE
OPTIONAL_LETTERS = LETTER + ZERO_OR_MORE


DOT = DECIMAL_POINT
OCTET = GROUP(e=OR.join([SINGLE_DIGIT, TWO_DIGITS, ONE_HUNDREDS,
                         WORD_BOUNDARY("2[0-4][0-9]"), WORD_BOUNDARY("25[0-5]")]))

IP_ADDRESS = DOT.join([OCTET] * 4)

# from commons.expressions
MAC_ADDRESS_NAME = "mac_address"
HEX_PAIR = HEX + EXACTLY.format(2)
MAC_ADDRESS = NAMED(n=MAC_ADDRESS_NAME,
                    e=":".join([HEX_PAIR] * 6))
