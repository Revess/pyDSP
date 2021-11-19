from ..oscillator.waveforms import *

class Synth:
    def __init__(self,sampleRate=44100,frequency=220,voices=1,angle=0.5,volume=0.5,detune=0.5,fm=0,am=0,rm=0,modulator=dict()) -> None:
        self.samplerate=sampleRate
        self.frequency=frequency
        self.angle=angle
        self.volume=volume
        self.voices = [Sine(self.frequency,self.samplerate) for i in range(voices)]
        self.detune = detune
        self.maxDetuneRatio = 20
        self.waveform = "sine"
        self.fm = fm
        self.am = am
        self.rm = rm
        self.modulators = modulator
        self.setFrequency(self.frequency)

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
        self.setFrequency(self.frequency)

    def addInput(self,unitID,item):
        self.modulators.update({unitID:[[""],item]})

    def modifyModulator(self,unitID,property,value):
        self.modulators[unitID][1].changeProperty(property,value)

    def removeInput(self,unitID):
        del self.modulators[unitID]

    def getModulatorValue(self,unitID):
        return self.modulators[unitID][1]

    def getModulators(self):
        return self.modulators

    def removeVoice(self):
        self.voices.pop()
        self.setFrequency(self.frequency)

    def setFrequency(self,frequency):
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
        self.setFrequency(self.frequency)

    def setFM(self,fm):
        self.fm = fm

    def setAM(self,am):
        self.am = am

    def setRM(self,rm):
        self.rm = rm

    def setFMInput(self,unitID):
        self.modulators[unitID][0] = "FM"
    
    def setAMInput(self,unitID):
        self.modulators[unitID][0] = "AM"

    def setRMInput(self,unitID):
        self.modulators[unitID][0] = "RM"

    def getFrequency(self):
        return self.frequency

    def getVolume(self):
        return self.volume

    def getAngle(self):
        return self.angle

    def changeProperty(self,property,value):
        print(property,value)
        if "frequency" in property:
            self.setFrequency(float(value))
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
        elif "Fm" in property:
            self.setFM(float(value))
        elif "Am" in property:
            self.setAM(float(value))
        elif "Rm" in property:
            self.setRM(float(value))
        elif "FMInput" in property:
            self.setFMInput(value)
        elif "AMInput" in property:
            self.setAMInput(value)
        elif "RMInput" in property:
            self.setRMInput(value)
