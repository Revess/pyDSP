class AudioUnit:
    def __init__(self,samplerate):
        self.samplerate = samplerate

    def get_sample(self):
        return 0

    def changeSamplerate(self,samplerate):
        self.samplerate = samplerate