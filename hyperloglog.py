from mmhash import mmhash
from math import log

class HyperLogLog:
    def __init__(self, log2m):
        self.log2m = log2m
        self.m = 1 << log2m
        self.data = [0]*self.m
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m)) * self.m * self.m
        
    def offer(self, o):
        x = mmhash(str(o), 0)
        i = x >> (32-self.log2m)
        v = self._bitscan((x << self.log2m) | ((1 << self.log2m)- 1))
        
        self.data[i] = max(self.data[i], v)
        
    def count(self):
        estimate = self.alphaMM * (1.0 / sum([2**-v for v in self.data]))
        if estimate <= 2.5 * self.m:
            z = float(self.data.count(0))
            return round(-self.m * log(z / self.m))
        else:
            return round(estimate)
        
    def _bitscan(self, x):
        if x==0: return 33
        v = 1
        while not x&0x80000000:
            v+=1
            x<<=1
        return v
