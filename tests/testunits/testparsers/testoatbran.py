from unittest import TestCase
import re

from apetools.parsers import oatbran

bran = oatbran
COW = 'cow'

class TestOatBran(TestCase):
    def test_brackets(self):
        L_BRACKET = '['
        R_BRACKET = "]"
        self.assertRegexpMatches(L_BRACKET, bran.L_BRACKET)
        self.assertNotRegexpMatches(R_BRACKET, bran.L_BRACKET)
        self.assertRegexpMatches(R_BRACKET, bran.R_BRACKET)
        self.assertNotRegexpMatches(L_BRACKET, bran.R_BRACKET)
        return

    def test_spaces(self):
        space = ' '
        empty_string = ''
        spaces = '    '
        self.assertRegexpMatches(space, bran.SPACE)
        self.assertNotRegexpMatches(empty_string, bran.SPACE)
        self.assertNotRegexpMatches(COW, bran.SPACE)
        self.assertRegexpMatches(spaces, bran.SPACE)
        self.assertRegexpMatches(spaces, bran.SPACES)
        self.assertNotRegexpMatches(empty_string, bran.SPACES)
        self.assertNotRegexpMatches(COW, bran.SPACES)                                    
        self.assertRegexpMatches(spaces, bran.OPTIONAL_SPACES)
        self.assertRegexpMatches(empty_string, bran.OPTIONAL_SPACES)
        self.assertRegexpMatches(COW, bran.OPTIONAL_SPACES)
        return

    def test_named(self):
        name = "boy"
        expression = COW
        match = re.search(bran.NAMED(n=name, e=expression), "a cow for liebowitz")
        self.assertEqual(expression, match.group(name))
        return

    def test_digit(self):
        digits = "1 2 3 4 5 6 7 8 9 0".split()
        for digit in digits:
            self.assertRegexpMatches(digit, bran.DIGIT)
        self.assertNotRegexpMatches(COW, bran.DIGIT)
        return

    def test_integer(self):
        n1 = "112345"
        n2 = "0.1"
        self.assertRegexpMatches(n1, bran.INTEGER)
        match = re.search(bran.GROUP(e=bran.INTEGER), n2)
        self.assertIsNone(match)
        return

    def test_float(self):
        n1 = '12.3'
        n2 = "11"
        self.assertRegexpMatches(n1, bran.FLOAT)
        self.assertNotRegexpMatches(n2, bran.FLOAT)
        return

    def test_real(self):
        n1 = "0.340"
        n2 = "123"
        match = re.search(bran.GROUP(e=bran.REAL), n1)
        self.assertEqual(n1, match.groups()[0])
        self.assertRegexpMatches(n2, bran.REAL)
        self.assertNotRegexpMatches(COW, bran.REAL)
        return

    def test_class(self):
        s = "Bboy"
        e = bran.CLASS(e="Bb") + "boy"
        self. assertRegexpMatches(s, e)

    def test_single_digit(self):
        self.assertRegexpMatches("0", bran.SINGLE_DIGIT)
        return
    
    def test_two_digits(self):
        self.assertRegexpMatches("19", bran.TWO_DIGITS)
        self.assertRegexpMatches("99", bran.TWO_DIGITS)
        self.assertNotRegexpMatches("9", bran.TWO_DIGITS)
        self.assertNotRegexpMatches("100", bran.TWO_DIGITS)
        return
                  
    def test_zero_or_one(self):
        s = "Gb"
        s2 = "Gab"
        s3 = "Gaab"
        e = "G(a)" + bran.ZERO_OR_ONE + 'b'
        self.assertRegexpMatches(s, e)
        match = re.search(e, s)
        self.assertIsNone(match.groups()[0])

        self.assertRegexpMatches(s2, e)
        match = re.search(e, s2)
        self.assertEqual("a", match.groups()[0])
        self.assertNotRegexpMatches(s3, e)
        return

    def test_range(self):
        s = "1"
        s3 = "315"
        s2 = "a" + s3 + "21"
        e = bran.NAMED(n="octet", e=bran.M_TO_N(m=1, n=3, e=bran.DIGIT))
        self.assertRegexpMatches(s, e)
        self.assertRegexpMatches(s2, e)
        self.assertRegexpMatches(s3,e)
        match = re.search(e, s2)
        self.assertEqual(s3, match.group("octet"))
        return

    def test_absolute_range(self):
        s = "a123"
        e = bran.NAMED(n="octet", e=bran.M_TO_N_ONLY(m=1, n=3, e=bran.DIGIT))
        self.assertNotRegexpMatches(s, e)
        return
    
    def test_octet(self):
        name = "octet"
        e = re.compile(bran.NAMED(name,bran.OCTET))
        sources = (str(i) for i in range(256))
        for source in sources:
            match = e.search(source)
            self.assertEqual(source, match.group(name))
        s = "256"
        self.assertNotRegexpMatches(s, bran.OCTET)
        return

    def test_ip_address(self):
        s = "0.0.0.0"
        self.assertRegexpMatches(s, bran.IP_ADDRESS)
        self.assertNotRegexpMatches("256.255.255.255", bran.IP_ADDRESS)
        return

    def test_not(self):
        source = ",,323.5,"
        match = re.search(bran.NAMED('not',bran.NOT(",")), source)
        self.assertEqual(match.group('not'), '323.5')
        self.assertRegexpMatches(",,3,", bran.NOT(","))
        self.assertNotRegexpMatches(",,,,,", bran.NOT(','))
# end class TestOatBran
