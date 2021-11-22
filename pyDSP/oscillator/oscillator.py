from math import pi
from random import random
import numpy as np

class Oscillator:
    def __init__(self,frequency,sampleRate,angle=0.5,volume=1,phase=None) -> None:
        self.TWO_PI = 2*pi
        if phase is not None:
            self.phase = phase
        else:
            self.phase = random()
        self.frequency = frequency
        self.sampleRate = sampleRate
        self.step = self.frequency/self.sampleRate
        self.volume = volume
        self.angle = angle
        if self.angle >= 1:
            self.angle -=0.00001
        elif self.angle <= 0:
            self.angle +=0.00001

    def get_sample(self):
        self.phase+=self.step
        if self.phase >= 1:
            self.phase-=1
        return self.calculate()*self.volume

    def calculate(self):
        return self.phase

    def setFrequecy(self,frequency):
        self.frequency = frequency
        self.step = self.frequency/self.sampleRate

    def setVolume(self,volume):
        self.volume = volume

    def getFrequency(self):
        return self.frequency

    def getVolume(self):
        return self.volume

    def setAngle(self,angle):
        self.angle = angle
        if self.angle >= 1:
            self.angle -=0.00001
        elif self.angle <= 0:
            self.angle +=0.00001

    def getAngle(self):
        return self.angle
