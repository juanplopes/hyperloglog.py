from mmhash import mmhash
from math import log
from zlib import compress
from base64 import b64encode

class HyperLogLog:
    def __init__(self, log2m):
        self.log2m = log2m
        self.m = 1 << log2m
        self.data = [0]*self.m
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m)) * self.m * self.m
        
    def offer(self, o):
        x = mmhash(str(o), 0)

        a, b = 32-self.log2m, self.log2m

        i = x >> a
        v = self._bitscan(x << b, a)
        
        self.data[i] = max(self.data[i], v)
        
    def count(self):
        estimate = self.alphaMM / sum([2**-v for v in self.data])
        if estimate <= 2.5 * self.m:
            zeros = float(self.data.count(0))
            return round(-self.m * log(zeros / self.m))
        else:
            return round(estimate)
        
    def _bitscan(self, x, m):
        v = 1
        while v<=m and not x&0x80000000:
            v+=1
            x<<=1
        return v
        
    def datastr(self):
        return b64encode(compress(str.join('', map(chr, self.data)), 9))

