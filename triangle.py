from math import sin
from oscillator import Oscillator

class Triangle(Oscillator):
    def __init__(self,frequency,sampleRate,angle) -> None:
        super().__init__(frequency,sampleRate)
        self.angle = angle
        self.tristep = 1/((1/self.step)*angle)

    def get_sample(self):
        self.phase+=self.tristep
        if self.phase >= 1:
            self.tristep = -(1/(1/(self.step)*(1-self.angle)))
            if self.tristep == 0:
                self.phase -=1
            else:
                self.phase = 1
        elif self.phase <= 0:
            self.tristep = 1/((1/self.step)*self.angle)
        return (self.phase*2)-1