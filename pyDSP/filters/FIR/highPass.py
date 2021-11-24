from math import pi,sin
from .filter import Filter

class HighPass(Filter):
    def __init__(self, cutoff=100, samplerate=44100, nTaps=None):
        super().__init__(cutoff=cutoff, samplerate=samplerate, nTaps=nTaps)
        self.designHPF()

    def designHPF(self):
        sample = 0
        for i in range(self.nTaps):
            sample = i - (self.nTaps - 1) / 2
            if sample == 0:
                self.taps[i] = 1 - (self.lambdaC / pi)
            else:
                self.taps[i] = -sin(sample*self.lambdaC) / (sample*pi)
    
    def setCutoff(self,cutoff):
        super().setCutoff(cutoff)
        self.designHPF()

    def setSamplerate(self, samplerate):
        super().setSamplerate(samplerate)
        self.designHPF()
        
    def setNTaps(self,taps):
        super().setNTaps(taps)
        self.designHPF()
        