from math import pi
from ..audioUnit import AudioUnit

class LowPass(AudioUnit):
    def __init__(self, filterDesign = "LPF", cutoffl=440, cutoffH=880, samplerate=44100, nTaps=1000):
        super().__init__(samplerate)
        self.nTaps = nTaps
        self.taps = [0]*nTaps
        self.sr = [0]*nTaps
        self.cutoff = cutoffl
        self.cutoffH = cutoffH
        self.lambdaC = pi*self.cutoff / (self.samplerate/2)
        self.phi = pi*self.cutoffH / (self.samplerate/2)
        if filterDesign == "LPF":
            self.designLPF()
        elif filterDesign == "HPF":
            self.designHPF()
        elif filterDesign == "BPF":
            self.designBPF()

    def get_sample(self, sample):
        pass

    def setCutoff(self,cutoff):
        pass

    def changeSamplerate(self, samplerate):
        super().changeSamplerate(samplerate)
        pass

    def designLPF(self):
        pass

    def designHPF(self):
        pass

    def designBPF(self):
        pass