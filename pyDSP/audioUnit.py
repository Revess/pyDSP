class AudioUnit:
    def __init__(self,samplerate):
        self.samplerate = samplerate

    def readSample(self):
        return 0

    def writeSample(self,sample):
        pass

    def setSamplerate(self,samplerate):
        self.samplerate = samplerate