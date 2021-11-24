from .biPass import *
from .highPass import *
from .lowPass import *
from ...audioUnit import *

class MultiFilter(AudioUnit):
    def __init__(self, filterDesign = "LPF", cutoff=500, cutoffH=880, samplerate=44100, nTaps=None):
        super().__init__(samplerate)
        self.type = filterDesign
        self.LP = LowPass(cutoff, samplerate, nTaps)
        self.HP = HighPass(cutoff, samplerate, nTaps)
        self.BP = BiPass(cutoff, cutoffH, samplerate, nTaps)

    def get_sample(self, sample):
        if self.type == "LPF":
            return self.LP.get_sample(sample)
        elif self.type == "HPF":
            return self.HP.get_sample(sample)
        elif self.type == "BPF":
            return self.BP.get_sample(sample)

    def setCutoff(self,cutoff,cutoffH=440):
        self.LP.setCutoff(cutoff)
        self.HP.setCutoff(cutoff)
        self.BP.setCutoff(cutoff,cutoffH)

    def setSamplerate(self, samplerate):
        self.LP.setSamplerate(samplerate)
        self.HP.setSamplerate(samplerate)
        self.BP.setSamplerate(samplerate)
        
    def setFilterType(self,filter):
        self.type = filter
        
    def setNTaps(self,taps):
        self.LP.setNTaps(taps)
        self.HP.setNTaps(taps)
        self.BP.setNTaps(taps)
        