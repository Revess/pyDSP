class DelayLine:
    def __init__(self,samplerate,feedback,length) -> None:
        self.delayLine = [0] * (samplerate*5)
        self.delayLength = length
        self.readHead = 0
        self.writeHead = len(self.delayLine)-1
        self.feedback = feedback
        self.samplerate = samplerate

    def readSample(self):
        sample = self.delayLine[self.readHead]
        self.readHead+=1
        self.readHead%=self.delayLength
        return sample

    def writeSample(self,sample):
        self.delayLine[self.writeHead] = sample #(self.delayLine[self.writeHead]*self.feedback)
        self.writeHead+=1
        self.writeHead%=self.delayLength

    def setLength(self,samples):
        self.delayLength = samples

    def setLengthMS(self,ms):
        self.delayLength = round((self.samplerate/1000)*(ms+1))
