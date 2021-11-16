from math import sin
from oscillator import Oscillator

class Saw(Oscillator):
    def __init__(self,frequency,sampleRate) -> None:
        super().__init__(frequency,sampleRate)

    def calculate(self):
        return ((self.phase)*2)-1