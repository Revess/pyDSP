from math import pi,sin
from .filter import Filter

class BiPass(Filter):
    def __init__(self, cutoff=100, cutoffH=880, samplerate=44100, nTaps=None):
        super().__init__(cutoff=cutoff, cutoffH=cutoffH, samplerate=samplerate, nTaps=nTaps)
        self.designBPF()

    def designBPF(self):
        sample = 0
        for i in range(self.nTaps):
            sample = i - (self.nTaps - 1) / 2
            if sample == 0:
                self.taps[i] =  (self.phi - self.lambdaC) / pi
            else:
                self.taps[i] = (sin(sample*self.phi) - sin(sample*self.lambdaC))/ (sample*pi)
    
    def setCutoff(self,cutoff,cutoffH):
        super().setCutoff(cutoff,cutoffH)
        self.designBPF()

    def setSamplerate(self, samplerate):
        super().setSamplerate(samplerate)
        self.designBPF()
        
    def setNTaps(self,taps):
        super().setNTaps(taps)
        self.designBPF()