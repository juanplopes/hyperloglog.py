import unittest
from hyperloglog import HyperLogLog
from random import randint

class TestHyperLogLog(unittest.TestCase):
    def test_mid_range_with_strings(self):
        self.execute(10000, 10, 0.05)

    def test_long_range_with_strings(self):
        self.execute(100000, 10, 0.05)

    def test_low_range_with_strings(self):
        self.execute(100, 10, 0.05)


    def execute(self, set_size, m, p):
        print 't', set_size, m, p

        hll = HyperLogLog(m)
        for i in range(set_size):
            hll.offer(str(i))

        estimate = hll.count()
        error = abs(estimate/float(set_size) - 1)
        
        strdata = hll.datastr()
        print 'e', estimate, error, 1<<m, len(strdata)
        self.assertLess(len(hll.datastr()), 1<<m)
        self.assertLess(error, p)
        
    
if __name__ == "__main__":
    unittest.main()
