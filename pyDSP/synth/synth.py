from ..waves.waveforms import *
from ..audioUnit import *

class Synth:
    def __init__(self,samplerate,voices):
        super().__init__(samplerate)
        self.noteManager = NoteManager(voices)
        self.voices = voices
        self.oscillatorModules = [OscillatorModule()]
           
    def readSample(self):
        output = 0
        for oscillator in self.oscillators:
            output += oscillator.readSample()/len(self.oscillators)

    def noteOn(self,note,velocity):
        self.noteManager.noteOn(note,velocity)
        frequency = self.noteManager.getNote(note)


    def noteOff(self,note):
        self.noteManager.noteOff(note)

class NoteManager:
    def __init__(self,voices):
        self.voices = voices
        self.notes = dict()
        self.openNote = 0

    def noteOn(self,note,velocity):
        if len(self.notes) < self.voices:
            self.notes.update({note:velocity})
    
    def noteOff(self,note):
        del self.notes[note]

    def getNote(self,note):
        return 2**((self.notes[note]-69)/12)*440

    def getNotes(self):
        return [2**((note-69)/12)*440 for note in self.notes.keys()]

class OscillatorModule(AudioUnit):
    def __init__(self,samplerate,voices,detune, frequency, waveform="Sine"):
        super().__init__(samplerate)
        self.maxDetuneRatio = 20
        self.detune = detune*self.maxDetuneRatio
        self.waveform = waveform
        self.frequency = frequency
        self.voices = [None]*voices
        self.setWaveForm(waveform)
        self.voices = [Sine(frequency, samplerate) for i in range(voices)]

    def setFrequency(self,frequency=None):
        if frequency is not None:
            self.frequency = frequency
        if len(self.voices) > 1:
            [voice.setFrequecy((self.frequency-self.detune)+(((self.detune*2)/(len(self.voices)-1))*index)) for index, voice in enumerate(self.voices)]
        else:
            self.voices[0].setFrequecy(self.frequency)

    def setDetune(self,detune):
        self.detune = detune*self.maxDetuneRatio
        self.setFrequency()
    
    def setWaveForm(self,waveform):
        match waveform.lower():
            case "sine":
                self.voices = [Sine(self.frequency, self.samplerate) for index in self.voices]
            case "saw":
                self.voices = [Saw(self.frequency, self.samplerate) for index in self.voices]
            case "square":
                self.voices = [Square(self.frequency, self.samplerate) for index in self.voices]
            case "triangle":
                self.voices = [Triangle(self.frequency, self.samplerate) for index in self.voices]
        self.setFrequency()

    def setVoices(self,voices):
        if len(self.voices) < voices:
            for i in range(voices-len(self.voices)):
                self.voices.append(Sine(self.frequency, self.samplerate))
        elif len(self.voices) > voices:
            self.voices[:voices]
        self.setFrequency()

OscillatorModule(44100,4,0.5,440)