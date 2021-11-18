from .waveforms import *

class Synth:
    def __init__(self,sampleRate=44100,frequency=220,voices=1,angle=0.5,volume=0.5,detune = 0.5) -> None:
        self.samplerate=sampleRate
        self.frequency=frequency
        self.angle=angle
        self.volume=volume
        self.voices = [Sine(self.frequency,self.samplerate) for i in range(voices)]
        self.detune = detune
        self.maxDetuneRatio = 20
        self.waveform = "sine"
        self.setFrequecny(self.frequency)

    def get_sample(self):
        sample = 0
        for voice in self.voices:
            sample += voice.get_sample()*(1/len(self.voices))
        return sample*self.volume

    def addVoice(self):
        if "saw" in self.waveform:
            self.voices.append(Saw(self.frequency,self.samplerate,self.angle))
        elif "triangle" in self.waveform:
            self.voices.append(Triangle(self.frequency,self.samplerate,self.angle))
        elif "square" in self.waveform:
            self.voices.append(Square(self.frequency,self.samplerate,self.angle))
        elif "sine" in self.waveform:
            self.voices.append(Sine(self.frequency,self.samplerate,self.angle))
        self.setFrequecny(self.frequency)

    def removeVoice(self):
        self.voices.pop()
        self.setFrequecny(self.frequency)

    def setFrequecny(self,frequency):
        self.frequency = frequency
        minimum = self.frequency-(self.detune*self.maxDetuneRatio)
        maximum = self.frequency+(self.detune*self.maxDetuneRatio)
        numVoices = len(self.voices)
        if numVoices > 1:
            for index,voice in enumerate(self.voices):
                freq = minimum+(((maximum-minimum)/(numVoices-1))*index)
                voice.setFrequecy(freq)
        else:
            self.voices[0].setFrequecy(self.frequency)

    def setVolume(self,volume):
        self.volume = volume

    def setAngle(self,angle):
        self.angle = angle
        if self.angle >= 1:
            self.angle -=0.00001
        elif self.angle <= 0:
            self.angle +=0.00001
        for voice in self.voices:
            voice.setAngle(self.angle)

    def setWaveForm(self,waveform):
        self.waveform = waveform
        if "saw" in self.waveform:
            for index,voice in enumerate(self.voices):
                self.voices[index] = Saw(voice.getFrequency(),self.samplerate,voice.getAngle(),voice.getVolume())
        elif "triangle" in self.waveform:
            for index,voice in enumerate(self.voices):
                self.voices[index] = Triangle(voice.getFrequency(),self.samplerate,voice.getAngle(),voice.getVolume())
        elif "square" in self.waveform:
            for index,voice in enumerate(self.voices):
                self.voices[index] = Square(voice.getFrequency(),self.samplerate,voice.getAngle(),voice.getVolume())
        elif "sine" in self.waveform:
            for index,voice in enumerate(self.voices):
                self.voices[index] = Sine(voice.getFrequency(),self.samplerate,voice.getAngle(),voice.getVolume())

    def setDetune(self,detune):
        self.detune = detune
        self.setFrequecny(self.frequency)


    def getFrequency(self):
        return self.frequency

    def getVolume(self):
        return self.volume

    def getAngle(self):
        return self.angle


    def changeProperty(self,property,value):
        if "frequency" in property:
            self.setFrequecny(float(value))
        elif "volume" in property:
            self.setVolume(float(value))
        elif "angle" in property:
            self.setAngle(float(value))
        elif "waveform" in property:
            self.setWaveForm(value)
        elif "detune" in property:
            self.setDetune(float(value))
        elif "voices" in property:
            if len(self.voices) < float(value):
                for i in range(int(float(value)-len(self.voices))):
                    self.addVoice()
            elif len(self.voices) > float(value):
                for i in range(int(len(self.voices)-float(value))):
                    self.removeVoice()
