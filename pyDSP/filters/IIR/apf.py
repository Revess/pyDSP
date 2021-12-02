from ...audioUnit import AudioUnit

class APF(AudioUnit):
    def __init__(self,samplerate,gain=0.9,m=1) -> None:
        super().__init__(samplerate)
        self.g = gain
        self.Z1 = [0]*m
        self.readHeader = 0
        self.writeHeader = len(self.Z1)-1

    def readSample(self,sample):
        delayedSample = self.Z1[self.readHeader]
        self.readHeader+=1
        self.readHeader%=len(self.Z1)

        self.Z1[self.writeHeader] = sample+(delayedSample*-self.g)
        output = (self.Z1[self.writeHeader]*self.g)+delayedSample

        self.writeHeader+=1
        self.writeHeader%=len(self.Z1)
        return output
