from math import fmod

class PitchShifter:
    def __init__(self,speed=0.5) -> None:
        self.speed = 1/(1-speed)
        self.delayLength = 1
        while round(fmod(self.delayLength,self.speed),2) != 0.0:
            self.delayLength+=1
            if self.delayLength >= 20 and round(fmod(self.delayLength,self.speed),2) < 0.5:
                break

        print(self.delayLength)
        self.delayLength*=2

        self.delayLine = [0] * self.delayLength
        self.writeHead = 0
        self.readHead = 0

    def readSample(self):
        sample = self.delayLine[self.readHead]
        self.readHead+=1
        self.readHead%=self.delayLength
        return sample


    def writeSample(self,sample):
        for i in range(int(self.delayLength/2)):
            self.delayLine[(self.writeHead+i)%self.delayLength] = (sample * (((self.delayLength-1)-i)/(self.delayLength-1)))+self.delayLine[(self.writeHead+i)%self.delayLength]
            self.delayLine[(self.writeHead+i)%self.delayLength] = self.delayLine[(self.writeHead+i)%self.delayLength]/2
        self.writeHead+=1
        self.writeHead%=self.delayLength