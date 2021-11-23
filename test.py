from math import pi
class AudioUnit:
    def __init__(self,samplerate):
        self.samplerate = samplerate

    def get_sample(self):
        return 0

    def changeSamplerate(self,samplerate):
        print("pleh")
        self.samplerate = samplerate


class lowPass(AudioUnit):
    def __init__(self,cutoff,samplerate):
        super().__init__(samplerate)
        self.dt = 1/self.samplerate
        self.alpha = self.dt/((1/(cutoff*2*pi))+self.dt)

    def setCutoff(self,cutoff):
        self.alpha = self.dt/((1/(cutoff*2*pi))+self.dt)

    def changeSamplerate(self, samplerate):
        super().changeSamplerate(samplerate)
        self.dt = 1/self.samplerate


LP = lowPass(440,44100)

LP.changeSamplerate(10)