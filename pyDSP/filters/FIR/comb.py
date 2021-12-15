from ...delay import DelayLine

class FIRComb(DelayLine):
    def __init__(self,samplerate,feedback,lengthInSamples=None,lengthInMS=None) -> None:
        super().__init__(samplerate,feedback,lengthInSamples,lengthInMS)

    def writeSample(self,sample):
        self.delayLine[self.writeHead] = sample * self.feedback
        self.writeHead+=1
        self.writeHead%=self.delayLength