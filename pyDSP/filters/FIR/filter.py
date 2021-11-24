from math import pi,log10
from ...audioUnit import AudioUnit

MAXTAPS = 25

class Filter(AudioUnit):
    def __init__(self, cutoff=100, cutoffH=880, samplerate=44100, nTaps=None):
        super().__init__(samplerate)
        if nTaps is None:
            self.nTaps = round(((2 / 3) * log10(10 ^ 9)) * (samplerate / (cutoff / 2)))
        else:
            self.nTaps = nTaps
        if self.nTaps > MAXTAPS:
            self.nTaps = MAXTAPS
        self.taps = [0]*self.nTaps
        self.samples = [0]*self.nTaps
        self.cutoff = cutoff
        self.cutoffH = cutoffH
        self.lambdaC = pi*self.cutoff / (self.samplerate/2)
        self.phi = pi*self.cutoffH / (self.samplerate/2)

    def get_sample(self, sample):
        self.samples.pop(0)
        self.samples = [sample] +  self.samples
        result=0
        for i in range(self.nTaps):
            result+=self.samples[i]*self.taps[i]
        return result

    def setCutoff(self,cutoff,cutoffH=440):
        self.cutoff = cutoff
        self.cutoffH = cutoffH
        self.setNTaps(round(((2.0 / 3.0) * log10(10 ^ 9)) * (self.samplerate / (self.cutoff / 2.0))))
        self.lambdaC = pi*self.cutoff / (self.samplerate/2)

    def setSamplerate(self, samplerate):
        super().changeSamplerate(samplerate)
        self.setNTaps(round(((2.0 / 3.0) * log10(10 ^ 9)) * (self.samplerate / (self.cutoff / 2.0))))
        self.lambdaC = pi*self.cutoff / (self.samplerate/2)
        self.phi = pi*self.cutoffH / (self.samplerate/2)

    def setNTaps(self,taps):
        if taps > MAXTAPS:
            taps = MAXTAPS
        if self.nTaps > taps:
            self.taps = self.taps[:self.nTaps]
            self.samples = self.samples[:self.nTaps]
        else:
            diff = taps-self.nTaps
            self.taps = self.taps + ([0]*diff)
            self.samples = self.samples + ([0]*diff)
        self.nTaps = taps