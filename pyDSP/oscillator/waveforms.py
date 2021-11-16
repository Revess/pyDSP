from math import sin
from oscillator import Oscillator

class Saw(Oscillator):
    def __init__(self,frequency,sampleRate) -> None:
        super().__init__(frequency,sampleRate)

    def calculate(self):
        return (self.phase*2)-1

class Square(Oscillator):
    def __init__(self,frequency,sampleRate,angle) -> None:
        super().__init__(frequency,sampleRate)
        self.angle = angle
        if self.angle >= 1:
            self.angle -=0.00001
        elif self.angle <= 0:
            self.angle +=0.00001

    def calculate(self):
        sample = 0
        if self.phase > self.angle:
            sample = 1
        else:
            sample = -1

        return sample

class Triangle(Oscillator):
    def __init__(self,frequency,sampleRate,angle) -> None:
        super().__init__(frequency,sampleRate)
        self.angle = angle
        if self.angle >= 1:
            self.angle -=0.00001
        elif self.angle <= 0:
            self.angle +=0.00001
        self.invAngle = 1-self.angle

    def calculate(self):
        sample = 0
        if self.phase > self.angle:
            sample = ((self.invAngle-(self.phase-self.angle))/self.invAngle)*self.angle
        else:
            sample = self.phase

        return ((sample/self.angle)*2)-1

class Sine(Oscillator):
    def __init__(self,frequency,sampleRate) -> None:
        super().__init__(frequency,sampleRate)

    def calculate(self):
        return sin(self.phase*self.TWO_PI)
