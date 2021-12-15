from ..filters.IIR.apf import *
from ..filters.FIR.comb import *
from ..audioUnit import *

class SchoederVerb(AudioUnit):
    def __init__(self,samplerate) -> None:
        super().__init__(samplerate)
        self.apf = [
            APF(samplerate,0.7,1051),
            APF(samplerate,0.7,337),
            APF(samplerate,0.7,113)
        ]
        self.combs = [
            FIRComb(samplerate,0.742,4799),
            FIRComb(samplerate,0.733,4999),
            FIRComb(samplerate,0.715,5399),
            FIRComb(samplerate,0.697,5801)
            ]

    def readSample(self,sample):
        for apf in self.apf:
            sample = apf.readSample(sample)
        output = 0
        for comb in self.combs:
            comb.writeSample(sample)
            output += comb.readSample()
        return sample