Oat Bran
========

Oat Bran helps with regular expressions.

Names are uppercased to avoid keyword clashes.



Groups
------

.. module:: apetools.parsers.oatbran
.. autosummary:: 
   :toctree: api

   GROUP
   NAMED
   CLASS
   NOT
   NOT_FOLLOWED_BY
   NOT_PRECEDED_BY



Cardinality
-----------

::

    ONE_OR_MORE = "+"
    ZERO_OR_MORE = '*'
    ZERO_OR_ONE = "?"
    EXACTLY = "{{{0}}}"
    
    



.. autosummary::
   :toctree: api

   M_TO_N
   M_to_N_ONLY


    
Escapes
-------

::

    DECIMAL_POINT = r'\.'
    L_BRACKET = r"\["
    R_BRACKET = r"\]"
    
    



Operators
---------

::

    OR = "|"
    
    



.. autosummary::
   :toctree: api

   WORD_BOUNDARY
   STRING_BOUNDARY



String Help
-----------

::

    STRING_START = "^"
    STRING_END = "$"
    ALPHA_NUM = r"\w"
    ALPHA_NUMS = ALPHA_NUM + ONE_OR_MORE
    
    



Anything And Everything
-----------------------

::

    ANYTHING = r"."
    EVERYTHING = ANYTHING + ZERO_OR_MORE
    
    



Numbers
-------

::

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
    



Spaces
------

::

    SPACE = r"\s"
    SPACES = SPACE + ONE_OR_MORE
    NOT_SPACE = r'\S'
    NOT_SPACES = NOT_SPACE + ONE_OR_MORE
    OPTIONAL_SPACES = SPACE + ZERO_OR_MORE
    
    



Common Constants
----------------

::

    DASH = "-"
    LETTER = CLASS(e=string.ascii_letters)
    LETTERS = LETTER + ONE_OR_MORE
    OPTIONAL_LETTERS = LETTER + ZERO_OR_MORE
    
    



Networking
----------

::

    DOT = DECIMAL_POINT
    OCTET = GROUP(e=OR.join([SINGLE_DIGIT, TWO_DIGITS, ONE_HUNDREDS,
                             WORD_BOUNDARY("2[0-4][0-9]"), WORD_BOUNDARY("25[0-5]")]))
    
    IP_ADDRESS = DOT.join([OCTET] * 4)
    
    # from commons.expressions
    MAC_ADDRESS_NAME = "mac_address"
    HEX_PAIR = HEX + EXACTLY.format(2)
    MAC_ADDRESS = NAMED(n=MAC_ADDRESS_NAME,
                        e=":".join([HEX_PAIR] * 6))
    

