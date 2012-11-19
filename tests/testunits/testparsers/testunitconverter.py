from unittest import TestCase

from tottest.parsers.unitconverter import UnitConverter
from tottest.parsers.unitconverter import UnitNames

bits = UnitNames.bits
kbits = UnitNames.kbits
mbits = UnitNames.mbits
gbits = UnitNames.gbits
Bytes = UnitNames.bytes
kbytes = UnitNames.kbytes
mbytes = UnitNames.mbytes
gbytes = UnitNames.gbytes

units = [bits, kbits, mbits, gbits, Bytes, kbytes, mbytes, gbytes]

converter = UnitConverter()

class TestUnitConverter(TestCase):
    def assert_almost(self, source, values):
        self.assertEqual(1, converter[source][source])
        dests = [unit for unit in units if unit != source]
        
        for index, dest in enumerate(dests):
            self.assertAlmostEqual(values[index], converter[source][dest])
        return
    
    def test_from_bits(self):
        values = [0.001, 0.000001, 0.0000000001, 0.125, 0.000125, 0.000000125,0.0000000000125]
        self.assert_almost(bits, values)
        return

    def test_from_kbits(self):
        values = [1000, 0.001, 0.000001, 125, 0.125, 0.000125, 0.000000125] 
        self.assert_almost(kbits, values)
        return

    def test_from_mbits(self):
        values = [10**6, 10**3, 0.001,
                  125000, 125, 0.125, 0.000125] 
        self.assert_almost(mbits, values)
        return

    def test_from_gbits(self):
        values = [10**9, 10**6, 10**3,
                  125000000, 125000, 125, 0.125, ]
        self.assert_almost(gbits, values)
        return
    

    def test_from_bytes(self):
        values = [8, 8/1000., 0.000008, 0.000000008,
                  0.001, 0.000001, 0.000000001]
        self.assert_almost(Bytes, values)
        return

    def test_from_kbytes(self):
        values = [8000, 8, .008, 0.000008,
                  1000, 0.001, 0.000001] 
        self.assert_almost(kbytes, values)
        return

    def test_from_mbytes(self):
        values = [8000000, 8000, 8, 0.008,
                  1000000, 1000, 0.001]
        self.assert_almost(mbytes, values)
        return

    def test_from_gbytes(self):
        values = [8000000000, 8000000, 8000, 8,
                  1000000000, 1000000, 1000]
        self.assert_almost(gbytes, values)
    
