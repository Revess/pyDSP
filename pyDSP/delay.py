from .audioUnit import *

class DelayLine(AudioUnit):
    def __init__(self,samplerate,feedback,lengthInSamples=None,lengthInMS=None) -> None:
        super().__init__(samplerate)
        self.delayLine = [0] * (samplerate*5)
        assert((lengthInMS is not None and lengthInSamples is None) or(lengthInMS is None and lengthInSamples is not None))
        if lengthInMS is not None:
            self.delayLength = round((samplerate/1000)*(lengthInMS+1))
        else:
            self.delayLength = lengthInSamples
        self.readHead = 0
        self.writeHead = len(self.delayLine)-1
        self.feedback = feedback

    def readSample(self):
        sample = self.delayLine[self.readHead]
        self.readHead+=1
        self.readHead%=self.delayLength
        return sample

    def writeSample(self,sample):
        self.delayLine[self.writeHead] = sample + (self.delayLine[self.writeHead]*self.feedback)
        self.writeHead+=1
        self.writeHead%=self.delayLength

    def setLength(self,samples):
        self.delayLength = samples

    def setLengthMS(self,ms):
        self.delayLength = round((self.samplerate/1000)*(ms+1))