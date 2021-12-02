from math import cos,pi
from .audioUnit import AudioUnit

class PitchShifter(AudioUnit):
    def __init__(self,ferquency=2,samplerate=44100,speed=0.5) -> None:
        super().__init__(samplerate)
        self.delayLine = [0] * (round(samplerate/10)+1)
        self.phase = 0
        self.step = ferquency/self.samplerate

        self.writeHead = round(samplerate/10)-1
        self.previousSample = 0

    def readSample(self):
        if self.phase >= 1:
            self.phase -= 1
        sample = 0

        delayLength = round((self.samplerate/10)*self.phase)
        if delayLength == 0:
            delayLength = 1
        sample += self.delayLine[delayLength]*cos(((self.phase-0.5)/2)*(pi*2))

        delayLength = round((self.samplerate/10)*((self.phase+0.5)%1))
        if delayLength == 0:
            delayLength = 1
        sample += self.delayLine[delayLength]*cos(((((self.phase+0.5)%1)-0.5)/2)*(pi*2))

        sample /= 2
        sample = self.previousSample-(0.5*(self.previousSample-sample))

        self.previousSample = sample
        self.phase += self.step
        return sample

    def writeSample(self,sample):
        self.delayLine[self.writeHead] = sample
        self.writeHead+=1
        self.writeHead%=round(self.samplerate/10)

    def changePitch(self,pitch):
        self.step = pitch/self.samplerate
