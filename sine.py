from math import sin,cos
from oscillator import Oscillator

class Sine(Oscillator):
    def __init__(self,frequency,sampleRate) -> None:
        super().__init__(frequency,sampleRate)

    def calculate(self):
        return cos(self.phase*self.TWO_PI)