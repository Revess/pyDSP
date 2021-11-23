from math import pi
from ..audioUnit import AudioUnit

class LowPass(AudioUnit):
    def __init__(self,cutoff,samplerate,nSamples=1000):
        super().__init__(samplerate)
        self.cutoff = cutoff
        self.dt = 1/self.samplerate
        self.rc = (1/(self.cutoff*2*pi))
        self.alpha = self.dt/(self.rc+self.dt)
        self.delayLine = [0] * nSamples
        self.nSamples = nSamples
        self.pointer = 0

    def get_sample(self, sample):
        self.delayLine[self.pointer] = self.delayLine[self.pointer-1] + (self.alpha*(sample - self.delayLine[self.pointer-1]))
        self.pointer+=1
        self.pointer%=self.nSamples
        return self.delayLine[self.pointer]

    def setCutoff(self,cutoff):
        self.cutoff = cutoff
        self.rc = (1/(self.cutoff*2*pi))
        self.alpha = self.dt/(self.rc+self.dt)

    def changeSamplerate(self, samplerate):
        super().changeSamplerate(samplerate)
        self.dt = 1/self.samplerate
        self.alpha = self.dt/(self.rc+self.dt)