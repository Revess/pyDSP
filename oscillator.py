from math import pi

class Oscillator:
    def __init__(self,frequency,sampleRate) -> None:
        self.TWO_PI = 2*pi
        self.phase = 0
        self.frequency = frequency
        self.sampleRate = sampleRate
        self.step = self.frequency/self.sampleRate

    def get_sample(self):
        self.phase+=self.step
        if self.phase >= 1:
            self.phase-=1
        return self.calculate()

    def setFrequecy(self,frequency):
        self.frequency = frequency

    def calculate(self):
        pass